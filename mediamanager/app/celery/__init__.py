from celery import Celery

broker_url = 'amqp://guest@localhost:8080//'

celery = Celery('mediamanager', broker=broker_url)
celery.conf.update(
    task_serializer='json',
    # accept_content=['json'],  # Ignore other content
    result_serializer='json',
    timezone='Europe/Paris',
    enable_utc=True,
    result_persistent=True,
    ignore_result=False,
)
