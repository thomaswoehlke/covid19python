from logging.config import dictConfig
from celery.utils.log import get_task_logger
from celery import Celery, states
from database import db, app, my_logging_config
from org.woehlke.covid19.who.who_service import WhoService
from org.woehlke.covid19.europe.europe_service import EuropeService
from org.woehlke.covid19.vaccination.vaccination_service import VaccinationService
from org.woehlke.covid19.admin.admin_service import AdminService

logger = get_task_logger(__name__)
who_service = WhoService(db)
europe_service = EuropeService(db)
vaccination_service = VaccinationService(db)
admin_service = AdminService(db)
celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)
celery.conf.result_backend = app.config['CELERY_BROKER_URL']
celery.conf.broker_transport_options = {'visibility_timeout': 18000, 'max_retries': 5}
celery.conf.worker_send_task_events = True
celery.conf.task_send_sent_event = True


@celery.task(bind=True)
def who_run_update_task(self, import_file=True):
    self.update_state(state=states.STARTED)
    logger.info("------------------------------------------------------------")
    logger.info(" Received: who_run_update_task [OK] ")
    logger.info("------------------------------------------------------------")
    who_service.run_update(import_file)
    self.update_state(state=states.SUCCESS)
    result = "OK (who_run_update_task)"
    return result


@celery.task(bind=True)
def who_update_short_task(self):
    self.update_state(state=states.STARTED)
    logger.info("------------------------------------------------------------")
    logger.info(" Received: who_update_short_task [OK] ")
    logger.info("------------------------------------------------------------")
    who_service.run_update_short()
    self.update_state(state=states.SUCCESS)
    result = "OK (who_update_short_task)"
    return result


@celery.task(bind=True)
def who_update_initial_task(self):
    self.update_state(state=states.STARTED)
    logger.info("------------------------------------------------------------")
    logger.info(" Received: who_update_initial_task [OK] ")
    logger.info("------------------------------------------------------------")
    who_service.run_update_initial()
    self.update_state(state=states.SUCCESS)
    result = "OK (who_update_initial_task)"
    return result


@celery.task(bind=True)
def alive_message_task(self):
    self.update_state(state=states.STARTED)
    logger.info("------------------------------------------------------------")
    logger.info(" Received: Alive Message [OK] ")
    logger.info("------------------------------------------------------------")
    self.update_state(state=states.SUCCESS)
    result = "OK"
    return result


@celery.task(bind=True)
def europe_update_initial_task(self):
    self.update_state(state=states.STARTED)
    logger.info("------------------------------------------------------------")
    logger.info(" Received: europe_update_task [OK] ")
    logger.info("------------------------------------------------------------")
    europe_service.run_update_initial()
    self.update_state(state=states.SUCCESS)
    result = "OK (europe_update_task)"
    return result


@celery.task(bind=True)
def vaccination_update_initial_task(self):
    self.update_state(state=states.STARTED)
    logger.info("------------------------------------------------------------")
    logger.info(" Received: vaccination_update_initial_task [OK] ")
    logger.info("------------------------------------------------------------")
    vaccination_service.run_update_initial()
    self.update_state(state=states.SUCCESS)
    result = "OK (vaccination_update_initial_task)"
    return result


@celery.task(bind=True)
def admin_database_drop_create_task(self):
    self.update_state(state=states.STARTED)
    logger.info("------------------------------------------------------------")
    logger.info(" Received: admin_database_drop_create_task [OK] ")
    logger.info("------------------------------------------------------------")
    who_service.run_update_initial()
    europe_service.run_update_initial()
    vaccination_service.run_update_initial()
    admin_service.run_admin_database_dump()
    self.update_state(state=states.SUCCESS)
    result = "OK (admin_database_drop_create_task)"
    return result



