import re
import shutil
import urllib
import uuid
from os import environ, makedirs

import cv2

from app.objects.Envelope import Envelope
from app.objects.Recipient import TelegramRecipient
from app.telegram.telegram_bot_api import TelegramBot

TG_MAX_PHOTO_LEN = 1000
TG_MAX_MESSAGE_LEN = 4000
TG_MAX_AUDIO_THUMB_SIZE = 320


def publish(envelope: Envelope):
    """Publish envelope to telegram channels"""

    # create telegram bot instance,
    tb = TelegramBot(environ.get('TELEGRAM_TOKEN', environ.get('TELEGRAM_SERVER')))

    hashtags = ' '.join(['#' + re.sub('[\s]+', '_', hashtag) for hashtag in envelope.hashtags])
    text = f'<strong>{envelope.title}</strong>\n\n' \
           f'{envelope.description}\n\n' \
           f'{hashtags}'

    # split big text description to telegram partial message
    caption = ''
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

    tmpdir = f'/tmp/{str(uuid.uuid4())}'
    makedirs(tmpdir, exist_ok=True)

    # download thumb if url passed
    photo = envelope.photo
    if photo is not None:
        if photo.startswith('http'):
            filename = f'{tmpdir}/{str(uuid.uuid4())}'
            urllib.request.urlretrieve(photo, filename)
            photo = filename

        # create thumbnail for audio
        photo = cv2.imread(photo)
        h, w = photo.shape[:2]
        maxSize = max(h, w)
        thumb = cv2.resize(photo, (int(w / maxSize * TG_MAX_AUDIO_THUMB_SIZE), int(h / maxSize * TG_MAX_AUDIO_THUMB_SIZE)))

        caption = messages[0]
        messages = messages[1:]
    else:
        thumb = None

    audio = envelope.audio
    if audio.startswith('http'):
        filename = f'{tmpdir}/{str(uuid.uuid4())}'
        urllib.request.urlretrieve(audio, filename)
        audio = filename

    # filter recipient list, select only telegram recipients
    for recipient in [rec for rec in envelope.recipients if isinstance(rec, TelegramRecipient)]:
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
            audio=open(audio, 'rb'),
            thumb=cv2.imencode('.jpg', thumb)[1] if thumb is not None else None
        )

    shutil.rmtree(tmpdir)
