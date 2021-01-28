from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from datetime import date

app = Flask('app')
CORS(app)
app.config.from_object("config")
ITEMS_PER_PAGE = app.config['ITEMS_PER_PAGE']
DB_URL = 'postgresql+psycopg2://{user}:{pw}@{url}/{db}'.format(
    user=app.config['POSTGRES_USER'],
    pw=app.config['POSTGRES_PW'],
    url=app.config['POSTGRES_URL'],
    db=app.config['POSTGRES_DB'])
app.config['SQLALCHEMY_DATABASE_URI'] = DB_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # silence the deprecation warning
db = SQLAlchemy(app)
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
run_run_with_debug = app.config['APP_DEBUGGER_ACTIVE']


def transform_datum_europe(my_date):
    my_date_reported = my_date.split('/')
    my_year = int(my_date_reported[2])
    my_month = int(my_date_reported[1])
    my_day = int(my_date_reported[0])
    my_datum = date(year=my_year, month=my_month, day=my_day)
    return my_datum


def transform_datum(my_date_reported):
    my_date_reported = my_date_reported.split("-")
    my_year = int(my_date_reported[0])
    my_month = int(my_date_reported[1])
    my_day = int(my_date_reported[2])
    my_datum = date(my_year, my_month, my_day)
    return my_datum
