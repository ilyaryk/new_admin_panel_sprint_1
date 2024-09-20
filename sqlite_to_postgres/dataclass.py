from datetime import time
import sqlite3
from dataclasses import dataclass, astuple, field
from typing import Generator
from uuid import UUID

@dataclass
class Genre:
    id: UUID
    name: str
    description: str
    created: time
    modified: time

    def __post_init__(self):
        if isinstance(self.id, str):
            self.id = UUID(self.id)


@dataclass
class FilmWork:
    id: UUID
    name: str
    description: str
    creation_date: time
    rating: float
    type: str
    created: time
    modified: time

    def __post_init__(self):
        if isinstance(self.id, str):
            self.id = UUID(self.id)


@dataclass
class Person:
    id: UUID
    full_name: str
    created: time
    modified: time

    def __post_init__(self):
        if isinstance(self.id, str):
            self.id = UUID(self.id)


@dataclass
class GenreFilmwork:
    id: UUID
    genre_id: int
    film_work_id: int
    created: time


    def __post_init__(self):
        if isinstance(self.id, str):
            self.id = UUID(self.id)


@dataclass
class PersonFilmwork:
    id: UUID
    person_id: int
    film_work_id: int
    role: str
    created: time

    def __post_init__(self):
        if isinstance(self.id, str):
            self.id = UUID(self.id)


