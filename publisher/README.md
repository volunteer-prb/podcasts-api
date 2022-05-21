# Publisher service

Consumes notification topic from other service, prepare and publish 
messages to selected social media sources.

## Build

```commandline
docker build -t volunteer-prb/podcasts-api-publisher .
```

## Running

Local
```commandline
export TELEGRAM_TOKEN=<put_bot_token_here>
cd src && python main.py
```

In docker 
```commandline
docker run -e TELEGRAM_TOKEN=<put_bot_token_here> \
  -e REDIS_HOST=<redis_host> \
  --name publisher --rm \
  volunteer-prb/podcasts-api-publisher
```

In docker compose (increase maximum audio size to 2GB)
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
      REDIS_HOST: <redis_host>
    depends_on:
      - telegram-bot-api
```

Run with scale factor 3

```commandline
docker-compose up --scale publisher=3
```

## Example 

```python
import json

from redis import Redis


envelope = dict(
    title='Podcasts API Example',
   description='Project for uploading videos from YouTube as audio podcasts to TG and Soundcloud',
   hashtags=['volunteer', 'prb', 'media'],
   publisher='Volunteer PRB',
   photo='https://file-examples.com/storage/feb04797b46286b5ea5f061/2017/10/file_example_JPG_500kB.jpg',
   audio='https://file-examples.com/storage/feb04797b46286b5ea5f061/2017/11/file_example_MP3_700KB.mp3',
   recipients=[
       dict(
           _type_ = 'telegram',
           channel_id=-1000000000000  # replace it by you channel id
       )
   ]
)

r = Redis()
r.publish('notification_topic', json.dumps(envelope))
```