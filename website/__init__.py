from flask import Flask

def create_app():
    app = Flask(__name__)

    from .view import view
    
    app.register_blueprint(view, url_prefix='/')

    return app