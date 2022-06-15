# Publisher service

Consumes notification topic from other service, prepare and publish messages to selected social media sources.

## Build

```commandline
docker build -t volunteer-prb/podcasts-api-publisher .
```

## Running

#### Local
```commandline
export TELEGRAM_TOKEN=<put_bot_token_here>
celery --app=app.publisher --broker=redis://localhost worker --loglevel=INFO -Q publisher_tasks
```

#### In docker 
```commandline
docker run -e TELEGRAM_TOKEN=<put_bot_token_here> \
  -e BROKER_URL=<redis_host> \
  --name publisher --rm \
  volunteer-prb/podcasts-api-publisher
```

#### In docker compose (increase maximum audio size to 2GB)
```yaml
version: '3.8'
services:
  telegram-bot-api:
    image: aiogram/telegram-bot-api:latest
    environment:
      TELEGRAM_API_ID: <put_telegram_api_id>
      TELEGRAM_API_HASH: <put_telegram_api_hash>
    volumes:
      - ./telegram-bot-api-data:/var/lib/telegram-bot-api

  publisher:
    image: volunteer-prb/podcasts-api-publisher:latest
    environment:
      TELEGRAM_SERVER: http://telegram-bot-api:8081
      TELEGRAM_TOKEN: <put_bot_token_here>
      BROKER_URL: redis://<redis_host>
    depends_on:
      - telegram-bot-api
```

Run with scale factor 3

```commandline
docker-compose up --scale publisher=3
```

## Examples

#### With objects class
```python
from app.objects.Envelope import EnvelopeBody, Envelope
from app.objects.Recipient import TelegramRecipient
from app.publisher import publish


envelope = Envelope(
    body=EnvelopeBody(
        title='Podcasts API Example',
        description='Project for uploading videos from YouTube as audio podcasts to TG and Soundcloud',
        hashtags=['volunteer', 'prb', 'media'],
        publisher='Volunteer PRB',
        photo='https://transfer.sh/get/shqEBi/photo.jpg',
        audio='https://transfer.sh/get/vYyWP8/audio.mp3',
    ),
    recipients=[
        TelegramRecipient(
            channel_id=-1000000000000  # replace it by you channel id
        )
    ]
)

publish.delay(envelope)
```

#### With raw dict
```python
from app.publisher import publish


envelope = dict(
    _type_='Envelope',
    body=dict(
        _type_='EnvelopeBody',
        title='Podcasts API Example',
        description='Project for uploading videos from YouTube as audio podcasts to TG and Soundcloud',
        hashtags=['volunteer', 'prb', 'media'],
        publisher='Volunteer PRB',
        photo='https://transfer.sh/get/shqEBi/photo.jpg',
        audio='https://transfer.sh/get/vYyWP8/audio.mp3',
    ),
    recipients=[
        dict(
            _type_='TelegramRecipient',
            channel_id=-1000000000000  # replace it by you channel id
        )
    ]
)

publish.delay(envelope)
```
