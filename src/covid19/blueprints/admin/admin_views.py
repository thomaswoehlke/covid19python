from flask import render_template, redirect, url_for, flash, Blueprint
from celery import states
from celery.utils.log import get_task_logger
from flask_admin.contrib.sqla import ModelView

from database import app, admin, db
from covid19.blueprints.application.application_services import who_service, ecdc_service, rki_vaccination_service
from covid19.blueprints.application.application_services import rki_service_bundeslaender, rki_service_landkreise
from covid19.blueprints.application.application_services import admin_service, owid_service
from covid19.blueprints.application.application_workers import celery
from covid19.blueprints.application.application_model_transient import ApplicationPage

drop_and_create_data_again = True

app_admin = Blueprint('app_admin', __name__, template_folder='templates', url_prefix='/admin')


# ---------------------------------------------------------------------------------------------------------------
#  Url Routes Frontend
# ---------------------------------------------------------------------------------------------------------------

@app_admin.route('/')
def url_admin_index():
    page_info = ApplicationPage('Admin', "Covid19 Admin")
    return render_template(
        'admin/index.html',
        page_info=page_info)


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


# ----------------------------------------------------------------------------------------------------------------
#  Celery TASKS
# ----------------------------------------------------------------------------------------------------------------


@celery.task(bind=True)
def task_admin_alive_message(self):
    logger = get_task_logger(__name__)
    self.update_state(state=states.STARTED)
    logger.info("------------------------------------------------------------")
    logger.info(" task_admin_alive_message [received] ")
    logger.info("------------------------------------------------------------")
    self.update_state(state=states.SUCCESS)
    result = "OK (task_admin_alive_message)"
    return result


@celery.task(bind=True)
def task_admin_database_drop_create(self):
    logger = get_task_logger(__name__)
    self.update_state(state=states.STARTED)
    logger.info("------------------------------------------------------------")
    logger.info(" task_admin_database_drop_create [start] ")
    logger.info("------------------------------------------------------------")
    who_service.task_database_drop_create()
    ecdc_service.task_database_drop_create()
    owid_service.task_database_drop_create()
    rki_vaccination_service.task_database_drop_create()
    admin_service.task_database_drop_create()
    logger.info("------------------------------------------------------------")
    logger.info(" task_admin_database_drop_create [done] ")
    logger.info("------------------------------------------------------------")
    self.update_state(state=states.SUCCESS)
    result = "OK (task_admin_database_drop_create)"
    return result


@celery.task(bind=True)
def task_admin_import_all_files(self):
    logger = get_task_logger(__name__)
    self.update_state(state=states.STARTED)
    logger.info("------------------------------------------------------------")
    logger.info(" task_admin_import_all_files [start] ")
    logger.info("------------------------------------------------------------")
    who_service.task_import_all_files()
    ecdc_service.task_import_all_files()
    owid_service.task_import_all_files()
    rki_vaccination_service.task_import_all_files()
    rki_service_bundeslaender.task_import_all_files()
    rki_service_landkreise.task_import_all_files()
    logger.info("------------------------------------------------------------")
    logger.info(" task_admin_import_all_files [done] ")
    logger.info("------------------------------------------------------------")
    self.update_state(state=states.SUCCESS)
    result = "OK (task_admin_import_all_files)"
    return result


@celery.task(bind=True)
def task_admin_update_dimension_tables_only(self):
    logger = get_task_logger(__name__)
    self.update_state(state=states.STARTED)
    logger.info("------------------------------------------------------------")
    logger.info(" task_admin_update_dimension_tables_only [start] ")
    logger.info("------------------------------------------------------------")
    who_service.update_dimension_tables_only()
    ecdc_service.update_dimension_tables_only()
    owid_service.update_dimension_tables_only()
    rki_vaccination_service.update_dimension_tables_only()
    rki_service_bundeslaender.update_dimension_tables_only()
    rki_service_landkreise.update_dimension_tables_only()
    logger.info("------------------------------------------------------------")
    logger.info(" task_admin_update_dimension_tables_only [done] ")
    logger.info("------------------------------------------------------------")
    self.update_state(state=states.SUCCESS)
    result = "OK (task_admin_update_dimension_tables_only)"
    return result


