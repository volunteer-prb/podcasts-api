import re
from os import environ

from celery import Celery

from publisher.objects import Envelope
from publisher.objects.Recipient import TelegramRecipient
from publisher.telegram.telegram_bot_api import TelegramBot

TG_MAX_PHOTO_LEN = 1000
TG_MAX_MESSAGE_LEN = 4000

app = Celery('telegram', broker=environ.get('TELEGRAM_BROKER', 'pyamqp://guest@localhost//'))


@app.task
def publish(envelope: Envelope):
    """Publish envelope to telegram channels"""

    # create telegram bot instance,
    tb = TelegramBot(environ.get('TELEGRAM_TOKEN', environ.get('TELEGRAM_SERVER')))

    hashtags = ' '.join(['#' + re.sub('[\s]+', '_', hashtag) for hashtag in envelope.hashtags])
    text = f'<strong>{envelope.title}</strong>\n\n' \
           f'{envelope.description}\n\n' \
           f'{hashtags}'

    # split big text description to telegram partial message
    messages = []
    msg = ''
    for paragraph in text.split('\n'):
        if (len(msg) + len(paragraph)) < (TG_MAX_MESSAGE_LEN if len(messages) > 0 else TG_MAX_PHOTO_LEN):
            msg += '\n' + paragraph
        else:
            messages.append(msg.strip())
            msg = paragraph
    if len(msg) > 0:
        messages.append(msg.strip())

    # filter recipient list, select only telegram recipients
    for recipient in [rec for rec in envelope.recipients if isinstance(rec, TelegramRecipient)]:
        # first send photo message
        tb.send_photo(
            chat_id=recipient.channel_id,
            photo=envelope.thumb,
            caption=messages[0],
            parse_mode='html',
        )

        # second send other text (description) message
        for msg in messages[1:]:
            tb.send_message(
                chat_id=recipient.channel_id,
                text=msg,
                parse_mode='html',
            )

        # and the last send audio
        tb.send_audio(
            chat_id=recipient.channel_id,
            caption=f'<strong>{envelope.title}</strong>\n\n{hashtags}',
            parse_mode='html',
            performer=envelope.publisher,
            title=envelope.title,
            audio=envelope.audio,  # todo: perform open(envelope.audio, 'rb') when passed file path, not url
            thumb=envelope.thumb   # todo: perform open(envelope.thumb, 'rb') when passed file path, not url
        )
