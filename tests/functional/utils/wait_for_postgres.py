import os
import time
import asyncio
import socket

import backoff
import psycopg2
from psycopg2.extensions import connection as _connection
from psycopg2.extras import DictCursor

POSTGRES_DBNAME = os.getenv('POSTGRES_DBNAME', 'auth')
POSTGRES_USER = os.getenv('POSTGRES_USER', 'postgres')
POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD', 'password')
POSTGRES_HOST = os.getenv('POSTGRES_HOST', 'postgres')
POSTGRES_PORT = os.getenv('POSTGRES_PORT', 5432)


@backoff.on_exception(backoff.expo, (socket.gaierror, psycopg2.OperationalError), max_time=30)
def wait():
    dsl = {
        'dbname': POSTGRES_DBNAME,
        'user': POSTGRES_USER,
        'password': POSTGRES_PASSWORD,
        'host': POSTGRES_HOST,
        'port': POSTGRES_PORT
    }

    connection = psycopg2.connect(**dsl, cursor_factory=DictCursor)
    connection.close()


if __name__ == '__main__':
    wait()