@celery.task(bind=True)
def task_admin_update_fact_table_initial_only(self):
    logger = get_task_logger(__name__)
    self.update_state(state=states.STARTED)
    logger.info("------------------------------------------------------------")
    logger.info(" task_admin_update_fact_table_initial_only [start] ")
    logger.info("------------------------------------------------------------")
    who_service.update_fact_table_initial_only()
    ecdc_service.update_fact_table_initial_only()
    owid_service.update_fact_table_initial_only()
    rki_vaccination_service.update_fact_table_initial_only()
    rki_service_bundeslaender.update_fact_table_initial_only()
    rki_service_landkreise.update_fact_table_initial_only()
    logger.info("------------------------------------------------------------")
    logger.info(" task_admin_update_fact_table_initial_only [done] ")
    logger.info("------------------------------------------------------------")
    self.update_state(state=states.SUCCESS)
    result = "OK (task_admin_update_fact_table_initial_only)"
    return result


@celery.task(bind=True)
def task_admin_update_fact_table_incremental_only(self):
    logger = get_task_logger(__name__)
    self.update_state(state=states.STARTED)
    logger.info("------------------------------------------------------------")
    logger.info(" task_admin_update_fact_table_incremental_only [start] ")
    logger.info("------------------------------------------------------------")
    who_service.update_fact_table_incremental_only()
    ecdc_service.update_fact_table_incremental_only()
    owid_service.update_fact_table_incremental_only()
    rki_vaccination_service.update_fact_table_incremental_only()
    rki_service_bundeslaender.update_fact_table_incremental_only()
    rki_service_landkreise.update_fact_table_incremental_only()
    logger.info("------------------------------------------------------------")
    logger.info(" task_admin_update_fact_table_incremental_only [done] ")
    logger.info("------------------------------------------------------------")
    self.update_state(state=states.SUCCESS)
    result = "OK (task_admin_update_fact_table_incremental_only)"
    return result


@celery.task(bind=True)
def task_admin_update_star_schema_initial(self):
    logger = get_task_logger(__name__)
    self.update_state(state=states.STARTED)
    logger.info("------------------------------------------------------------")
    logger.info(" task_admin_update_star_schema_initial [start] ")
    logger.info("------------------------------------------------------------")
    who_service.run_update_star_schema_initial()
    ecdc_service.run_update_star_schema_initial()
    owid_service.run_update_star_schema_initial()
    rki_vaccination_service.run_update_star_schema_initial()
    rki_service_bundeslaender.run_update_star_schema_initial()
    rki_service_landkreise.run_update_star_schema_initial()
    logger.info("------------------------------------------------------------")
    logger.info(" task_admin_update_star_schema_initial [done] ")
    logger.info("------------------------------------------------------------")
    self.update_state(state=states.SUCCESS)
    result = "OK (task_admin_update_star_schema_initial)"
    return result


@celery.task(bind=True)
def task_admin_update_star_schema_incremental(self):
    logger = get_task_logger(__name__)
    self.update_state(state=states.STARTED)
    logger.info("------------------------------------------------------------")
    logger.info(" task_admin_update_star_schema_incremental [start] ")
    logger.info("------------------------------------------------------------")
    who_service.run_update_star_schema_incremental()
    ecdc_service.run_update_star_schema_incremental()
    owid_service.run_update_star_schema_incremental()
    rki_vaccination_service.run_update_star_schema_incremental()
    rki_service_bundeslaender.run_update_star_schema_incremental()
    rki_service_landkreise.run_update_star_schema_incremental()
    logger.info("------------------------------------------------------------")
    logger.info(" task_admin_update_star_schema_incremental [done] ")
    logger.info("------------------------------------------------------------")
    self.update_state(state=states.SUCCESS)
    result = "OK (task_admin_update_star_schema_incremental)"
    return result

# ----------------------------------------------------------------------------------------------------------------
#  URL Routes for Celery TASKS
# ----------------------------------------------------------------------------------------------------------------


@app_admin.route('/alive_message')
def url_alive_message_start():
    app.logger.info("url_alive_message_start [start]")
    task_admin_alive_message.apply_async()
    flash("alive_message_task started")
    app.logger.info("url_alive_message_start [done]")
    return redirect(url_for('app_admin.url_admin_tasks'))


@app_admin.route('/database/dump')
def url_admin_database_dump():
    app.logger.info("url_admin_database_dump [start]")
    admin_service.run_admin_database_dump()
    flash("admin_service.run_admin_database_dump started")
    app.logger.info("url_admin_database_dump [done]")
    return redirect(url_for('app_admin.url_admin_tasks'))


@app_admin.route('/database/reimport')
def url_admin_database_dump_reimport():
    app.logger.info("url_admin_database_dump_reimport [start]")
    admin_service.run_admin_database_dump_reimport()
    flash("admin_service.run_admin_database_import started")
    app.logger.info("url_admin_database_dump_reimport [done]")
    return redirect(url_for('app_admin.url_admin_tasks'))


