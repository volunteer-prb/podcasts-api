from flask import Blueprint

from app.celery import publisher
from app.models.video import Record

records = Blueprint('records', __name__)


@records.route('/publish/<int:id>', methods=['POST', 'PUT'])
def publish_record(id=None):
    """
    Endpoint query record by ID and create publish task in celery for publisher
    """

    record = Record.query.filter_by(id=id).first_or_404()

    recipients = []
    for output_service in record.youtube_video.channel.outputs:
        service = output_service.output_service
        match service.type:
            case 'telegram': recipients.append(dict(
                _type_='TelegramRecipient',
                channel_id=service.channel_id,
            ))

    envelope = dict(
        _type_='Envelope',
        body=dict(
            _type_='EnvelopeBody',
            title=record.title,
            description=record.descriptions,
            hashtags=[tag.text for tag in record.tags],
            publisher=record.youtube_video.channel.title,
            photo=record.image.uri,
            audio=record.audio.uri,
        ),
        recipients=recipients,
    )

    task = publisher.send_task('publisher.publish', (envelope,))
    return dict(
        task_id=task.id,
    )
