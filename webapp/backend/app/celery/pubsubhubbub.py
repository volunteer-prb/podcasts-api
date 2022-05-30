import requests

from app.celery import celery


def resubscribe():
    print('resubscribe')


@celery.task()
def subscribe(channel_id: str, callback_url: str, mode_subscribe: bool = True, lease_seconds: int = 1e6):
    print(channel_id)
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    return requests.post('https://pubsubhubbub.appspot.com/subscribe', headers=headers, data={
        'hub.callback': callback_url,
        'hub.mode': 'subscribe' if mode_subscribe else 'unsubscribe',
        'hub.topic': f'https://www.youtube.com/xml/feeds/videos.xml?channel_id={channel_id}',
        'hub.verify': 'sync',
        'hub.lease_seconds': lease_seconds
    })
