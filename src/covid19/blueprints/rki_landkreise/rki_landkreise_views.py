from flask import render_template, redirect, url_for, flash, Blueprint
from sqlalchemy.exc import OperationalError
from flask_admin.contrib.sqla import ModelView
from celery import states

from database import app, admin, db

from covid19.blueprints.application.application_workers import celery
from covid19.blueprints.application.application_services import rki_service_landkreise
from covid19.blueprints.application.application_model import RkiDateReported
from covid19.blueprints.rki_landkreise.rki_landkreise_model import RkiLandkreise
from covid19.blueprints.rki_landkreise.rki_landkreise_model_import import RkiLandkreiseImport
from covid19.blueprints.application.application_model_transient import ApplicationPage

drop_and_create_data_again = True


app_rki_landkreise = Blueprint(
    'rki_landkreise', __name__,
    template_folder='templates',
    url_prefix='/rki/landkreise'
)

admin.add_view(ModelView(RkiLandkreiseImport, db.session, category="RKI Cases and Deaths"))
admin.add_view(ModelView(RkiLandkreise, db.session, category="RKI Cases and Deaths"))


##################################################################################################################
#
# RKI
#
##################################################################################################################
@app_rki_landkreise.route('/info')
def url_rki_landkreise_info():
    page_info = ApplicationPage('RKI', "Info")
    return render_template(
        'rki_landkreise/rki_landkreise_info.html',
        page_info=page_info)


@app_rki_landkreise.route('/tasks')
def url_rki_landkreise_tasks():
    page_info = ApplicationPage('RKI', "Tasks")
    return render_template(
        'rki_landkreise/rki_landkreise_tasks.html',
        page_info=page_info)


@app_rki_landkreise.route('/landkreise/imported/page/<int:page>')
@app_rki_landkreise.route('/landkreise/imported')
def url_rki_landkreise_imported(page=1):
    page_info = ApplicationPage('RKI', "Last Import")
    try:
        page_data = RkiLandkreiseImport.get_all_as_page(page)
    except OperationalError:
        flash("No data in the database.")
        page_data = None
    return render_template(
        'rki_landkreise/rki_landkreise_imported.html',
        page_data=page_data,
        page_info=page_info)

# ------------------------------------------------------------------------
#  Celery TASKS
# ------------------------------------------------------------------------


@celery.task(bind=True)
def task_rki_landkreise_task_update_starschema_initial(self):
    self.update_state(state=states.STARTED)
    rki_service_landkreise.run_update_star_schema_initial()
    self.update_state(state=states.SUCCESS)
    result = "OK (task_rki_landkreise_task_update_starschema_initial)"
    return result


@celery.task(bind=True)
def task_rki_landkreise_task_update_starschema_incremental(self):
    self.update_state(state=states.STARTED)
    rki_service_landkreise.run_update_star_schema_incremental()
    self.update_state(state=states.SUCCESS)
    result = "OK (task_rki_landkreise_task_update_starschema_incremental)"
    return result


@celery.task(bind=True)
def task_rki_landkreise_task_import_only(self):
    self.update_state(state=states.STARTED)
    rki_service_landkreise.run_import_only()
    self.update_state(state=states.SUCCESS)
    result = "OK (task_rki_bundeslaender_task_update_starschema_incremental)"
    return result


@celery.task(bind=True)
def task_rki_landkreise_task_update_dimensiontables_only(self):
    self.update_state(state=states.STARTED)
    rki_service_landkreise.run_update_dimension_tables_only()
    self.update_state(state=states.SUCCESS)
    result = "OK (task_rki_landkreise_task_update_dimensiontables_only)"
    return result


@celery.task(bind=True)
def task_rki_landkreise_task_update_facttable_incremental_only(self):
    self.update_state(state=states.STARTED)
    rki_service_landkreise.run_update_fact_table_initial_only()
    self.update_state(state=states.SUCCESS)
    result = "OK (task_rki_landkreise_task_update_facttable_incremental_only)"
    return result


@celery.task(bind=True)
def task_rki_landkreise_task_update_facttable_initial_only(self):
    self.update_state(state=states.STARTED)
    rki_service_landkreise.run_update_fact_table_initial_only()
    self.update_state(state=states.SUCCESS)
    result = "OK (task_rki_landkreise_task_update_facttable_initial_only)"
    return result


@celery.task(bind=True)
def task_url_rki_landkreise_task_update_dimension_tables_only(self):
    self.update_state(state=states.STARTED)
    rki_service_landkreise.run_update_star_schema_incremental()
    self.update_state(state=states.SUCCESS)
    result = "OK (task_url_rki_landkreise_task_update_dimension_tables_only)"
    return result

# ------------------------------------------------------------------------
#  URL Routes for Celery TASKS
# ------------------------------------------------------------------------


@app_rki_landkreise.route('/landkreise/task/update/star_schema/initial')
def url_rki_landkreise_task_update_starschema_initial():
    app.logger.info("url_rki_landkreise_task_update_starschema_initial [start]")
    task_rki_landkreise_task_update_starschema_initial.apply_async()
    return redirect(url_for('rki_landkreise.url_rki_tasks'))


@app_rki_landkreise.route('/landkreise/task/update/star_schema/incremental')
def url_rki_landkreise_task_update_starschema_incremental():
    app.logger.info("url_rki_landkreise_task_update_starschema_incremental [start]")
    task_rki_landkreise_task_update_starschema_incremental.apply_async()
    return redirect(url_for('rki_landkreise.url_rki_tasks'))


@app_rki_landkreise.route('/landkreise/task/download/only')
def url_rki_landkreise_task_download_only():
    app.logger.info("url_rki_landkreise_task_download_only [start]")
    rki_service_landkreise.run_download_only()
    return redirect(url_for('rki_landkreise.url_rki_tasks'))


@app_rki_landkreise.route('/landkreise/task/import/only')
def url_rki_landkreise_task_import_only():
    app.logger.info("url_rki_landkreise_task_import_only [start]")
    task_rki_landkreise_task_import_only.apply_async()
    return redirect(url_for('rki_landkreise.url_rki_tasks'))


@app_rki_landkreise.route('/landkreise/task/update/dimension-tables/only')
def url_rki_landkreise_task_update_dimensiontables_only():
    app.logger.info("url_rki_landkreise_task_update_dimensiontables_only [start]")
    task_rki_landkreise_task_update_dimensiontables_only.apply_async()
    return redirect(url_for('rki_landkreise.url_rki_tasks'))


@app_rki_landkreise.route('/landkreise/task/update/fact-table/incremental/only')
def url_rki_landkreise_task_update_facttable_incremental_only():
    app.logger.info("url_rki_landkreise_task_update_facttable_incremental_only [start]")
    task_rki_landkreise_task_update_facttable_incremental_only.apply_async()
    return redirect(url_for('rki_landkreise.url_rki_tasks'))


@app_rki_landkreise.route('/landkreise/task/update/fact-table/initial/only')
def url_rki_landkreise_task_update_facttable_initial_only():
    app.logger.info("url_rki_landkreise_task_update_facttable_initial_only [start]")
    task_rki_landkreise_task_update_facttable_initial_only.apply_async()
    return redirect(url_for('rki_landkreise.url_rki_tasks'))


@app_rki_landkreise.route('/task/update/dimension-tables/only')
def url_rki_landkreise_task_update_dimension_tables_only():
    app.logger.info("url_task_who_update_dimension_tables_only [start]")
    task_url_rki_landkreise_task_update_dimension_tables_only.apply_async()
    return redirect(url_for('rki_landkreise.url_rki_tasks'))
