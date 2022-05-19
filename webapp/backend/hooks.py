from flask import Blueprint, request, jsonify
from xmltodict import parse
from mediamanager.objects.video import Entry
from mediamanager.celery import download
from celery.execute import send_task

hooks = Blueprint('hooks', __name__)


@hooks.route('/new', methods=['POST'])
def index():
    data = parse(request.data)
    if 'feed' not in data or 'entry' not in data['feed']:
        return jsonify({'error': 'Invalid XML'}), 400
    yt_video = data['feed']['entry']
    entry = Entry(yt_video)
    download.delay(entry.to_json())
    # send_task("mediamanager.download", args=[entry.to_json()])
    return jsonify(entry), 200