@app_admin.route('/database/dropcreate/only')
def url_admin_database_dropcreate_only():
    app.logger.info("url_admin_database_drop [start]")
    flash("admin_service.run_admin_database_drop started")
    admin_service.run_admin_database_drop()
    app.logger.info("url_admin_database_drop [done]")
    return redirect(url_for('app_admin.url_admin_tasks'))


@app_admin.route('/database/drop')
def url_admin_database_drop():
    app.logger.info("url_admin_database_drop [start]")
    admin_service.run_admin_database_drop()
    if drop_and_create_data_again:
        who_service.pretask_database_drop_create()
        ecdc_service.pretask_database_drop_create()
        owid_service.pretask_database_drop_create()
        rki_vaccination_service.pretask_database_drop_create()
        rki_service_bundeslaender.pretask_database_drop_create()
        flash("task_admin_database_drop_create async started")
        task_admin_database_drop_create.apply_async()
    app.logger.info("url_admin_database_drop [done]")
    return redirect(url_for('app_admin.url_admin_tasks'))


@app_admin.route('/download/all')
def url_admin_download_all_files():
    who_service.download_all_files()
    ecdc_service.download_all_files()
    owid_service.pretask_database_drop_create()
    rki_vaccination_service.download_all_files()
    rki_service_bundeslaender.download_all_files()
    rki_service_landkreise.download_all_files()
    app.logger.info("url_admin_download_all_files [done]")
    return redirect(url_for('app_admin.url_admin_tasks'))


@app_admin.route('/import/all')
def url_admin_import_all_files():
    app.logger.info("url_admin_import_all_files [start]")
    task_admin_import_all_files.apply_async()
    flash("task_admin_import_all_files async started")
    app.logger.info("task_admin_import_all_files async started")
    app.logger.info("url_admin_import_all_files [done]")
    return redirect(url_for('app_admin.url_admin_tasks'))


@app_admin.route('/update/dimension_tables/all')
def url_admin_update_dimension_tables_only():
    app.logger.info("url_admin_update_all_groups [start]")
    task_admin_update_dimension_tables_only.apply_async()
    flash("task_admin_import_all_files async started")
    app.logger.info("task_admin_update_all_blueprints async started")
    app.logger.info("url_admin_update_all_groups [done]")
    return redirect(url_for('app_admin.url_admin_tasks'))


@app_admin.route('/update/fact_tables/initial/all')
def url_admin_update_fact_table_initial_only():
    app.logger.info("url_admin_update_fact_table_initial_only [start]")
    task_admin_update_fact_table_initial_only.apply_async()
    flash("task_admin_update_fact_table_initial_only async started")
    app.logger.info("task_admin_update_fact_table_initial_only async started")
    app.logger.info("url_admin_update_fact_table_initial_only [done]")
    return redirect(url_for('app_admin.url_admin_tasks'))


@app_admin.route('/update/fact_tables/incremental/all')
def url_admin_update_fact_table_incremental_only():
    app.logger.info("url_admin_update_fact_table_incremental_only [start]")
    task_admin_update_fact_table_incremental_only.apply_async()
    flash("task_admin_update_fact_table_incremental_only async started")
    app.logger.info("task_admin_update_fact_table_incremental_only async started")
    app.logger.info("url_admin_update_fact_table_incremental_only [done]")
    return redirect(url_for('app_admin.url_admin_tasks'))


@app_admin.route('/update/star_schema/initial/all')
def url_admin_update_star_schema_initial():
    app.logger.info("url_admin_update_star_schema_initial [start]")
    task_admin_update_star_schema_initial.apply_async()
    flash("task_admin_update_fact_table_incremental_only async started")
    app.logger.info("task_admin_update_fact_table_incremental_only async started")
    app.logger.info("url_admin_update_star_schema_initial [done]")
    return redirect(url_for('app_admin.url_admin_tasks'))


@app_admin.route('/update/star_schema/incremental/all')
def run_update_star_schema_incremental():
    app.logger.info("run_update_star_schema_incremental [start]")
    task_admin_update_star_schema_incremental.apply_async()
    flash("task_admin_update_fact_table_incremental_only async started")
    app.logger.info("task_admin_update_fact_table_incremental_only async started")
    app.logger.info("run_update_star_schema_incremental [done]")
    return redirect(url_for('app_admin.url_admin_tasks'))
