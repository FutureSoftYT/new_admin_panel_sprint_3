import logging
from typing import List, Optional, Mapping, Any

from elasticsearch import Elasticsearch, helpers

from backoff import backoff
from logger import logger
from models import FilmWork


class ElasticsearchLoader:

    @backoff()
    def __init__(
            self,
            es_host: str = "localhost",
            es_port: int = 9200,
            es_index: str = "movies",
            mappings: Mapping[str, Any] | None = None,
            settings: Mapping[str, Any] | None = None
    ) -> None:
        """
           Initialize the ElasticsearchLoader.

           :param es_host: The hostname or IP address of the Elasticsearch server. Default is 'localhost'.
           :param es_port: The port number of the Elasticsearch server. Default is 9200.
           :param es_index: The name of the Elasticsearch index to use. Default is 'movies'.
           :param mappings: Optional mappings for the Elasticsearch index. Default is None.
           :param settings: Optional settings for the Elasticsearch index. Default is None.
       """
        self.es_host = es_host
        self.es_port = es_port
        self.es_index = es_index
        self.es = Elasticsearch("http://localhost:9200")

        if self.is_index_exists() is False:
            logger.info("Creating index %s ....", (es_index,))
            try:
                # Creating index
                self.es.indices.create(index=es_index, mappings=mappings, settings=settings)
                logger.info("Index %s created successfully!", (es_index,))
            except Exception as e:
                logging.error("Something went wrong while creating index %s , Error: %s", (es_index, e))
                raise Exception

    def is_index_exists(self) -> bool:
        """
        Check if the Elasticsearch index exists.

        :return: True if the index exists, False otherwise.
        """
        return self.es.indices.exists(index=self.es_index).body

    @backoff()
    def load_data_to_es(self, films_data: List[Optional[FilmWork]]) -> None:
        """
            Loads data to ElasticSearch.

            :param films_data: List of FilmWorks to load.
            :return: None
        """
        documents = []
        for film in films_data:
            doc = {
                "_index": self.es_index,
                "_id": film.id,
                "_source": film.model_dump()
            }
            documents.append(doc)

        try:
            helpers.bulk(self.es, documents)
            logger.info('Loading complete! %s Films uploaded!', len(documents))
        except Exception as e:
            logging.error('Loading to Elastic Search failed, Error: %s', (e,))
            raise Exception
