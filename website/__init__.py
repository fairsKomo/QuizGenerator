from flask import Flask
from rq import Queue
from redis import Redis

r = Redis()
q = Queue(connection=r)

def create_app():
    app = Flask(__name__)

    from .view import view
    
    app.register_blueprint(view, url_prefix='/')

    return app