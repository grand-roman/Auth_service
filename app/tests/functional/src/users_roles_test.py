def get_token(postgres_client, make_post_request):
    response = make_post_request('/user', data={
        "login": "user1",
        "password": "password"
    })

    user_id = response.body['id']

    response = make_post_request('/auth/login', data={
        "login": "user1",
        "password": "password"
    })

    return response.body['access_token'], user_id


def create_role(make_post_request, access_token):
    data = {
        'name': 'role0',
        'permissions': ['admin', 'superuser']
    }
    response = make_post_request('/role', data=data, headers={
        "Authorization": "Bearer {}".format(access_token)
    })
    return response.body['id']


def test_set_user_role(make_post_request, redis_client, postgres_client):
    access_token, user_id = get_token(postgres_client, make_post_request)
    role_id = create_role(make_post_request, access_token)

    response = make_post_request('/user/{}/role/{}'.format(user_id, role_id), headers={
        "Authorization": "Bearer {}".format(access_token)
    })

    assert len(response.body) == 1
    assert response.body[0]['id'] == role_id


def test_get_user_role(make_post_request, make_put_request, make_get_request, redis_client, postgres_client):
    access_token, user_id = get_token(postgres_client, make_post_request)
    role_id = create_role(make_post_request, access_token)

    response = make_post_request('/user/{}/role/{}'.format(user_id, role_id), headers={
        "Authorization": "Bearer {}".format(access_token)
    })

    response = make_get_request('/user/{}/role'.format(user_id), headers={
        "Authorization": "Bearer {}".format(access_token)
    })

    assert len(response.body) == 1
    assert response.body[0]['id'] == role_id


def test_delete_user_role(make_post_request, make_delete_request, make_get_request, redis_client, postgres_client):
    access_token, user_id = get_token(postgres_client, make_post_request)
    role_id = create_role(make_post_request, access_token)

    response = make_post_request('/user/{}/role/{}'.format(user_id, role_id), headers={
        "Authorization": "Bearer {}".format(access_token)
    })

    response = make_delete_request('/user/{}/role/{}'.format(user_id, role_id), headers={
        "Authorization": "Bearer {}".format(access_token)
    })

    assert response.body['success'] is True

    response = make_get_request('/user/{}/role'.format(user_id, role_id), headers={
        "Authorization": "Bearer {}".format(access_token)
    })

    assert len(response.body) == 0
