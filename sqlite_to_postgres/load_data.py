import sqlite3
from enum import Enum
import psycopg
from psycopg import ClientCursor, connection as _connection
from psycopg.rows import dict_row
import os
import sqlite3
from contextlib import closing
from dataclasses import dataclass, astuple
from typing import Generator
from uuid import UUID

import psycopg
from dotenv import load_dotenv
from psycopg.rows import dict_row
from dataclass import Genre, FilmWork, Person, GenreFilmwork, PersonFilmwork


class Tables(Enum):
    GENRE = 'genre'
    PERSON = 'person'
    FILM_WORK = 'film_work'
    GENRE_FILM_WORK = 'genre_film_work'
    PERSON_FILM_WORK = 'person_film_work'


def extract_data(sqlite_cursor: sqlite3.Cursor, table: str) -> Generator[list[sqlite3.Row], None, None]:
    sqlite_cursor.execute(f'SELECT * FROM {table};')
    while results := sqlite_cursor.fetchmany(100):
        yield results

def transform_data(sqlite_cursor, table_name):
    for batch in extract_data(sqlite_cursor, table_name):
        if table_name == Tables.GENRE.value:
            data = [Genre(**dict(genre)) for genre in batch]
        if table_name == Tables.PERSON.value:
            data = [Person(**dict(person)) for person in batch]
        if table_name == Tables.FILM_WORK.value:
            data = [FilmWork(**dict(film)) for film in batch]
        if table_name == Tables.GENRE_FILM_WORK.value:
            data = [GenreFilmwork(**dict(genre_film)) for genre_film in batch]
        if table_name == Tables.PERSON_FILM_WORK.value:
            data = [PersonFilmwork(**dict(person_film)) for person_film in batch]
    print(table_name)
    yield {
        'table': table_name,
        'data': data
    }
class PostgresSaver():
    def __init__(self, pg_conn):
        self.pg_conn = pg_conn

    def save_all_data(self, data):
        print([i for i in data])
        pg_cursor = pg_conn.cursor()
        if data['table'] == Tables.GENRE.value:
            for batch in data:
                query = 'INSERT INTO genre (id, name, description, created, modified) \
                VALUES (%s, %s, %s, %s, %s) ON CONFLICT (id) DO NOTHING'
                batch_as_tuples = [astuple(genre) for genre in batch]
                pg_cursor.executemany(query, batch_as_tuples)
        
        if data['table'] == Tables.FILM_WORK.value:
            for batch in data:
                query = 'INSERT INTO film_work (id, title, description, creation_date, \
                rating, type, created, modified) VALUES (%s, %s, %s, %s, %s, %s, %s, %s) ON CONFLICT (id) DO NOTHING'
                batch_as_tuples = [astuple(genre) for genre in batch]
                pg_cursor.executemany(query, batch_as_tuples)

        if data['table'] == Tables.PERSON.value:
            for batch in data:
                query = 'INSERT INTO person (id, full_name, created, modified) \
                VALUES (%s, %s, %s, %s) ON CONFLICT (id) DO NOTHING'
                batch_as_tuples = [astuple(genre) for genre in batch]
                pg_cursor.executemany(query, batch_as_tuples)
        
        if data['table'] == Tables.PERSON_FILM_WORK.value:
            for batch in data:
                query = 'INSERT INTO person_film_work (id, person_id, film_work_id, role, created) \
                VALUES (%s, %s, %s, %s, %s) ON CONFLICT (id) DO NOTHING'
                batch_as_tuples = [astuple(genre) for genre in batch]
                pg_cursor.executemany(query, batch_as_tuples)

        if data['table'] == Tables.PERSON_FILM_WORK.value:
            for batch in data:
                query = 'INSERT INTO genre_film_work (id, genre_id, film_work_id, created) \
                VALUES (%s, %s, %s, %s) ON CONFLICT (id) DO NOTHING'
                batch_as_tuples = [astuple(genre) for genre in batch]
                pg_cursor.executemany(query, batch_as_tuples)


class SQLiteLoader():
    def __init__(self, connection):
        self.connection = connection

    def transform_genre(self, sqlite_cursor: sqlite3.Cursor) -> Generator[list[Genre], None, None]:
        for batch in extract_data(sqlite_cursor, 'genre'):
            yield [Genre(**dict(genre)) for genre in batch]
    
    def transform_film_work(sqlite_cursor: sqlite3.Cursor) -> Generator[list[FilmWork], None, None]:
        for batch in extract_data(sqlite_cursor, 'film_work'):
            yield [FilmWork(**dict(filmwork)) for filmwork in batch]

    def load_movies(self):
        with closing(self.connection.cursor()) as cursor:
            cursor.row_factory = sqlite3.Row
            for table in Tables:
                for batch in transform_data(cursor, table.value):
                    yield batch


def load_from_sqlite(connection: sqlite3.Connection, pg_conn: _connection):
    """Основной метод загрузки данных из SQLite в Postgres"""
    postgres_saver = PostgresSaver(pg_conn=pg_conn)
    sqlite_loader = SQLiteLoader(connection)

    data = sqlite_loader.load_movies()
    postgres_saver.save_all_data(data)


if __name__ == '__main__':
    dsl = {'dbname': 'movies_database', 'user': 'app', 'password': '123qwe', 'host': '127.0.0.1', 'port': 5432}
    with sqlite3.connect('db.sqlite') as sqlite_conn, psycopg.connect(
        **dsl, row_factory=dict_row, cursor_factory=ClientCursor
    ) as pg_conn:
        load_from_sqlite(sqlite_conn, pg_conn)