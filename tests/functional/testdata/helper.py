def create_user(make_post_request, login='user', password='password'):
    response = make_post_request('/user', data={
        "login": login,
        "password": password
    })


def get_token(make_post_request):
    create_user(make_post_request)

    response = make_post_request('/auth/login', data={
        "login": "user",
        "password": "password"
    })

    return response.body['access_token']
