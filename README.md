# podcasts-api

## General

Project for uploading videos from YouTube as audio podcasts to TG and Soundcloud

[Detailed base architecture](Conversion%20Service.md)

## Subscribe for updates on a channel

Please follow instructions at [official YouTube data API page](https://developers.google.com/youtube/v3/guides/push_notifications). 
WebApp expects notifications on `/hooks/new/<channel_id>` endpoint.

## First run

Build applications with followed instructions: 
[backend](webapp/backend/README.md); 
[media manager](mediamanager/README.md);
[publisher](publisher/README.md).

Open docker-compose.yml and edit missing properties, then

```commandline
docker-compose up -d postgres telegram-bot-api redis

docker-compose run backend flask db init

docker-compose run backend flask db migrate -m 'initial database'

docker-compose run backend flask db upgrade

docker-compose up -d backend media_manager publisher backend_worker
```

## Examples of usage

### Register new Source Channel

```commandline
curl --location --request POST 'http://localhost:1235/channels/' \
--header 'Content-Type: application/json' \
--data-raw '{
    "channel_id": "UC7Elc-kLydl-NAV4g204pDQ",
    "title": "Popular politic",
    "pubsubhubbub_mode": "subscribe"
}'
```

Given response:

```json
{
    "status": "success",
    "data": {
        "channel_id": "UC7Elc-kLydl-NAV4g204pDQ",
        "created": 1655238791.048011,
        "id": 1,
        "pubsubhubbub_expires_at": 1655238791.048026,
        "pubsubhubbub_mode": "subscribe",
        "title": "Popular politic",
        "updated": 1655238791.048021,
        "uri": null
    }
}
```

### Register new Output Service

Register new Output Service (e.g. Telegram channel) and associate it with Source Channel #1.

```commandline
curl --location --request POST 'http://localhost:1235/outputs/?include_sources' \
--header 'Content-Type: application/json' \
--data-raw '{
    "title": "Popular politic",
    "type": "telegram",
    "channel_id": -1000000000000,
    "sources": [1]
}'
```

Given response:

```json
{
    "status": "success",
    "data": {
        "channel_id": -1000000000000,
        "created": 1655242254.858093,
        "id": 1,
        "sources": [
            {
                "id": 1,
                "output_service_id": 1,
                "source_channel_id": 1
            }
        ],
        "title": "Popular politic",
        "type": "telegram",
        "updated": 1655242254.858098
    }
}
```

### Emulate new video event

Backend service will receive new video event from Google PubSubHubbub Hub, 
you can check work with manual request new video event, e.g.:

```commandline
curl --location --request POST 'http://localhost:1235/hooks/new/UC7Elc-kLydl-NAV4g204pDQ' \
--header 'Content-Type: application/xml' \
--data-raw '<feed xmlns:yt="http://www.youtube.com/xml/schemas/2015" xmlns="http://www.w3.org/2005/Atom">
    <link rel="hub" href="https://pubsubhubbub.appspot.com"/>
    <link rel="self" href="https://www.youtube.com/xml/feeds/videos.xml?channel_id=CHANNEL_ID"/>
    <title>YouTube video feed</title>
    <updated>2015-04-01T19:05:24.552394234+00:00</updated>
    <entry>
    <id>yt:video:KBOny-tYdNQ</id>
    <yt:videoId>KBOny-tYdNQ</yt:videoId>
    <yt:channelId>UC7Elc-kLydl-NAV4g204pDQ</yt:channelId>
    <title>Ходорковский о конце Путина</title>
    <link rel="alternate" href="https://www.youtube.com/watch?v=KBOny-tYdNQ"/>
    <author>
        <name>Популярная политика</name>
        <uri>https://www.youtube.com/channel/UC7Elc-kLydl-NAV4g204pDQ</uri>
    </author>
    <published>2022-06-11T20:32:12.687871+00:00</published>
    <updated>2022-06-11T20:32:12.687876+00:00</updated>
    </entry>
</feed>'
```

Given response:

```json
{
    "status": "success",
    "data": {
        "channel_id": 1,
        "created": 1655241792.879899,
        "id": 1,
        "title": "Ходорковский о конце Путина",
        "updated": 1655241792.879905,
        "uri": "https://www.youtube.com/watch?v=KBOny-tYdNQ",
        "yt_id": "KBOny-tYdNQ",
        "yt_published": 1654979532.687871,
        "yt_updated": 1654979532.687876
    }
}
```

### Publish new Record to Output Services (e.g. Telegram)

After new video event will be received, _media manager_ will download it and create new Record in database, 
after you can manually publish this Record to Output Services, associated with Source Channel. 

```commandline
curl --location --request PUT 'http://localhost:1235/records/publish/1'
```

Given response:

```json
{
    "status": "success",
    "data": {
        "task_id": "995440b5-257f-4545-871b-85b48d9137e8"
    }
}
```