from flask import Blueprint, request
from xmltodict import parse

hooks = Blueprint('hooks', __name__)

@hooks.route('/new', methods=['POST'])
def index():
    data = parse(request.data)
    yt_video = data['feed']['entry']['id']
    return yt_video