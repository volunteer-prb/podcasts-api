from app import celery
from app.objects.Envelope import Envelope
from app.objects.Recipient import TelegramRecipient
from app.telegram import publisher as tg_publisher


@celery.task()
def publish(envelope: Envelope):
    """Publish envelope (topic) to social media by recipients list"""
    # filter recipient list, select only telegram recipients
    for recipient in envelope.recipients:
        if isinstance(recipient, TelegramRecipient):
            tg_publisher.publish.delay(envelope.body, recipient)
