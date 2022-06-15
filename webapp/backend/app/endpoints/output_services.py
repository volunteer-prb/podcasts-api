from flask import Blueprint, g, request
from flask_sqlalchemy_extension.func import serialize
from werkzeug.exceptions import BadRequest

from app import db
from app.models.output_services import OutputService, TelegramOutputService
from app.models.source_channels import SourceChannelOutputService

services = Blueprint('output_services', __name__)


@services.route('/find', methods=['GET'])
def find_outputs():
    """
    Endpoint provide search function to select output services from database,
    order and paginate results.

    Example:
        # select 20 items at page 1
        curl --location --request GET 'http://localhost:5000/outputs/find?page=1&per_page=20'

        # select 20 items at page 1 contains word "popular" (case insensitive) in title
        curl --location --request GET \
            'http://localhost:5000/outputs/find?page=1&per_page=20&filter_by_title__ilike=%popular%'

    Returns:
        Serialized output services and pagination or raise an exception
    """
    return serialize(OutputService.complex_query(**g.complex_query).paginate(page=g.page, per_page=g.per_page),
                     include=g.includes)


@services.route('/<int:id>', methods=['GET'])
def get_output(id=None):
    """
    Endpoint select output services by its id

    Example:
        curl --location --request GET 'http://localhost:5000/outputs/1'

    Returns:
        Serialized output service or raise an exception
    """
    return OutputService.query.filter_by(id=id).first_or_404().serialize(include=g.includes)


@services.route('/', methods=['POST'])
@services.route('/<int:id>', methods=['PUT'])
def create_or_update_channel(id=None):
    """
    Endpoint provide create and update functions for manipulate output services.

    Example:
        # create new
        curl --location --request POST 'http://localhost:5000/outputs/' \
            --header 'Content-Type: application/json' \
            --data-raw '{
                "title": "Popular politic",
                "type": "telegram",
                "channel_id": -1000000000000,
                "sources": [1, 2, 3]
            }'

        # update existing
        curl --location --request PUT 'http://localhost:5000/outputs/2' \
            --header 'Content-Type: application/json' \
            --data-raw '{
                "title": "Politic popular",
                "type": "telegram",
                "channel_id": -1000000000000,
                "sources": [1, 2, 3]
            }'

    Returns:
        Serialized output service or raise an exception
    """
    if 'type' not in request.json:
        raise BadRequest('Missing required property `type`')
    match request.json['type']:
        case 'telegram': base_class = TelegramOutputService
        case _type:
            raise BadRequest(f'Unsupported output service type: {_type}')

    if id is not None:
        output_service = base_class.query.filter_by(id=id).first_or_404()
    else:
        output_service = base_class()

    # deserialize json body to object
    output_service.deserialize(request.json)
    output_service.check_constrains()

    if 'sources' in request.json:
        # Extract only `id` from request body
        _sources = request.json['sources']
        _sources = [source['source_channel_id'] if isinstance(source, dict) and 'source_channel_id' in source else source
                    for source in _sources]

        # Select exists sources in relation table
        prev_sources = output_service.sources

        # Mark to delete all sources doesn't exist in request body list
        for excluded_source in [source for source in prev_sources if source.source_channel_id not in _sources]:
            db.session.delete(excluded_source)

        # Create new sources doesn't exist in relation table
        new_sources = []
        exists_sources = [source.source_channel_id for source in prev_sources if source.source_channel_id in _sources]
        for source in _sources:
            if source not in exists_sources:
                new_sources.append(SourceChannelOutputService(
                    output_service=output_service,
                    source_channel_id=source
                ))
        db.session.add_all(new_sources)

    # save to db
    db.session.add(output_service)
    db.session.commit()

    return output_service.serialize(include=g.includes)


@services.route('/<int:id>', methods=['DELETE'])
def delete_channel(id=None):
    """
    Endpoint provide delete function for delete output service

    Example:
        curl --location --request DELETE 'http://localhost:5000/outputs/2'

    Returns:
        Empty dict if ok or raise an exception
    """
    output_service = OutputService.query.filter_by(id=id).first_or_404()

    # Cascade delete sources
    for source in output_service.sources:
        db.session.delete(source)

    db.session.delete(output_service)
    db.session.commit()
    return {}
