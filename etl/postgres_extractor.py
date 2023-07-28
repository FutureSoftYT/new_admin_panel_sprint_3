import datetime
import uuid
from typing import List, Optional, Union, Generator

from psycopg2._psycopg import connection
from psycopg2.extras import DictCursor

from backoff import backoff
from logger import logger
from models import FilmWork


class PostgresExtractor:
    chunk_size: int = 100
    time: Optional[Union[datetime.datetime, str]] = None

    def __init__(self, conn: connection, schema: str = 'public') -> None:
        """
        Initializes the PostgresExtractor instance.

        Args:
            conn (connection): A PostgreSQL database connection object.
            schema (str): The schema of the database to be used. Default is 'public'.
        :return: None
        """
        self.connection = conn
        self.schema = schema

    def update_time(self, time: Optional[Union[datetime.datetime, str]]):
        """
        Update the time used for time-based filtering during data extraction.
        Example time: 2023-07-27 20:30:42.494066

        Args:
            time (datetime.datetime | str | None): The time to use for filtering.
                                                  Can be a datetime object, a string representing
                                                  a datetime, or None for no filtering.
        """
        if isinstance(time, datetime.datetime):
            self.time = time
            return

        if time is None:
            self.time = None
            return

        try:
            self.time = datetime.datetime.fromisoformat(time)
            return
        except Exception as e:
            logger.error('Error occurred during converting %s to datetime, time was set to None, Error: %s', time, e)
            self.time = None

    @backoff()
    def load_table_ids(self, table: str) -> Generator[List[uuid.UUID], None, None]:
        """
        Fetches the 'id' values from the specified table in the Postgres database.

        Args:
            table (str): The name of the table from which to retrieve the 'id' values.

        Yields:
            Generator[List[uuid.UUID], None, None]: A generator that yields batches of 'id' values
                                                   fetched from the database table.

        Note:
            The function uses an SQL query to retrieve the 'id' values from the specified table.
            If a self.time value is provided, it includes a WHERE clause in the query to filter
            the 'modified' column based on the provided time.
        """
        cursor = self.connection.cursor()
        query = f"""SELECT id
        FROM {self.schema}.{table}
        {"WHERE modified > %s" if self.time else ''}
        ORDER BY modified
        """
        try:
            # Execute the SQL query with optional time-based filtering
            cursor.execute(query, (self.time,))

            # Fetch data from the database in batches using fetchmany and yield each batch
            while data := cursor.fetchmany(self.chunk_size):
                yield data
        finally:
            cursor.close()

    @backoff()
    def load_film_ids(self, m2m_table: str, column_id: str, ids: List[uuid.UUID]) -> Generator[
        List[uuid.UUID], None, None]:
        """
        Fetches FilmWork 'id' values based on the provided m2m_table and column_id.

        Args:
            m2m_table (str): The name of the m2m table to join with the FilmWork table.
            column_id (str): The column ID representing the relationship with FilmWork.
            ids (List[uuid.UUID]): A list of UUIDs representing the IDs to match in the m2m_table.

        Yields:
            Generator[List[uuid.UUID], None, None]: A generator that yields batches of 'id' values
                                                   fetched from the database based on the m2m_table and ids.

        """
        cursor = self.connection.cursor()

        query = f"""
        SELECT fw.id
        FROM {self.schema}.film_work fw
        LEFT JOIN {self.schema}.{m2m_table} m2mfw ON m2mfw.film_work_id = fw.id
        WHERE m2mfw.{column_id} IN ({', '.join(['%s'] * len(ids))})
        ORDER BY fw.modified
        """

        try:
            cursor.execute(query, ids)
            while data := cursor.fetchmany(self.chunk_size):
                yield data
        finally:
            cursor.close()

    @backoff()
    def load_films(self, film_ids: List[uuid.UUID]) -> Generator[List[FilmWork], None, None]:
        """
        Fetches film data based on the provided film_ids.

        Args:
            film_ids (List[uuid.UUID]): A list of UUIDs representing the FilmWork IDs to retrieve.

        Yields:
            Generator[List[FilmWork], None, None]: A generator that yields batches of FilmWork objects
                                                  fetched from the database based on the film_ids.
        """

        cursor = self.connection.cursor(cursor_factory=DictCursor)

        query = f"""
SELECT
    fw.id,
    fw.rating AS imdb_rating,
    fw.description,
    fw.title,
    COALESCE(array_agg(DISTINCT p.full_name) FILTER (WHERE pfw.role = 'actor'), ARRAY[]::text[]) AS "actors_names",
    COALESCE(array_agg(DISTINCT p.full_name) FILTER (WHERE pfw.role = 'writer'), ARRAY[]::text[]) AS "writers_names",
    COALESCE(array_agg(DISTINCT p.full_name) FILTER (WHERE pfw.role = 'director'), ARRAY[]::text[]) AS "director",
    array_agg(DISTINCT g.name) as genre,
   COALESCE (
       json_agg(
           DISTINCT jsonb_build_object(
               'id', p.id,
               'name', p.full_name
           )
       ) FILTER (WHERE p.id is not null and pfw.role = 'actor'),
       '[]'
   ) as actors,
   COALESCE (
       json_agg(
           DISTINCT jsonb_build_object(
               'id', p.id,
               'name', p.full_name
           )
       ) FILTER (WHERE p.id is not null and pfw.role = 'writer'),
       '[]'
   ) as writers
FROM {self.schema}.film_work fw
LEFT JOIN {self.schema}.person_film_work pfw ON pfw.film_work_id = fw.id
LEFT JOIN {self.schema}.person p ON p.id = pfw.person_id
LEFT JOIN {self.schema}.genre_film_work gfw ON gfw.film_work_id = fw.id
LEFT JOIN {self.schema}.genre g ON g.id = gfw.genre_id
WHERE fw.id  IN ({', '.join(['%s'] * len(film_ids))})
GROUP BY fw.id, fw.rating, fw.description, fw.title;
"""
        try:
            cursor.execute(query, film_ids)
            while rows := cursor.fetchmany(self.chunk_size):
                yield [FilmWork(**row) for row in rows]
        finally:
            cursor.close()
