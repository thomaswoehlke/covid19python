from logging.config import dictConfig
from celery import Celery, states
from database import db, app, my_logging_config
from org.woehlke.covid19.who.who_service import WhoService, who_service
from org.woehlke.covid19.europe.europe_service import EuropeService, europe_service
from server_mq import celery, who_run_update_task


if __name__ == '__main__':
    dictConfig(my_logging_config)
    db.create_all()
    who_service = WhoService(db)
    europe_service = EuropeService(db)
    app.run(port=9090, debug=True)
