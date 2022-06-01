import atexit
import json
import traceback
from typing import Tuple, Dict

from flask import Flask, request, g, Response
from flask_migrate import Migrate
from os import environ
from apscheduler.schedulers.background import BackgroundScheduler
from flask_sqlalchemy_extension.model import SqlalchemyExtensionError
from werkzeug.exceptions import HTTPException

from app.encoder import ObjectEncoder
from app.celery.pubsubhubbub import resubscribe
from app.models import db


def create_app():
    app = Flask(__name__)

    app.config['SECRET_KEY'] = environ.get("DB_SECRET")
    app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('DATABASE_URI', 'sqlite:///db.sqlite')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.json_encoder = ObjectEncoder
    db.init_app(app)

    Migrate(app, db)

    @app.before_request
    def app_context():
        # Properties for SQLAlchemy REST extension
        g.per_page = int(request.args.get('per_page', 20))
        g.page = int(request.args.get('page', 1))
        filter_type = request.args.get('filter_type', 'and')
        filter_by = dict((k[len('filter_by_'):], v) for k, v in request.args.items()
                         if k.startswith('filter_by_') and len(k) > len('filter_by_'))
        order_by = dict((k[len('order_by_'):], v) for k, v in request.args.items()
                        if k.startswith('order_by_') and len(k) > len('order_by_'))
        g.complex_query = dict(
            filter_type=filter_type,
            filter_by=filter_by,
            order_by=order_by
        )
        g.includes = list(k[len('include_'):] for k, v in request.args.items()
                          if k.startswith('include_') and len(k) > len('include_'))

    @app.errorhandler(Exception)
    def errorhandler(e: Exception) -> Tuple[Dict, int]:
        def wrapper(e: Exception) -> Tuple[Dict, int]:
            if isinstance(e, HTTPException):
                return dict(
                    status='error',
                    message=str(e),
                ), e.code
            elif isinstance(e, SqlalchemyExtensionError):
                return dict(
                    status='error',
                    message=str(e),
                ), 500
            else:
                traceback.print_exc()
                return dict(
                    status='error',
                    message='Internal server error'
                ), 500

        db.session.rollback()
        return wrapper(e)

    @app.after_request
    def response_wrap(response: Response) -> Response:
        if response.status_code < 300 and response.get_json() is not None:
            response.data = json.dumps(dict(
                status='success',
                data=response.get_json(),
            ))
            response.headers['Content-Type'] = 'application/json'
        return response

    # blueprint for auth routes in our app
    from app.endpoints.main import main as main_blueprint
    from app.endpoints.hooks import hooks as hooks_blueprint
    from app.endpoints.channels import channels as channels_blueprint

    app.register_blueprint(main_blueprint)
    app.register_blueprint(hooks_blueprint, url_prefix='/hooks')
    app.register_blueprint(channels_blueprint, url_prefix='/channels')

    scheduler = BackgroundScheduler()
    scheduler.add_job(func=resubscribe, trigger="interval", seconds=600)
    scheduler.start()
    atexit.register(lambda: scheduler.shutdown())
    return app
