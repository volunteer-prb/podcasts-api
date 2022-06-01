from flask import Blueprint, g, request
from flask_sqlalchemy_extension.func import serialize
from werkzeug.exceptions import BadRequest

from app import db
from app.celery import pubsubhubbub
from app.models.source_channels import SourceChannel

channels = Blueprint('channels', __name__)


@channels.route('/find', methods=['GET'])
def find_channels():
    """
    Endpoint provide search function to select channel sources from database,
    order and paginate results.

    Example:
        # select 20 items at page 1
        curl --location --request GET 'http://localhost:5000/channels/find?page=1&per_page=20'

        # select 20 items at page 1 contains word "popular" (case insensitive) in title
        curl --location --request GET \
            'http://localhost:5000/channels/find?page=1&per_page=20&filter_by_title__ilike=%popular%'

    Returns:
        Serialized source channels and pagination or raise an exception
    """
    return serialize(SourceChannel.complex_query(**g.complex_query).paginate(page=g.page, per_page=g.per_page),
                     include=g.includes)


@channels.route('/<int:id>', methods=['GET'])
def get_channel(id=None):
    """
    Endpoint select channel by its id

    Example:
        curl --location --request GET 'http://localhost:5000/channels/1'

    Returns:
        Serialized source channel or raise an exception
    """
    return SourceChannel.query.filter_by(id=id).first_or_404().serialize(include=g.includes)


@channels.route('/', methods=['POST'])
@channels.route('/<int:id>', methods=['PUT'])
def create_or_update_channel(id=None):
    """
    Endpoint provide create and update functions for manipulate channel sources.

    Example:
        # create new
        curl --location --request POST 'http://localhost:5000/channels/' \
            --header 'Content-Type: application/json' \
            --data-raw '{
                "channel_id": "UC7Elc-kLydl-NAV4g204pDQ",
                "title": "Popular politic",
                "pubsubhubbub_mode": "subscribe"
            }'

        # update existing
        curl --location --request PUT 'http://localhost:5000/channels/2' \
            --header 'Content-Type: application/json' \
            --data-raw '{
                "channel_id": "UC7Elc-kLydl-NAV4g204pDQ",
                "title": "Popular politic",
                "pubsubhubbub_mode": "unsubscribe"
            }'

    Returns:
        Serialized channel or raise an exception
    """
    if id is not None:
        channel = SourceChannel.query.filter_by(id=id).first_or_404()
    else:
        channel = SourceChannel()

    # deserialize json body to object
    channel.deserialize(request.json) \
        .check_constrains()

    # additional checks
    if channel.pubsubhubbub_mode.lower() not in ['subscribe', 'unsubscribe']:
        raise BadRequest('Column `pubsubhubbub_mode` must be "subscribe" or "unsubscribe"')

    channel.pubsubhubbub_mode = channel.pubsubhubbub_mode.lower()

    # save to db
    db.session.add(channel)
    db.session.commit()

    # change subscription mode
    pubsubhubbub.subscribe.delay(channel.channel_id, mode_subscribe=channel.pubsubhubbub_mode)

    return channel.serialize(include=g.includes)


@channels.route('/<int:id>', methods=['DELETE'])
def delete_channel(id=None):
    """
    Endpoint provide delete function for delete source channel

    Example:
        curl --location --request DELETE 'http://localhost:5000/channels/2'

    Returns:
        Empty dict if ok or raise an exception
    """
    channel = SourceChannel.query.filter_by(id=id).first_or_404()
    db.session.delete(channel)
    db.session.commit()
    return {}
