import atexit

from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from mediamanager.objects.encoder import ObjectEncoder
from os import environ
from apscheduler.schedulers.background import BackgroundScheduler

from webapp.backend.subscriptions import resubscribe

# init SQLAlchemy so we can use it later in our models
db = SQLAlchemy()


def create_app():
    app = Flask(__name__)

    app.config['SECRET_KEY'] = environ.get("DB_SECRET")
    app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('DATABASE_URI', 'sqlite:///db.sqlite')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.json_encoder = ObjectEncoder
    db.init_app(app)

    Migrate(app, db)

    # blueprint for auth routes in our app
    from webapp.backend.main import main as main_blueprint
    from webapp.backend.hooks import hooks as hooks_blueprint

    app.register_blueprint(main_blueprint)
    app.register_blueprint(hooks_blueprint, url_prefix='/hooks')

    scheduler = BackgroundScheduler()
    scheduler.add_job(func=resubscribe, trigger="interval", seconds=60)
    scheduler.start()
    atexit.register(lambda: scheduler.shutdown())
    return app
