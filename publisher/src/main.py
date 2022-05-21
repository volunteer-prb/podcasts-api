import json
import time
import traceback
from os import environ

from redis.client import Redis

from objects.Envelope import Envelope
from telegram import publisher


def publish_event(data):
    """Publish envelope (topic) to social media by recipients list"""
    try:
        envelope = Envelope.from_json(data)
        publisher.publish(envelope)
    except Exception as e:
        traceback.print_exc()
        # todo: handle exception
        pass


def get_notification_data(r):
    """Get notification id from list, extract data by id"""
    data = r.lpop('notification_topic_list')
    if data is not None:
        data = r.get(f'notification_topic_{data.decode("utf-8")}')
    return data


if __name__ == '__main__':
    r = Redis(host=environ.get('REDIS_HOST'), port=environ.get('REDIS_PORT', 6379), db=environ.get('REDIS_DB', 0))

    while True:
        try:
            data = get_notification_data(r)
            if data is not None:
                publish_event(json.loads(data))
            time.sleep(0.1)
        except KeyboardInterrupt:
            break
