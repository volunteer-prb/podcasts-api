from celery import Celery

celery = Celery('publisher', broker='redis://')
