import sqlite3
from enum import Enum
import psycopg
from psycopg import ClientCursor, connection as _connection
from psycopg.rows import dict_row
from contextlib import closing
from dataclasses import astuple
from typing import Generator
from dataclass import Genre, FilmWork, Person, GenreFilmwork, PersonFilmwork
from ..config.settings import BATCH_SIZE


class Tables(Enum):
    GENRE = 'genre'
    PERSON = 'person'
    FILM_WORK = 'film_work'
    GENRE_FILM_WORK = 'genre_film_work'
    PERSON_FILM_WORK = 'person_film_work'


def extract_data(sqlite_cursor: sqlite3.Cursor, table: str) -> Generator[
        list[sqlite3.Row], None, None]:
    sqlite_cursor.execute(f'SELECT * FROM {table};')
    while results := sqlite_cursor.fetchmany(BATCH_SIZE):
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
            data = [
                PersonFilmwork(**dict(person_film)) for person_film in batch
                    ]
    yield {
        'table': table_name,
        'data': data
    }


class PostgresSaver():
    def __init__(self, pg_conn):
        self.pg_conn = pg_conn

    def save_all_data(self, data):
        pg_cursor = pg_conn.cursor()
        for table in data:
            if table['table'] == Tables.GENRE.value:
                query = 'INSERT INTO content.genre \
                (id, name, description, created_at, updated_at)\
                VALUES (%s, %s, %s, %s, %s) ON CONFLICT (id) DO NOTHING'
                batch_as_tuples = [astuple(genre) for genre in table['data']]
                pg_cursor.executemany(query, batch_as_tuples)

            if table['table'] == Tables.FILM_WORK.value:
                query = 'INSERT INTO content.film_work \
                (id, title, description, creation_date, file_path,\
                rating, type, created_at, updated_at) VALUES \
                (%s, %s, %s, %s, %s, %s, %s, %s, %s) \
                ON CONFLICT (id) DO NOTHING'
                batch_as_tuples = [
                    astuple(film_work) for film_work in table['data']
                                   ]
                pg_cursor.executemany(query, batch_as_tuples)

            if table['table'] == Tables.PERSON.value:
                query = 'INSERT INTO content.person \
                (id, full_name, created_at, updated_at) \
                VALUES (%s, %s, %s, %s) ON CONFLICT (id) DO NOTHING'
                batch_as_tuples = [astuple(person) for person in table['data']]
                pg_cursor.executemany(query, batch_as_tuples)

            if table['table'] == Tables.PERSON_FILM_WORK.value:
                query = 'INSERT INTO content.person_film_work \
                (id, person_id, film_work_id, role, created_at) \
                VALUES (%s, %s, %s, %s, %s) ON CONFLICT (id) DO NOTHING'
                batch_as_tuples = [astuple(p_f_w) for p_f_w in table['data']]
                pg_cursor.executemany(query, batch_as_tuples)

            if table['table'] == Tables.GENRE_FILM_WORK.value:
                query = 'INSERT INTO content.genre_film_work \
                (id, genre_id, film_work_id, created_at) \
                VALUES (%s, %s, %s, %s) ON CONFLICT (id) DO NOTHING'
                batch_as_tuples = [astuple(p_f_w) for p_f_w in table['data']]
                pg_cursor.executemany(query, batch_as_tuples)


class SQLiteLoader():
    def __init__(self, connection):
        self.connection = connection

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
    dsl = {'dbname': 'postgres', 'user': 'app',
           'password': '123qwe', 'host': '127.0.0.1', 'port': 5432}
    with sqlite3.connect('db.sqlite') as sqlite_conn, psycopg.connect(
        **dsl, row_factory=dict_row, cursor_factory=ClientCursor
    ) as pg_conn:
        load_from_sqlite(sqlite_conn, pg_conn)
