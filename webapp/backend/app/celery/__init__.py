from celery import Celery

celery = Celery('backend', broker='redis://')
media_manager = Celery('media_manager', broker='redis://')
