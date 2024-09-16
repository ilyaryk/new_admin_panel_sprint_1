import sqlite3

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
from dataclass import Genre






class PostgresSaver():
    def __init__(pg_conn):
        self.pg_conn = pg_conn


class SQLiteLoader():
    def __init__(connection):
        self.connection = connection

    def extract_data(sqlite_cursor: sqlite3.Cursor) -> Generator[list[sqlite3.Row], None, None]:
        sqlite_cursor.execute('SELECT * FROM students')
        while results := sqlite_cursor.fetchmany(100):
            yield results

    def transform_data(sqlite_cursor: sqlite3.Cursor) -> Generator[list[Genre], None, None]:
        for batch in extract_data(sqlite_cursor):
            yield [Genre(**dict(student)) for student in batch]

    def load_data(sqlite_cursor: sqlite3.Cursor, pg_cursor: psycopg.Cursor):
        for batch in transform_data(sqlite_cursor):
            query = 'INSERT INTO students (id, name, class_name, age) VALUES (%s, %s, %s, %s) ON CONFLICT (id) DO NOTHING'
            batch_as_tuples = [astuple(student) for student in batch]
            pg_cursor.executemany(query, batch_as_tuples)


def load_from_sqlite(connection: sqlite3.Connection, pg_conn: _connection):
    """Основной метод загрузки данных из SQLite в Postgres"""
    # postgres_saver = PostgresSaver(pg_conn)
    # sqlite_loader = SQLiteLoader(connection)

    # data = sqlite_loader.load_movies()
    # postgres_saver.save_all_data(data)


if __name__ == '__main__':
    dsl = {'dbname': 'movies_database', 'user': 'app', 'password': '123qwe', 'host': '127.0.0.1', 'port': 5432}
    with sqlite3.connect('db.sqlite') as sqlite_conn, psycopg.connect(
        **dsl, row_factory=dict_row, cursor_factory=ClientCursor
    ) as pg_conn:
        load_from_sqlite(sqlite_conn, pg_conn)