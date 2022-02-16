from ..testdata.helper import create_user

def test_login(make_post_request, redis_client, postgres_client):
    create_user(make_post_request)

    result = make_post_request('/auth/login', data={
        "login": "user",
        "password": "password"
    })

    assert ("access_token" in result.body) is True
    assert ("refresh_token" in result.body) is True


def test_update_access_token(make_post_request, redis_client, postgres_client):
    create_user(make_post_request)

    response = make_post_request('/auth/login', data={
        "login": "user",
        "password": "password"
    })
    access_token = response.body['access_token']
    refresh_token = response.body['refresh_token']

    response = make_post_request('/auth/refresh', headers={
        "Authorization": "Bearer {}".format(refresh_token)
    })
    new_access_token = response.body['access_token']
    new_refresh_token = response.body['refresh_token']

    assert access_token != new_access_token
    assert refresh_token != new_refresh_token


def test_get_login_history(make_get_request, make_post_request, redis_client, postgres_client):
    create_user(make_post_request)

    for i in range(3):
        response = make_post_request('/auth/login', data={
            "login": "user",
            "password": "password"
        })

    response = make_post_request('/auth/login', data={
        "login": "user",
        "password": "password"
    })

    access_token = response.body['access_token']
    response = make_get_request('/auth/history', headers={
        "Authorization": "Bearer {}".format(access_token)
    })

    assert len(response.body) == 4


def test_refresh_token_store(make_post_request, redis_client, postgres_client):
    pass


def test_access_token_expire(make_post_request, redis_client, postgres_client):
    pass


def test_refresh_token_expire(make_post_request, redis_client, postgres_client):
    pass
