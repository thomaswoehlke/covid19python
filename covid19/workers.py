from database import app
from celery import Celery

############################################################################################
#
# Celery
#
celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)
celery.conf.result_backend = app.config['CELERY_BROKER_URL']
celery.conf.broker_transport_options = {'visibility_timeout': 18000, 'max_retries': 5}
celery.conf.worker_send_task_events = app.config['CELERY_CONF_WORKER_SEND_TASK_EVENTS']
celery.conf.task_send_sent_event = app.config['CELERY_CONF_TASK_SEND_SENT_EVENT']
