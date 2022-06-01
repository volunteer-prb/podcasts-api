from flask import Blueprint

main = Blueprint('main', __name__)


@main.route('/')
def index():
    return 'Index'


@main.route('/list')
def profile():
    return 'List'
