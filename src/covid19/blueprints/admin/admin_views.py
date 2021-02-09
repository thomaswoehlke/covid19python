from flask import render_template, redirect, url_for, flash, Blueprint
from celery import states
from celery.utils.log import get_task_logger

from database import app
from covid19.services import who_service, europe_service, vaccination_service, admin_service, rki_service_bundeslaender
from covid19.workers import celery

from covid19.blueprints.common.common_model_transient import ApplicationPage


drop_and_create_data_again = True


app_admin = Blueprint('admin', __name__, template_folder='templates')


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
    who_service.task_database_drop_create()
    europe_service.task_database_drop_create()
    vaccination_service.task_database_drop_create()
    admin_service.task_database_drop_create()
    self.update_state(state=states.SUCCESS)
    result = "OK (task_admin_database_drop_create)"
    return result


@app_admin.route('/tasks')
def url_admin_tasks():
    page_info = ApplicationPage('Admin', "Tasks")
    return render_template(
        'admin/admin_tasks.html',
        page_info=page_info)


@app_admin.route('/info')
def url_admin_info():
    page_info = ApplicationPage('Admin', "Info")
    return render_template(
        'admin/admin_info.html',
        page_info=page_info)


@app_admin.route('/alive_message')
def url_alive_message_start():
    app.logger.info("url_alive_message_start [start]")
    task_admin_alive_message.apply_async()
    flash("alive_message_task started")
    app.logger.info("url_alive_message_start [done]")
    return redirect(url_for('admin.url_admin_tasks'))


@app_admin.route('/database/dump')
def url_admin_database_dump():
    app.logger.info("url_admin_database_dump [start]")
    admin_service.run_admin_database_dump()
    flash("admin_service.run_admin_database_dump started")
    app.logger.info("url_admin_database_dump [done]")
    return redirect(url_for('admin.url_admin_tasks'))


@app_admin.route('/database/import')
def url_admin_database_import():
    app.logger.info("url_admin_database_import [start]")
    admin_service.run_admin_database_import()
    flash("admin_service.run_admin_database_import started")
    app.logger.info("url_admin_database_import [done]")
    return redirect(url_for('admin.url_admin_tasks'))

@app_admin.route('/database/dropcreate/only')
def url_admin_database_dropcreate_only():
    app.logger.info("url_admin_database_drop [start]")
    flash("admin_service.run_admin_database_drop started")
    admin_service.run_admin_database_drop()
    app.logger.info("url_admin_database_drop [done]")
    return redirect(url_for('admin.url_admin_tasks'))

@app_admin.route('/database/drop')
def url_admin_database_drop():
    app.logger.info("url_admin_database_drop [start]")
    flash("admin_service.run_admin_database_drop started")
    admin_service.run_admin_database_drop()
    if drop_and_create_data_again:
        who_service.pretask_database_drop_create()
        europe_service.pretask_database_drop_create()
        vaccination_service.pretask_database_drop_create()
        rki_service_bundeslaender.pretask_database_drop_create()
        flash("task_admin_database_drop_create async started")
        task_admin_database_drop_create.apply_async()
    app.logger.info("url_admin_database_drop [done]")
    return redirect(url_for('admin.url_admin_tasks'))
