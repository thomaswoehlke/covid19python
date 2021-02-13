from flask import render_template, redirect, url_for, flash, Blueprint
from celery import states
from celery.utils.log import get_task_logger

from database import app
from covid19.blueprints.common.application_services import rki_vaccination_service
from covid19.blueprints.common.application_workers import celery

from covid19.blueprints.rki_vaccination.rki_vaccination_model import RkiVaccinationData, RkiVaccinationDateReported
from covid19.blueprints.rki_vaccination.rki_vaccination_model_import import RkiVaccinationImport
from covid19.blueprints.common.application_model_transient import ApplicationPage


app_rki_vaccination = Blueprint('rki_vaccination', __name__, template_folder='templates', url_prefix='/rki/vaccination')


##################################################################################################################
#
# Vaccination
#
##################################################################################################################


@celery.task(bind=True)
def task_vaccination_download_only(self):
    logger = get_task_logger(__name__)
    self.update_state(state=states.STARTED)
    logger.info("------------------------------------------------------------")
    logger.info(" Received: task_europe_download_only [OK] ")
    logger.info("------------------------------------------------------------")
    rki_vaccination_service.run_download_only()
    self.update_state(state=states.SUCCESS)
    result = "OK (task_europe_download_only)"
    return result


@celery.task(bind=True)
def task_vaccination_import_only(self):
    logger = get_task_logger(__name__)
    self.update_state(state=states.STARTED)
    logger.info("------------------------------------------------------------")
    logger.info(" Received: task_europe_import_only [OK] ")
    logger.info("------------------------------------------------------------")
    rki_vaccination_service.run_import_only()
    self.update_state(state=states.SUCCESS)
    result = "OK (task_europe_import_only)"
    return result


@celery.task(bind=True)
def task_vaccination_update_dimension_tables_only(self):
    logger = get_task_logger(__name__)
    self.update_state(state=states.STARTED)
    logger.info("------------------------------------------------------------")
    logger.info(" Received: task_europe_update_dimension_tables_only [OK] ")
    logger.info("------------------------------------------------------------")
    rki_vaccination_service.run_update_dimension_tables_only()
    self.update_state(state=states.SUCCESS)
    result = "OK (task_europe_update_dimension_tables_only)"
    return result


@celery.task(bind=True)
def task_vaccination_update_facttable_incremental_only(self):
    logger = get_task_logger(__name__)
    self.update_state(state=states.STARTED)
    logger.info("------------------------------------------------------------")
    logger.info(" Received: task_europe_update_fact_table_incremental_only [OK] ")
    logger.info("------------------------------------------------------------")
    rki_vaccination_service.run_update_fact_table_incremental_only()
    self.update_state(state=states.SUCCESS)
    result = "OK (task_europe_update_fact_table_incremental_only)"
    return result


@celery.task(bind=True)
def task_vaccination_update_facttable_initial_only(self):
    logger = get_task_logger(__name__)
    self.update_state(state=states.STARTED)
    logger.info("------------------------------------------------------------")
    logger.info(" Received: task_europe_update_fact_table_initial_only [OK] ")
    logger.info("------------------------------------------------------------")
    rki_vaccination_service.run_update_fact_table_initial_only()
    self.update_state(state=states.SUCCESS)
    result = "OK (task_europe_update_fact_table_initial_only)"
    return result


@celery.task(bind=True)
def task_vaccination_update_starschema_incremental(self):
    logger = get_task_logger(__name__)
    self.update_state(state=states.STARTED)
    logger.info("------------------------------------------------------------")
    logger.info(" Received: task_europe_update_star_schema_incremental [OK] ")
    logger.info("------------------------------------------------------------")
    rki_vaccination_service.run_update_star_schema_incremental()
    self.update_state(state=states.SUCCESS)
    result = "OK (task_europe_update_star_schema_incremental)"
    return result


@celery.task(bind=True)
def task_vaccination_task_update_starschema_initial(self):
    logger = get_task_logger(__name__)
    self.update_state(state=states.STARTED)
    logger.info("------------------------------------------------------------")
    logger.info(" Received: task_europe_update_star_schema_initial [OK] ")
    logger.info("------------------------------------------------------------")
    rki_vaccination_service.run_update_star_schema_initial()
    self.update_state(state=states.SUCCESS)
    result = "OK (task_europe_update_star_schema_initial)"
    return result


@app_rki_vaccination.route('/info')
def url_vaccination_info():
    page_info = ApplicationPage('Vaccination', "Info")
    return render_template(
        'rki_vaccination/vaccination_info.html',
        page_info=page_info)


