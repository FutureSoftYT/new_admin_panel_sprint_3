import datetime
from time import sleep

import psycopg2
from redis.client import Redis

from config import *
from elastic_search_loader import ElasticsearchLoader
from logger import logger
from postgres_extractor import PostgresExtractor
from state import RedisStorage, State


def load_data(state: State, extractor: PostgresExtractor, es_loader: ElasticsearchLoader):
    # Get the last execution time and queue index from the state
    last_execution_time = state.get_state('last_execution_time')
    queue_index = int(state.get_state('queue_index', 0)) % len(TABLES_DATA.keys())
    execution_time = datetime.datetime.now().__str__()
    # Setting time to filter by modified column
    extractor.update_time(last_execution_time)

    # Getting current datas
    table, m2m, column_id = TABLES_DATA[queue_index]

    logger.info("Current queue %s, working on table %s, filtering time %s", *(queue_index, table, extractor.time))

    # Getting ids from the current table
    table_ids = extractor.load_table_ids(table)
    for batch_table_ids in table_ids:
        # If the current table is not the FilmWork table, then we need to get ids of FilmWork tables
        # according to the m2m tables
        if table != FILM_WORK_TABLE:
            film_work_ids = extractor.load_film_ids(m2m, column_id, batch_table_ids)
        else:
            film_work_ids = table_ids

        # Loop through the film_work_ids in batches and load films for each batch
        for batch_film_work_ids in film_work_ids:
            films = extractor.load_films(batch_film_work_ids)
            for batch_films in films:
                # Load data to Elasticsearch for each batch of films
                es_loader.load_data_to_es(batch_films)

    # Update the state with the current execution time and queue index
    # Update last_execution_time when completes iteration throw all tables
    queue_index += 1

    if queue_index == len(TABLES_DATA.keys()) or last_execution_time is None:
        state.set_state('last_execution_time', execution_time)
    state.set_state('queue_index', queue_index)


def main():
    storage = RedisStorage(redis_adapter=Redis.from_url(url=REDIS_URL))
    state = State(storage=storage)
    pg_connection = psycopg2.connect(**DSL)

    try:
        with pg_connection as conn:
            extractor = PostgresExtractor(conn, schema=SCHEMA_CONTENT)
            es_loader = ElasticsearchLoader(es_host=ES_HOST,
                                            es_port=ES_PORT,
                                            es_index=INDEX_NAME,
                                            mappings=ES_MAPPINGS,
                                            settings=ES_SETTINGS)
            while True:
                load_data(state, extractor, es_loader)
                sleep(2)
    finally:
        pg_connection.close()


if __name__ == "__main__":
    main()
