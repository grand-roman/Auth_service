import os
from hashlib import pbkdf2_hmac


def hash_password(password: str):
    alg = 'sha256'
    salt = os.environ.get("PASSWORD_SALT").encode()
    iterations = int(os.environ.get("PASSWORD_ITERATIONS", 32))

    hash_ = pbkdf2_hmac(alg, password.encode(), salt, iterations).hex()

    return "{}${}${}${}".format(alg, iterations, salt, hash_)
