import datetime
from typing import List, Optional

from pydantic import BaseModel


class Person(BaseModel):
    id: str
    name: str


class FilmWork(BaseModel):
    id: str
    modified: datetime.datetime
    imdb_rating: Optional[float] = 0.00
    genre: List[Optional[str]]
    title: Optional[str]
    description: Optional[str]
    director: List[Optional[str]]
    actors_names: List[Optional[str]]
    writers_names: List[Optional[str]]
    actors: List[Optional[Person]]
    writers: List[Optional[Person]]

