from ..testdata.helper import create_user


def get_token(postgres_client, make_post_request):
    user = create_user("user1", "password")
    cur = postgres_client.cursor()
    cur.execute("INSERT INTO users (id, login, password) VALUES (%s, %s, %s)", tuple(user.values()))
    postgres_client.commit()

    response = make_post_request('/auth/login', data={
        "login": "user1",
        "password": "password"
    })

    return response.body['access_token']


def test_create(make_post_request, redis_client, postgres_client):
    access_token = get_token(postgres_client, make_post_request)
    data = {
        'name': 'role0',
        'permissions': ['admin', 'superuser']
    }
    response = make_post_request('/role', data=data, headers={
        "Authorization": "Bearer {}".format(access_token)
    })

    assert response.body['id']


def test_update(make_post_request, make_put_request, make_get_request, redis_client, postgres_client):
    access_token = get_token(postgres_client, make_post_request)
    data = {
        'name': 'role1',
        'permissions': ['admin']
    }
    response = make_post_request('/role', data=data, headers={
        "Authorization": "Bearer {}".format(access_token)
    })

    data = {
        'name': 'role1',
        'permissions': ['admin', 'superuser']
    }
    response = make_put_request('/role/{}'.format(response.body['id']), data=data, headers={
        "Authorization": "Bearer {}".format(access_token)
    })

    response = make_get_request('/role/{}'.format(response.body['id']), headers={
        "Authorization": "Bearer {}".format(access_token)
    })

    assert len(response.body['permissions']) == 2


def test_delete(make_post_request, make_delete_request, make_get_request, redis_client, postgres_client):
    access_token = get_token(postgres_client, make_post_request)
    data = {
        'name': 'role2',
        'permissions': ['admin']
    }
    response = make_post_request('/role', data=data, headers={
        "Authorization": "Bearer {}".format(access_token)
    })
    role_id = response.body['id']

    response = make_delete_request('/role/{}'.format(role_id), headers={
        "Authorization": "Bearer {}".format(access_token)
    })

    assert response.body['success'] is True

    response = make_get_request('/role/{}'.format(role_id), headers={
        "Authorization": "Bearer {}".format(access_token)
    })

    print(1)


def test_read(make_post_request, make_get_request, redis_client, postgres_client):
    access_token = get_token(postgres_client, make_post_request)
    data = {
        'name': 'role3',
        'permissions': ['admin']
    }
    response = make_post_request('/role', data=data, headers={
        "Authorization": "Bearer {}".format(access_token)
    })

    response = make_get_request('/role/{}'.format(response.body['id']), headers={
        "Authorization": "Bearer {}".format(access_token)
    })

    assert response.body['name'] == data['name']
    assert response.body['permissions'] == data['permissions']
