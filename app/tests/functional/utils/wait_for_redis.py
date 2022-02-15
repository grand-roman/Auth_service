import os
import time
import socket

import backoff
import redis

REDIS_HOST = os.getenv('REDIS_HOST', 'redis')
REDIS_PORT = os.getenv('REDIS_PORT', 6379)


@backoff.on_exception(backoff.expo, (socket.gaierror, redis.exceptions.ConnectionError), max_time=30)
def wait():
    connection = redis.Redis(REDIS_HOST, REDIS_PORT)
    if connection.ping():
        connection.close()
        return True
    else:
        time.sleep(1)


if __name__ == '__main__':
    wait()