@app_rki_vaccination.route('/tasks')
def url_vaccination_tasks():
    page_info = ApplicationPage('Vaccination', "Tasks")
    return render_template(
        'rki_vaccination/vaccination_tasks.html',
        page_info=page_info)


@app_rki_vaccination.route('/imported/page/<int:page>')
@app_rki_vaccination.route('/imported')
def url_vaccination_imported(page=1):
    page_info = ApplicationPage('Vaccination', "Data: Germany Timeline imported")
    page_data = RkiVaccinationImport.get_all_as_page(page)
    return render_template(
        'rki_vaccination/vaccination_imported.html',
        page_data=page_data,
        page_info=page_info)


@app_rki_vaccination.route('/data/page/<int:page>')
@app_rki_vaccination.route('/data')
def url_vaccination_data(page=1):
    page_info = ApplicationPage('Vaccination', "Data: Germany Timeline")
    page_data = RkiVaccinationData.get_all_as_page(page)
    return render_template(
        'rki_vaccination/vaccination_data.html',
        page_data=page_data,
        page_info=page_info)


@app_rki_vaccination.route('/date-reported/all/page/<int:page>')
@app_rki_vaccination.route('/date-reported/all')
def url_vaccination_datereported_all(page=1):
    page_info = ApplicationPage('Vaccination', "Germany Timeline")
    page_data = RkiVaccinationDateReported.get_all_as_page(page)
    return render_template(
        'rki_vaccination/vaccination_timeline_germany.html',
        page_data=page_data,
        page_info=page_info)


@app_rki_vaccination.route('/date-reported/<int:vaccination_date_reported_id>/page/<int:page>')
@app_rki_vaccination.route('/date-reported/<int:vaccination_date_reported_id>')
def url_vaccination_datereported_one(page=1, vaccination_date_reported_id=0):
    page_info = ApplicationPage('Vaccination', "Germany Timeline")
    datereported = RkiVaccinationDateReported.find_by_id(vaccination_date_reported_id)
    page_data = RkiVaccinationData.find_by_datum(page, datereported)
    return render_template(
        'rki_vaccination/vaccination_timeline_germany.html',
        datereported=datereported,
        page_data=page_data,
        page_info=page_info)


@app_rki_vaccination.route('/task/download/only')
def url_vaccination_task_download_only():
    flash("url_vaccination_task_download_only started")
    rki_vaccination_service.run_download_only()
    return redirect(url_for('vaccination.url_vaccination_tasks'))


@app_rki_vaccination.route('/task/import/only')
def url_vaccination_task_import_only():
    flash("url_vaccination_task_import_only started")
    task_vaccination_import_only.apply_async()
    return redirect(url_for('vaccination.url_vaccination_tasks'))


@app_rki_vaccination.route('/task/update/dimension-tables/only')
def url_vaccination_task_update_dimensiontables_only():
    flash("url_vaccination_task_update_dimensiontables_only started")
    task_vaccination_update_dimension_tables_only.apply_async()
    return redirect(url_for('vaccination.url_vaccination_tasks'))


@app_rki_vaccination.route('/task/update/fact-table/incremental/only')
def url_vaccination_task_update_facttable_incremental_only():
    flash("url_vaccination_task_update_facttable_incremental_only started")
    task_vaccination_update_facttable_incremental_only.apply_async()
    return redirect(url_for('vaccination.url_vaccination_tasks'))


@app_rki_vaccination.route('/task/update/fact-table/initial/only')
def url_vaccination_task_update_facttable_initial_only():
    flash("url_vaccination_task_update_facttable_initial_only started")
    task_vaccination_update_facttable_initial_only.apply_async()
    return redirect(url_for('vaccination.url_vaccination_tasks'))


@app_rki_vaccination.route('/task/update/star_schema/initial')
def url_vaccination_task_update_starschema_initial():
    flash("url_vaccination_task_update_star_schemainitial started")
    rki_vaccination_service.run_download_only()
    task_vaccination_task_update_starschema_initial.apply_async()
    return redirect(url_for('vaccination.url_vaccination_tasks'))


@app_rki_vaccination.route('/task/update/star_schema/incremental')
def url_vaccination_task_update_starschema_incremental():
    flash("url_vaccination_task_update_starschema_incremental started")
    rki_vaccination_service.run_download_only()
    task_vaccination_update_starschema_incremental.apply_async()
    return redirect(url_for('vaccination.url_vaccination_tasks'))
