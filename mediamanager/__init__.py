from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import environ

# init SQLAlchemy so we can use it later in our models
db = SQLAlchemy()

def create_app():
    app = Flask(__name__)

    app.config['SECRET_KEY'] = environ.get("DB_SECRET")
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'

    db.init_app(app)

    # blueprint for auth routes in our app
    from mediamanager.main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app