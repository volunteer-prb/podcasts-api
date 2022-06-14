from os import environ

from celery import Celery

celery = Celery('backend', broker=environ.get('CELERY_BROKER_URL', 'redis://'))
celery.conf.task_routes = {
    '*': {'queue': 'celery_backend_tasks'},
}

# May be helpful to use separate Celery in separate brokers (for security reason)
media_manager = Celery('media_manager', broker=environ.get('MEDIA_MANAGER_BROKER_URL', 'redis://'))
media_manager.conf.task_routes = {
    '*': {'queue': 'media_manager_tasks'},
}

publisher = Celery('publisher', broker=environ.get('PUBLISHER_BROKER_URL', 'redis://'))
publisher.conf.task_routes = {
    '*': {'queue': 'publisher_tasks'},
}
