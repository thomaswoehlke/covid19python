SECRET_KEY = 'vfdjv423ndf654&%%'
CELERY_BROKER_URL = 'redis://localhost:6379/1'
MY_CELERY_RESULT_BACKEND = 'redis://localhost:6379/1'
CELERY_CONF_WORKER_SEND_TASK_EVENTS = True
CELERY_CONF_TASK_SEND_SENT_EVENT = True
SQLALCHEMY_POSTGRES_USER = 'covid19data'
SQLALCHEMY_POSTGRES_PW = 'covid19datapwd'
SQLALCHEMY_POSTGRES_URL = 'localhost'
SQLALCHEMY_POSTGRES_DB = 'covid19datatest'
SQLALCHEMY_ITEMS_PER_PAGE = 10
SQLALCHEMY_TRACK_MODIFICATIONS = True
FLASK_ADMIN_SWATCH = 'superhero'
FLASK_APP_DEBUGGER_ACTIVE = True
PORT = 7070
