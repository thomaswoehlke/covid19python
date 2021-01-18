from logging.config import dictConfig
from celery import Celery, states
from database import db, app, my_logging_comfig
from org.woehlke.covid19.who.who_service import WhoService
from org.woehlke.covid19.europe.europe_service import EuropeService

who_service = WhoService(db)
celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)


@celery.task(bind=True)
def who_run_update_task(self, import_file=True):
    self.update_state(state=states.STARTED)
    app.logger.info("------------------------------------------------------------")
    app.logger.info(" Received: who_run_update_task [OK] ")
    app.logger.info("------------------------------------------------------------")
    who_service.run_update(import_file)
    self.update_state(state=states.SUCCESS)
    result = "OK (who_run_update_task)"
    return result


@celery.task(bind=True)
def who_update_short_task(self, import_file=True):
    self.update_state(state=states.STARTED)
    app.logger.info("------------------------------------------------------------")
    app.logger.info(" Received: who_update_short_task [OK] ")
    app.logger.info("------------------------------------------------------------")
    who_service.run_update_short(import_file)
    self.update_state(state=states.SUCCESS)
    result = "OK (who_update_short_task)"
    return result


@celery.task(bind=True)
def alive_message_task(self):
    self.update_state(state=states.STARTED)
    app.logger.info("------------------------------------------------------------")
    app.logger.info(" Received: Alive Message [OK] ")
    app.logger.info("------------------------------------------------------------")
    self.update_state(state=states.SUCCESS)
    result = "OK"
    return result

