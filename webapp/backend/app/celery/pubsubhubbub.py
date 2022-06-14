from datetime import timedelta, datetime
from os import environ

import requests
from sqlalchemy import and_

from app.celery import celery


def resubscribe(ctx, time_delta=None):
    with ctx:
        from app.models.source_channels import SourceChannel
        if not time_delta:
            time_delta = timedelta(days=1)

        resubscribe_channels = SourceChannel.query.filter(and_(
            SourceChannel.pubsubhubbub_mode == 'subscribe',
            SourceChannel.pubsubhubbub_expires_at <= datetime.now() + time_delta
        ))

        for channel in resubscribe_channels:
            subscribe.delay(channel.channel_id, channel.pubsubhubbub_mode)


@celery.task()
def subscribe(channel_id: str, mode_subscribe: str = 'subscribe', lease_seconds: int = 1e6):
    """
    Create subscribe request to pubsubhubbub.appspot.com hub
    """
    assert mode_subscribe in ['subscribe', 'unsubscribe']

    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    return requests.post('https://pubsubhubbub.appspot.com/subscribe', headers=headers, data={
        'hub.callback': f'{environ.get("BASE_URL")}/hooks/new/{channel_id}',
        'hub.mode': mode_subscribe,
        'hub.topic': f'https://www.youtube.com/xml/feeds/videos.xml?channel_id={channel_id}',
        'hub.verify': 'sync',
        'hub.lease_seconds': lease_seconds
    })
