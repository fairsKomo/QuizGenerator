from redis import Redis
from rq import Worker, Queue, Connection
import os
listen = ['default']

redis_conn = Redis.from_url(os.environ.get('REDIS_URL', 'redis://localhost:6379/0'))

if __name__ == '__main__':
    with Connection(redis_conn):
        worker = Worker(map(Queue, listen))
        worker.work()