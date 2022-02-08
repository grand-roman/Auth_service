from uuid import uuid4


def create_user(login: str, password: str):
    return {
        "uuid": str(uuid4()),
        "login": login,
        "password": password
    }
