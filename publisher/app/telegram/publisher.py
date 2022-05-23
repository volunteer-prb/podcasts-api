import re
import shutil
from urllib.request import urlretrieve
import uuid
from os import environ, makedirs

import cv2

from app import celery, image_utils
from app.objects.Envelope import EnvelopeBody
from app.objects.Recipient import TelegramRecipient
from app.telegram.telegram_bot_api import TelegramBot


@celery.task()
def publish(envelope: EnvelopeBody, recipient: TelegramRecipient):
    """Publish envelope to telegram channel"""

    # create telegram bot instance,
    tb = TelegramBot(environ.get('TELEGRAM_TOKEN', environ.get('TELEGRAM_SERVER')))

    hashtags = ' '.join(['#' + re.sub(r'\s+', '_', hashtag) for hashtag in envelope.hashtags])
    text = f'<strong>{envelope.title}</strong>\n\n' \
           f'{envelope.description}\n\n' \
           f'{hashtags}'

    # split big text description to telegram partial message
    caption = ''
    messages = []
    msg = ''
    for paragraph in text.split('\n'):
        if (len(msg) + len(paragraph)) < (tb.MAX_MESSAGE_LEN if len(messages) > 0 else tb.MAX_PHOTO_LEN):
            msg += '\n' + paragraph
        else:
            messages.append(msg.strip())
            msg = paragraph
    if len(msg) > 0:
        messages.append(msg.strip())

    tmpdir = f'/tmp/{str(uuid.uuid4())}'
    makedirs(tmpdir, exist_ok=True)

    # download photo if url passed, make thumb
    photo = envelope.photo
    if photo is not None:
        if photo.startswith('http'):
            filename = f'{tmpdir}/{str(uuid.uuid4())}'
            urlretrieve(photo, filename)
            photo = filename

        # create thumbnail for audio
        photo = cv2.imread(photo)
        thumb = image_utils.resize_max(photo, tb.MAX_AUDIO_THUMB_SIZE)

        caption = messages[0]
        messages = messages[1:]
    else:
        thumb = None

    audio = envelope.audio
    if audio.startswith('http'):
        filename = f'{tmpdir}/{str(uuid.uuid4())}'
        urlretrieve(audio, filename)
        audio = open(filename, 'rb')
    else:
        audio = open(audio, 'rb')

    # first send photo message
    if photo is not None:
        tb.send_photo(
            chat_id=recipient.channel_id,
            photo=cv2.imencode('.jpg', photo)[1],
            caption=caption,
            parse_mode='html',
        )

    # second send other text (description) message
    for msg in messages:
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
        audio=audio,
        thumb=cv2.imencode('.jpg', thumb)[1] if thumb is not None else None
    )

    shutil.rmtree(tmpdir)
