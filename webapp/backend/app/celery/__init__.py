from celery import Celery

celery = Celery('backend', broker='redis://')
celery.conf.task_routes = {
    '*': {'queue': 'celery_backend_tasks'},
}

# May be helpful to use separate Celery in separate brokers (for security reason)
media_manager = Celery('media_manager', broker='redis://')
media_manager.conf.task_routes = {
    '*': {'queue': 'media_manager_tasks'},
}

publisher = Celery('publisher', broker='redis://')
publisher.conf.task_routes = {
    '*': {'queue': 'publisher_tasks'},
}
