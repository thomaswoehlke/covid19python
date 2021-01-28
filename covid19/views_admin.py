from flask import render_template, redirect, url_for, flash
from sqlalchemy.exc import OperationalError
from celery import states
from celery.utils.log import get_task_logger

from database import app
from services import who_service, europe_service, vaccination_service, admin_service, rki_service
from workers import celery

from covid19.oodm.who.who_model import WhoGlobalDataImportTable
from covid19.oodm.who.who_model import WhoRegion, WhoCountry, WhoDateReported, WhoGlobalData
from covid19.oodm.europe.europe_model import EuropeDataImportTable, EuropeDateReported, EuropeContinent
from covid19.oodm.europe.europe_model import EuropeCountry, EuropeData
from covid19.oodm.common.common_model_transient import ApplicationPage
from covid19.oodm.vaccination.vaccination_model import VaccinationGermanyTimeline

drop_and_create_data_again = True


#################################################################################################################
#
# Admin
#
#################################################################################################################


@celery.task(bind=True)
def task_admin_alive_message(self):
    logger = get_task_logger(__name__)
    self.update_state(state=states.STARTED)
    logger.info("------------------------------------------------------------")
    logger.info(" Received: task_admin_alive_message [OK] ")
    logger.info("------------------------------------------------------------")
    self.update_state(state=states.SUCCESS)
    result = "OK (task_admin_alive_message)"
    return result


@celery.task(bind=True)
def task_admin_database_drop_create(self):
    logger = get_task_logger(__name__)
    self.update_state(state=states.STARTED)
    logger.info("------------------------------------------------------------")
    logger.info(" Received: task_admin_database_drop_create [OK] ")
    logger.info("------------------------------------------------------------")
    who_service.run_update_initial()
    europe_service.run_update_initial()
    vaccination_service.run_update_initial()
    admin_service.run_admin_database_dump()
    self.update_state(state=states.SUCCESS)
    result = "OK (task_admin_database_drop_create)"
    return result


@app.route('/admin/tasks')
def url_admin_tasks():
    page_info = ApplicationPage('Admin', "Tasks")
    return render_template(
        'admin/admin_tasks.html',
        page_info=page_info)


@app.route('/admin/info')
def url_admin_info():
    page_info = ApplicationPage('Admin', "Info")
    return render_template(
        'admin/admin_info.html',
        page_info=page_info)


@app.route('/admin/alive_message')
def url_alive_message_start():
    app.logger.info("url_alive_message_start [start]")
    task_admin_alive_message.apply_async()
    flash("alive_message_task started")
    app.logger.info("url_alive_message_start [done]")
    return redirect(url_for('url_admin_tasks'))


@app.route('/admin/database/dump')
def url_admin_database_dump():
    app.logger.info("url_admin_database_dump [start]")
    admin_service.run_admin_database_dump()
    flash("admin_service.run_admin_database_dump started")
    app.logger.info("url_admin_database_dump [done]")
    return redirect(url_for('url_admin_tasks'))


@app.route('/admin/database/import')
def url_admin_database_import():
    app.logger.info("url_admin_database_import [start]")
    admin_service.run_admin_database_import()
    flash("admin_service.run_admin_database_import started")
    app.logger.info("url_admin_database_import [done]")
    return redirect(url_for('url_admin_tasks'))


@app.route('/admin/database/drop')
def url_admin_database_drop():
    app.logger.info("url_admin_database_drop [start]")
    flash("admin_service.run_admin_database_drop started")
    admin_service.run_admin_database_drop()
    if drop_and_create_data_again:
        flash("europe_service.download started")
        europe_service.download()
        flash("who_service.run_download started")
        who_service.run_download()
        flash("vaccination_service.run_download started")
        vaccination_service.run_download()
        flash("rki_service.run_download started")
        rki_service.run_download()
        flash("task_admin_database_drop_create async started")
        task_admin_database_drop_create.apply_async()
    app.logger.info("url_admin_database_drop [done]")
    return redirect(url_for('url_admin_tasks'))
