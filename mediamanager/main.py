from flask import Blueprint, request

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return 'Index'

@main.route('/new', methods=['POST'])
def profile():
    data = request.json
    
    return 'List'