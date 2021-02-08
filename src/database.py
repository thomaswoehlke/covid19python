from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from logging.config import dictConfig


app = Flask('app')
CORS(app)
app.config.from_object("config")
port = app.config['PORT']
ITEMS_PER_PAGE = app.config['ITEMS_PER_PAGE']
DB_URL = 'postgresql+psycopg2://{user}:{pw}@{url}/{db}'.format(
    user=app.config['POSTGRES_USER'],
    pw=app.config['POSTGRES_PW'],
    url=app.config['POSTGRES_URL'],
    db=app.config['POSTGRES_DB'])
app.config['SQLALCHEMY_DATABASE_URI'] = DB_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # silence the deprecation warning
run_run_with_debug = app.config['APP_DEBUGGER_ACTIVE']
db = SQLAlchemy(app)
db.create_all()

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
