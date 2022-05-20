import json
import time
import traceback
from os import environ

from redis.client import Redis

from objects.Envelope import Envelope
from telegram import publisher


def publish_event(event):
    try:
        if event['type'] == 'message':
            data = json.loads(event['data'])
            envelope = Envelope.from_json(data)
            publisher.publish(envelope)
    except Exception as e:
        traceback.print_exc()
        # todo: handle exception
        pass


if __name__ == '__main__':
    r = Redis(host=environ.get('REDIS_HOST'), port=environ.get('REDIS_PORT', 6379), db=environ.get('REDIS_DB', 0))
    sub = r.pubsub(ignore_subscribe_messages=True)
    sub.subscribe(**{'notification_topic': publish_event})
    thread = sub.run_in_thread(sleep_time=0.3)

    while True:
        try:
            # wait keyboard interrupt
            time.sleep(1)
        except KeyboardInterrupt:
            break

    thread.stop()
    thread.join()
    sub.close()
