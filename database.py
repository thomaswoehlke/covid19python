from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
CORS(app)
app.config.from_object("config")
ITEMS_PER_PAGE = 10
DB_URL = 'postgresql+psycopg2://{user}:{pw}@{url}/{db}'.format(
    user=app.config['POSTGRES_USER'],
    pw=app.config['POSTGRES_PW'],
    url=app.config['POSTGRES_URL'],
    db=app.config['POSTGRES_DB'])
app.config['SQLALCHEMY_DATABASE_URI'] = DB_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # silence the deprecation warning
db = SQLAlchemy(app)

my_logging_comfig = {
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
