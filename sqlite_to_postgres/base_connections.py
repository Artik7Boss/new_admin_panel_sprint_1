import psycopg2
import sqlite3
from psycopg2.extras import DictCursor
from contextlib import contextmanager
import os

from load_data import main

sqlite_db_path = os.environ.get('DB_PATH')


dsn = {
    'dbname': os.environ.get('DB_NAME'),
    'user': os.environ.get('DB_USER'),
    'password': os.environ.get('DB_PASSWORD'),
    'host': os.environ.get('DB_HOST'),
    'port': os.environ.get('DB_PORT'),
    'options': os.environ.get('DB_OPTIONS'),
}


@contextmanager
def sqlite_connection(db_path: str):
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
    finally:
        conn.close()


def set_connections():
    pg_conn = None
    try:
        with sqlite_connection(sqlite_db_path) as sqlite_conn, psycopg2.connect(
            **dsn, cursor_factory=DictCursor
        ) as pg_conn:
            main(sqlite_conn, pg_conn)
    except (sqlite3.Error, psycopg2.Error) as _e:
        print("\nОшибка:", _e)
    finally:
        if pg_conn is not None:
            pg_conn.close()
