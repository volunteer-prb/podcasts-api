from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from mediamanager.objects.encoder import ObjectEncoder
from os import environ

# init SQLAlchemy so we can use it later in our models
db = SQLAlchemy()


def create_app():
    app = Flask(__name__)

    app.config['SECRET_KEY'] = environ.get("DB_SECRET")
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
    app.json_encoder = ObjectEncoder
    db.init_app(app)

    # blueprint for auth routes in our app
    from main import main as main_blueprint
    from hooks import hooks as hooks_blueprint

    app.register_blueprint(main_blueprint)
    app.register_blueprint(hooks_blueprint, url_prefix='/hooks')

    return app
