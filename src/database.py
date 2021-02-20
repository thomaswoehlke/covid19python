from flask import Flask
from flask_cors import CORS
from flask_bs4 import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from logging.config import dictConfig
from flask_admin import Admin
from celery import Celery


def create_app():
    my_app = Flask('covid19')
    CORS(my_app)
    Bootstrap(my_app)
    my_app.config.from_object("config")
    db_url = 'postgresql+psycopg2://{user}:{pw}@{url}/{db}'.format(
        user=my_app.config['SQLALCHEMY_POSTGRES_USER'],
        pw=my_app.config['SQLALCHEMY_POSTGRES_PW'],
        url=my_app.config['SQLALCHEMY_POSTGRES_URL'],
        db=my_app.config['SQLALCHEMY_POSTGRES_DB'])
    my_app.config['SQLALCHEMY_DATABASE_URI'] = db_url
    my_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # silence the deprecation warning
    my_app.config['FLASK_ADMIN_SWATCH'] = 'superhero'
    return my_app


def create_db(my_app):
    my_db = SQLAlchemy(my_app)
    my_db.create_all()
    return my_db


def create_db_test(my_app):
    my_db = SQLAlchemy(my_app)
    my_db.create_all()
    return my_db


def create_celery(my_app):
    celery = Celery(
        my_app.import_name,
        backend=my_app.config['MY_CELERY_RESULT_BACKEND'],
        broker=my_app.config['CELERY_BROKER_URL'],
        worker_send_task_events=my_app.config['CELERY_CONF_WORKER_SEND_TASK_EVENTS'],
        task_send_sent_event=my_app.config['CELERY_CONF_TASK_SEND_SENT_EVENT'],
        broker_transport_options={'visibility_timeout': 18000, 'max_retries': 5}
    )
    celery.conf.update(my_app.config)

    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with my_app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask
    return celery


def create_admin(my_app):
    my_admin = Admin(
        my_app,
        name='covid19 | admin',
        template_mode='bootstrap4')
    return my_admin


app = create_app()
db = create_db(app)
admin = create_admin(app)

# TODO: deprecated
port = app.config['PORT']
# TODO: deprecated
run_run_with_debug = app.config['FLASK_APP_DEBUGGER_ACTIVE']
# TODO: deprecated
ITEMS_PER_PAGE = app.config['SQLALCHEMY_ITEMS_PER_PAGE']

my_logging_config = {
        'version': 1,
        'formatters': {'default': {
            'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
        }},
        'handlers': {'wsgi': {
            'class': 'logging.StreamHandler',
            'stream': 'ext://flask.logging.wsgi_errors_stream',
            'formatter': 'default'
        }},
        'root': {
            'level': 'INFO',
            'handlers': ['wsgi']
        }
    }
dictConfig(my_logging_config)
