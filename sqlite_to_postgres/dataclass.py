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
    created_at: time
    updated_at: time

    def __post_init__(self):
        if isinstance(self.id, str):
            self.id = UUID(self.id)


@dataclass
class FilmWork:
    id: UUID
    title: str
    description: str
    creation_date: time
    file_path: str
    rating: float
    type: str
    created_at: time
    updated_at: time

    def __post_init__(self):
        if isinstance(self.id, str):
            self.id = UUID(self.id)


@dataclass
class Person:
    id: UUID
    full_name: str
    created_at: time
    updated_at: time

    def __post_init__(self):
        if isinstance(self.id, str):
            self.id = UUID(self.id)


@dataclass
class GenreFilmwork:
    id: UUID
    film_work_id: int
    genre_id: int
    created_at: time


    def __post_init__(self):
        if isinstance(self.id, str):
            self.id = UUID(self.id)


@dataclass
class PersonFilmwork:
    id: UUID
    film_work_id: int
    person_id: int
    role: str
    created_at: time

    def __post_init__(self):
        if isinstance(self.id, str):
            self.id = UUID(self.id)


