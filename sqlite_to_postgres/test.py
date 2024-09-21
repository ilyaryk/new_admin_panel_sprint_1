import sqlite3
from typing import Generator

def extract_data(sqlite_cursor: sqlite3.Cursor, table: str) -> Generator[list[sqlite3.Row], None, None]:
    sqlite_cursor.execute(f'SELECT * FROM {table};')
    while results := sqlite_cursor.fetchmany(100):
        yield results

if __name__ == '__main__':
    with sqlite3.connect('db.sqlite') as sqlite_conn:
        for i in extract_data(sqlite_conn.cursor(), 'genre'):
            print(i)