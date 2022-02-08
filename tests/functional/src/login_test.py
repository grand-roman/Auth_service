from http import HTTPStatus
import pytest

# from ..testdata.data import FILMS
from ..testdata.helper import create_user

import requests


def test_login(make_post_request, redis_client, postgres_client):
    user = create_user("user1", "password")
    cur = postgres_client.cursor()
    cur.execute("INSERT INTO users (id, login, password) VALUES (%s, %s, %s)", tuple(user.values()))
    postgres_client.commit()

    result = make_post_request('/login', data={
        "login": "user1",
        "password": "password"
    })

    assert ("access_token" in result.body) is True
    assert ("refresh_token" in result.body) is True


def test_update_access_token(make_post_request, redis_client, postgres_client):
    user = create_user("user2", "password")
    cur = postgres_client.cursor()
    cur.execute("INSERT INTO users (id, login, password) VALUES (%s, %s, %s)", tuple(user.values()))
    postgres_client.commit()

    response = make_post_request('/login', data={
        "login": "user2",
        "password": "password"
    })
    access_token = response.body['access_token']
    refresh_token = response.body['refresh_token']

    response = make_post_request('/refresh', headers={
        "Authorization": "Bearer {}".format(refresh_token)
    })
    new_access_token = response.body['access_token']
    new_refresh_token = response.body['refresh_token']

    assert access_token != new_access_token
    assert refresh_token != new_refresh_token


def test_get_login_history(make_get_request, make_post_request, redis_client, postgres_client):
    user = create_user("user3", "password")
    cur = postgres_client.cursor()
    cur.execute("INSERT INTO users (id, login, password) VALUES (%s, %s, %s)", tuple(user.values()))
    postgres_client.commit()

    for i in range(3):
        response = make_post_request('/login', data={
            "login": "user3",
            "password": "password"
        })

    response = make_post_request('/login', data={
        "login": "user3",
        "password": "password"
    })

    access_token = response.body['access_token']
    response = make_get_request('/history', headers={
        "Authorization": "Bearer {}".format(access_token)
    })

    assert len(response.body) == 4


def test_refresh_token_store(make_post_request, redis_client, postgres_client):
    pass


def test_access_token_expire(make_post_request, redis_client, postgres_client):
    pass


def test_refresh_token_expire(make_post_request, redis_client, postgres_client):
    pass
