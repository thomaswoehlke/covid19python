from flask import render_template, redirect, url_for, flash, Blueprint
from celery import states
from celery.utils.log import get_task_logger

from database import app
from covid19.services import vaccination_service
from covid19.workers import celery

from covid19.blueprints.vaccination.vaccination_model import VaccinationData
from covid19.blueprints.vaccination.vaccination_model_import import VaccinationImport
from covid19.blueprints.common.common_model_transient import ApplicationPage


app_vaccination = Blueprint('vaccination', __name__, template_folder='templates')


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
    vaccination_service.task_europe_download_only() # TODO
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
    vaccination_service.task_europe_import_only() # TODO
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
    vaccination_service.task_europe_update_dimension_tables_only() # TODO
    self.update_state(state=states.SUCCESS)
    result = "OK (task_europe_update_dimension_tables_only)"
    return result


@celery.task(bind=True)
def task_vaccination_update_fact_table_incremental_only(self):
    logger = get_task_logger(__name__)
    self.update_state(state=states.STARTED)
    logger.info("------------------------------------------------------------")
    logger.info(" Received: task_europe_update_fact_table_incremental_only [OK] ")
    logger.info("------------------------------------------------------------")
    vaccination_service.task_europe_update_fact_table_incremental_only() # TODO
    self.update_state(state=states.SUCCESS)
    result = "OK (task_europe_update_fact_table_incremental_only)"
    return result


@celery.task(bind=True)
def task_vaccination_update_fact_table_initial_only(self):
    logger = get_task_logger(__name__)
    self.update_state(state=states.STARTED)
    logger.info("------------------------------------------------------------")
    logger.info(" Received: task_europe_update_fact_table_initial_only [OK] ")
    logger.info("------------------------------------------------------------")
    vaccination_service.task_europe_update_fact_table_initial_only() # TODO
    self.update_state(state=states.SUCCESS)
    result = "OK (task_europe_update_fact_table_initial_only)"
    return result


@celery.task(bind=True)
def task_vaccination_update_fact_table_initial_only(self):
    logger = get_task_logger(__name__)
    self.update_state(state=states.STARTED)
    logger.info("------------------------------------------------------------")
    logger.info(" Received: task_europe_update_fact_table_initial_only [OK] ")
    logger.info("------------------------------------------------------------")
    vaccination_service.task_europe_update_fact_table_initial_only() # TODO
    self.update_state(state=states.SUCCESS)
    result = "OK (task_europe_update_fact_table_initial_only)"
    return result


@celery.task(bind=True)
def task_vaccination_update_star_schema_incremental(self):
    logger = get_task_logger(__name__)
    self.update_state(state=states.STARTED)
    logger.info("------------------------------------------------------------")
    logger.info(" Received: task_europe_update_star_schema_incremental [OK] ")
    logger.info("------------------------------------------------------------")
    vaccination_service.task_europe_update_star_schema_incremental() # TODO
    self.update_state(state=states.SUCCESS)
    result = "OK (task_europe_update_star_schema_incremental)"
    return result


@celery.task(bind=True)
def task_vaccination_update_star_schema_initial(self):
    logger = get_task_logger(__name__)
    self.update_state(state=states.STARTED)
    logger.info("------------------------------------------------------------")
    logger.info(" Received: task_europe_update_star_schema_initial [OK] ")
    logger.info("------------------------------------------------------------")
    vaccination_service.task_europe_update_star_schema_initial()  # TODO
    self.update_state(state=states.SUCCESS)
    result = "OK (task_europe_update_star_schema_initial)"
    return result


@celery.task(bind=True)
def task_vaccination_update_initial(self):
    logger = get_task_logger(__name__)
    self.update_state(state=states.STARTED)
    logger.info("------------------------------------------------------------")
    logger.info(" Received: task_vaccination_update_initial [OK] ")
    logger.info("------------------------------------------------------------")
    vaccination_service.run_update_initial()
    self.update_state(state=states.SUCCESS)
    result = "OK (task_vaccination_update_initial)"
    return result


@app_vaccination.route('/info')
def url_vaccination_info():
    page_info = ApplicationPage('Vaccination', "Info")
    return render_template(
        'vaccination/vaccination_info.html',
        page_info=page_info)


@app_vaccination.route('/tasks')
def url_vaccination_tasks():
    page_info = ApplicationPage('Vaccination', "Tasks")
    return render_template(
        'vaccination/vaccination_tasks.html',
        page_info=page_info)


@app_vaccination.route('/update/initial')
def url_vaccination_update_data():
    vaccination_service.run_download()
    flash("vaccination_service.run_download done")
    task_vaccination_update_initial.apply_async()
    flash("vaccination_service.run_update started")
    return redirect(url_for('url_vaccination_tasks'))


@app_vaccination.route('/timeline/germany/page/<int:page>')
@app_vaccination.route('/timeline/germany')
def url_vaccination_timeline_germany(page=1):
    page_info = ApplicationPage('Vaccination', "Germany Timeline")
    # page_data = VaccinationImport.get_all_as_page(page)
    page_data = VaccinationData.get_all_as_page(page)
    return render_template(
        'vaccination/vaccination_timeline_germany.html',
        page_data=page_data,
        page_info=page_info)

# TODO: #106 add Tasks and URLs for starting Tasks to vaccination_views


@app_vaccination.route('/task/update/star_schema/initial')
def url_vaccination_task_update_star_schema_initial():
    flash("url_vaccination_task_update_star_schema_initial started")
    # TODO: #170 implement url_vaccination_task_update_star_schema_initial in vaccination_views.py
    return redirect(url_for('url_europe_tasks'))


@app_vaccination.route('/task/update/star_schema/incremental')
def url_vaccination_task_update_starschema_incremental():
    flash("url_vaccination_task_update_starschema_incremental started")
    # TODO: #171 implement url_vaccination_task_update_starschema_incremental in vaccination_views.py
    return redirect(url_for('url_europe_tasks'))


@app_vaccination.route('/task/download/only')
def url_vaccination_task_download_only():
    flash("url_vaccination_task_download_only started")
    # TODO: #172 implement url_vaccination_task_import_only in vaccination_views.py
    return redirect(url_for('url_europe_tasks'))


@app_vaccination.route('/task/import/only')
def url_vaccination_task_import_only():
    flash("url_vaccination_task_import_only started")
    # TODO: #173 implement url_vaccination_task_import_only in vaccination_views.py
    return redirect(url_for('url_europe_tasks'))


@app_vaccination.route('/task/update/dimension-tables/only')
def url_vaccination_task_update_dimensiontables_only():
    flash("url_vaccination_task_update_dimensiontables_only started")
    # TODO: #174 implement url_vaccination_task_update_dimensiontables_only in vaccination_views.py
    return redirect(url_for('url_europe_tasks'))


@app_vaccination.route('/task/update/fact-table/incremental/only')
def url_vaccination_task_update_facttable_incremental_only():
    flash("url_vaccination_task_update_facttable_incremental_only started")
    # TODO: #175 implement url_vaccination_task_update_facttable_incremental_only in vaccination_views.py
    return redirect(url_for('url_europe_tasks'))


@app_vaccination.route('/task/update/fact-table/initial/only')
def url_vaccination_task_update_facttable_initial_only():
    flash("url_vaccination_task_update_facttable_initial_only started")
    # TODO: #176 implement url_vaccination_task_update_facttable_initial_only in vaccination_views.py
    return redirect(url_for('url_europe_tasks'))

