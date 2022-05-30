from flask import Blueprint, g, request
from flask_sqlalchemy_extension.func import serialize

from app import db
from app.models.source_channels import SourceChannel

channels = Blueprint('channels', __name__)


@channels.route('/find', methods=['GET'])
def find_channels():
    return serialize(SourceChannel.complex_query(**g.complex_query).paginate(page=g.page, per_page=g.per_page),
                     include=g.includes)


@channels.route('/<int:id>', methods=['GET'])
def get_channel(id=None):
    return SourceChannel.query.filter_by(id=id).first_or_404().serialize(include=g.includes)


@channels.route('/', methods=['POST'])
@channels.route('/<int:id>', methods=['PUT'])
def create_or_update_channel(id=None):
    if id is not None:
        channel = SourceChannel.query.filter_by(id=id).first_or_404()
    else:
        channel = SourceChannel()

    channel.deserialize(request.json) \
        .check_constrains()

    db.session.add(channel)
    db.session.commit()
    return channel.serialize(include=g.includes)


@channels.route('/<int:id>', methods=['DELETE'])
def delete_channel(id=None):
    channel = SourceChannel.query.filter_by(id=id).first_or_404()
    db.session.delete(channel)
    db.session.commit()
    return {}
