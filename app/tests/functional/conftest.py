import os
import pytest
import requests

from .settings import HTTPResponse, service_url, redis_host, redis_port
import psycopg2
from psycopg2.extras import DictCursor
import redis


@pytest.fixture(scope='session')
def postgres_client():
    dsl = {
        'dbname': os.getenv('POSTGRES_DBNAME', 'auth'),
        'user': os.getenv('POSTGRES_USER', 'postgres'),
        'password': os.getenv('POSTGRES_PASSWORD', 'password'),
        'host': os.getenv('POSTGRES_HOST', 'postgres'),
        'port': os.getenv('POSTGRES_PORT', 5432)
    }

    connection = psycopg2.connect(**dsl, cursor_factory=DictCursor)
    yield connection
    connection.close()


@pytest.fixture(scope='session')
def redis_client():
    client = redis.Redis(redis_host, redis_port)
    yield client
    client.close()


@pytest.fixture(autouse=True)
def es_data(postgres_client):
    cur = postgres_client.cursor()
    for table_name in ['users', 'login_events', 'roles', 'users_roles']:
        cur.execute("DELETE FROM {}".format(table_name))
    postgres_client.commit()


@pytest.fixture
def make_put_request():
    def inner(method: str, expected_status_code=200, data: dict = None, headers: dict = None) -> HTTPResponse:
        data = data or {}
        headers = headers or {}
        url = service_url + '/api/v1' + method
        with requests.put(url, json=data, headers=headers) as response:
            assert response.status_code == expected_status_code
            return HTTPResponse(
                body=response.json(),
                headers=response.headers,
                status=response.status_code,
            )

    return inner


@pytest.fixture
def make_delete_request():
    def inner(method: str, expected_status_code=200, data: dict = None, headers: dict = None) -> HTTPResponse:
        data = data or {}
        headers = headers or {}
        url = service_url + '/api/v1' + method
        with requests.delete(url, json=data, headers=headers) as response:
            assert response.status_code == expected_status_code
            return HTTPResponse(
                body=response.json(),
                headers=response.headers,
                status=response.status_code,
            )

    return inner


@pytest.fixture
def make_post_request():
    def inner(method: str, expected_status_code=200, data: dict = None, headers: dict = None) -> HTTPResponse:
        data = data or {}
        headers = headers or {}
        url = service_url + '/api/v1' + method
        with requests.post(url, json=data, headers=headers) as response:
            assert response.status_code == expected_status_code
            return HTTPResponse(
                body=response.json(),
                headers=response.headers,
                status=response.status_code,
            )

    return inner


@pytest.fixture
def make_get_request():
    def inner(method: str, expected_status_code=200, params: dict = None, headers: dict = None) -> HTTPResponse:
        params = params or {}
        headers = headers or {}
        url = service_url + '/api/v1' + method
        with requests.get(url, params=params, headers=headers) as response:
            assert response.status_code == expected_status_code
            return HTTPResponse(
                body=response.json(),
                headers=response.headers,
                status=response.status_code,
            )

    return inner

# @pytest.fixture(autouse=True)
# def redis_flush(redis_client):
#     await redis_client.flushall()
#     print('flush redis')
#     return
