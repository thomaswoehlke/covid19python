from flask import render_template, redirect, url_for, flash, Blueprint
from celery import states
from celery.utils.log import get_task_logger
from flask_admin.contrib.sqla import ModelView

from database import app, admin, db
from covid19.blueprints.application.application_services import ecdc_service
from covid19.blueprints.application.application_workers import celery

from covid19.blueprints.ecdc.ecdc_model_import import EcdcImport
from covid19.blueprints.ecdc.ecdc_model import EcdcDateReported, EcdcContinent, EcdcCountry, EcdcData
from covid19.blueprints.application.application_model_transient import ApplicationPage


app_ecdc = Blueprint('ecdc', __name__, template_folder='templates', url_prefix='/ecdc')

admin.add_view(ModelView(EcdcImport, db.session, category="ECDC"))
admin.add_view(ModelView(EcdcDateReported, db.session, category="ECDC"))
admin.add_view(ModelView(EcdcContinent, db.session, category="ECDC"))
admin.add_view(ModelView(EcdcCountry, db.session, category="ECDC"))
admin.add_view(ModelView(EcdcData, db.session, category="ECDC"))


# ---------------------------------------------------------------------------------------------------------------
#  Url Routes Frontend
# ---------------------------------------------------------------------------------------------------------------

@app_ecdc.route('/info')
def url_ecdc_info():
    page_info = ApplicationPage('Europe', "Info")
    return render_template(
        'ecdc/ecdc_info.html',
        title='Europe',
        page_info=page_info)


@app_ecdc.route('/tasks')
def url_ecdc_tasks():
    page_info = ApplicationPage('Europe', "Tasks")
    return render_template(
        'ecdc/ecdc_tasks.html',
        title='Europe Tasks',
        page_info=page_info)


@app_ecdc.route('/imported/page/<int:page>')
@app_ecdc.route('/imported')
def url_ecdc_data_imported(page=1):
    page_info = ApplicationPage('Europe', "Last Import")
    page_data = EcdcImport.get_all_as_page(page)
    return render_template(
        'ecdc/imported/ecdc_imported.html',
        page_data=page_data,
        page_info=page_info)


@app_ecdc.route('/date_reported/all/page/<int:page>')
@app_ecdc.route('/date_reported/all')
def url_ecdc_date_reported_all(page=1):
    page_info = ApplicationPage('Europe', "date_reported")
    page_data = EcdcDateReported.get_all_as_page(page)
    return render_template(
        'ecdc/date_reported/ecdc_date_reported_all.html',
        page_data=page_data,
        page_info=page_info)


@app_ecdc.route('/date_reported/<int:europe_date_reported_id>/page/<int:page>')
@app_ecdc.route('/date_reported/<int:europe_date_reported_id>')
@app_ecdc.route('/date_reported/notification_rate/<int:europe_date_reported_id>/page/<int:page>')
@app_ecdc.route('/date_reported/notification_rate/<int:europe_date_reported_id>')
def url_ecdc_date_reported_one_notification_rate(europe_date_reported_id, page=1):
    page_info = ApplicationPage('Europe', "date_reported")
    europe_date_reported = EcdcDateReported.get_by_id(europe_date_reported_id)
    page_data = EcdcData.find_by_date_reported_notification_rate(europe_date_reported, page)
    return render_template(
        'ecdc/date_reported/ecdc_date_reported_one_notification_rate.html',
        europe_date_reported=europe_date_reported,
        page_data=page_data,
        page_info=page_info)


@app_ecdc.route('/date_reported/deaths_weekly/<int:europe_date_reported_id>/page/<int:page>')
@app_ecdc.route('/date_reported/deaths_weekly/<int:europe_date_reported_id>')
def url_ecdc_date_reported_one_deaths_weekly(europe_date_reported_id, page=1):
    page_info = ApplicationPage('Europe', "date_reported")
    europe_date_reported = EcdcDateReported.get_by_id(europe_date_reported_id)
    page_data = EcdcData.find_by_date_reported_deaths_weekly(europe_date_reported, page)
    return render_template(
        'ecdc/date_reported/ecdc_date_reported_one_deaths_weekly.html',
        europe_date_reported=europe_date_reported,
        page_data=page_data,
        page_info=page_info)


@app_ecdc.route('/date_reported/cases_weekly/<int:europe_date_reported_id>/page/<int:page>')
@app_ecdc.route('/date_reported/cases_weekly/<int:europe_date_reported_id>')
def url_ecdc_date_reported_one_cases_weekly(europe_date_reported_id, page=1):
    page_info = ApplicationPage('Europe', "date_reported")
    europe_date_reported = EcdcDateReported.get_by_id(europe_date_reported_id)
    page_data = EcdcData.find_by_date_reported_cases_weekly(europe_date_reported, page)
    return render_template(
        'ecdc/date_reported/ecdc_date_reported_one_cases_weekly.html',
        europe_date_reported=europe_date_reported,
        page_data=page_data,
        page_info=page_info)


@app_ecdc.route('/continent/all/page/<int:page>')
@app_ecdc.route('/continent/all')
def url_ecdc_continent_all(page=1):
    page_info = ApplicationPage('Europe', "continent")
    page_data = EcdcContinent.get_all_as_page(page)
    return render_template(
        'ecdc/continent/ecdc_continent_all.html',
        page_data=page_data,
        page_info=page_info)


@app_ecdc.route('/continent/<int:continent_id>/page/<int:page>')
@app_ecdc.route('/continent/<int:continent_id>')
def url_ecdc_continent_one(continent_id, page=1):
    page_info = ApplicationPage('Europe', "continent")
    continent = EcdcContinent.get_by_id(continent_id)
    page_data = EcdcCountry.find_by_continent(continent, page)
    return render_template(
        'ecdc/continent/ecdc_continent_one.html',
        continent=continent,
        page_data=page_data,
        page_info=page_info)


@app_ecdc.route('/country/all/page/<int:page>')
@app_ecdc.route('/country/all')
def url_ecdc_country_all(page=1):
    page_info = ApplicationPage('Europe', "country")
    page_data = EcdcCountry.get_all_as_page(page)
    return render_template(
        'ecdc/country/ecdc_country_all.html',
        page_data=page_data,
        page_info=page_info)


@app_ecdc.route('/country/<int:country_id>/page/<int:page>')
@app_ecdc.route('/country/<int:country_id>')
def url_ecdc_country_one(country_id, page=1):
    page_info = ApplicationPage('Europe', "country")
    europe_country = EcdcCountry.get_by_id(country_id)
    page_data = EcdcData.find_by_country(europe_country, page)
    return render_template(
        'ecdc/country/ecdc_country_one.html',
        europe_country=europe_country,
        page_data=page_data,
        page_info=page_info)


@app_ecdc.route('/country/germany/page/<int:page>')
@app_ecdc.route('/country/germany')
def url_ecdc_country_germany(page=1):
    page_info = ApplicationPage('Europe', "country: Germany")
    europe_country = EcdcCountry.get_germany()
    if europe_country is None:
        flash('country: Germany not found in Database', category='error')
        return redirect(url_for('ecdc.url_ecdc_tasks'))
    page_data = EcdcData.find_by_country(europe_country, page)
    return render_template(
        'ecdc/country/ecdc_country_germany.html',
        europe_country=europe_country,
        page_data=page_data,
        page_info=page_info)


# ----------------------------------------------------------------------------------------------------------------
#  Celery TASKS
# ----------------------------------------------------------------------------------------------------------------


@celery.task(bind=True)
def task_ecdc_download_only(self):
    logger = get_task_logger(__name__)
    self.update_state(state=states.STARTED)
    logger.info("------------------------------------------------------------")
    logger.info(" Received: task_ecdc_download_only [OK] ")
    logger.info("------------------------------------------------------------")
    ecdc_service.run_download_only()
    self.update_state(state=states.SUCCESS)
    result = "OK (task_ecdc_download_only)"
    return result


@celery.task(bind=True)
def task_ecdc_import_only(self):
    logger = get_task_logger(__name__)
    self.update_state(state=states.STARTED)
    logger.info("------------------------------------------------------------")
    logger.info(" Received: task_ecdc_import_only [OK] ")
    logger.info("------------------------------------------------------------")
    ecdc_service.run_import_only()
    self.update_state(state=states.SUCCESS)
    result = "OK (task_ecdc_import_only)"
    return result


@celery.task(bind=True)
def task_ecdc_update_dimension_tables_only(self):
    logger = get_task_logger(__name__)
    self.update_state(state=states.STARTED)
    logger.info("------------------------------------------------------------")
    logger.info(" Received: task_ecdc_update_dimension_tables_only [OK] ")
    logger.info("------------------------------------------------------------")
    ecdc_service.run_update_dimension_tables_only()
    self.update_state(state=states.SUCCESS)
    result = "OK (task_ecdc_update_dimension_tables_only)"
    return result


@celery.task(bind=True)
def task_ecdc_update_fact_table_incremental_only(self):
    logger = get_task_logger(__name__)
    self.update_state(state=states.STARTED)
    logger.info("------------------------------------------------------------")
    logger.info(" Received: task_ecdc_update_fact_table_incremental_only [OK] ")
    logger.info("------------------------------------------------------------")
    ecdc_service.run_update_fact_table_incremental_only()
    self.update_state(state=states.SUCCESS)
    result = "OK (task_ecdc_update_fact_table_incremental_only)"
    return result


@celery.task(bind=True)
def task_ecdc_update_fact_table_incremental_only(self):
    logger = get_task_logger(__name__)
    self.update_state(state=states.STARTED)
    logger.info("------------------------------------------------------------")
    logger.info(" Received: task_ecdc_update_fact_table_incremental_only [OK] ")
    logger.info("------------------------------------------------------------")
    ecdc_service.run_update_fact_table_incremental_only()
    self.update_state(state=states.SUCCESS)
    result = "OK (task_ecdc_update_fact_table_incremental_only)"
    return result


@celery.task(bind=True)
def task_ecdc_update_fact_table_initial_only(self):
    logger = get_task_logger(__name__)
    self.update_state(state=states.STARTED)
    logger.info("------------------------------------------------------------")
    logger.info(" Received: task_ecdc_update_fact_table_initial_only [OK] ")
    logger.info("------------------------------------------------------------")
    ecdc_service.run_update_fact_table_initial_only()
    self.update_state(state=states.SUCCESS)
    result = "OK (task_ecdc_update_fact_table_initial_only)"
    return result


@celery.task(bind=True)
def task_ecdc_update_star_schema_incremental(self):
    logger = get_task_logger(__name__)
    self.update_state(state=states.STARTED)
    logger.info("------------------------------------------------------------")
    logger.info(" Received: task_ecdc_update_star_schema_incremental [OK] ")
    logger.info("------------------------------------------------------------")
    ecdc_service.run_update_star_schema_incremental()
    self.update_state(state=states.SUCCESS)
    result = "OK (task_ecdc_update_star_schema_incremental)"
    return result


@celery.task(bind=True)
def task_ecdc_update_star_schema_initial(self):
    logger = get_task_logger(__name__)
    self.update_state(state=states.STARTED)
    logger.info("------------------------------------------------------------")
    logger.info(" Received: task_ecdc_update_star_schema_initial [OK] ")
    logger.info("------------------------------------------------------------")
    ecdc_service.run_update_star_schema_initial()
    self.update_state(state=states.SUCCESS)
    result = "OK (task_ecdc_update_star_schema_initial)"
    return result

# ----------------------------------------------------------------------------------------------------------------
#  URL Routes for Celery TASKS
# ----------------------------------------------------------------------------------------------------------------


# TODO: #163 implement url_ecdc_task_update_star_schema_initial in europe_views.py
@app_ecdc.route('/task/update/star_schema/initial')
def url_ecdc_task_update_star_schema_initial():
    flash("url_ecdc_task_update_star_schema_initial started")
    ecdc_service.run_download_only()
    task_ecdc_update_star_schema_initial.apply_async()
    return redirect(url_for('ecdc.url_ecdc_tasks'))


# TODO: #164 implement url_ecdc_task_update_starschema_incremental in europe_views.py
@app_ecdc.route('/task/update/star_schema/incremental')
def url_ecdc_task_update_starschema_incremental():
    flash("url_ecdc_task_update_starschema_incremental started")
    ecdc_service.run_download_only()
    task_ecdc_update_star_schema_incremental.apply_async()
    return redirect(url_for('ecdc.url_ecdc_tasks'))


# TODO: #165 implement url_ecdc_task_download_only in europe_views.py
@app_ecdc.route('/task/download/only')
def url_ecdc_task_download_only():
    flash("url_ecdc_task_download_only started")
    ecdc_service.run_download_only()
    return redirect(url_for('ecdc.url_ecdc_tasks'))


# TODO: #166 implement url_ecdc_task_import_only in europe_views.py
@app_ecdc.route('/task/import/only')
def url_ecdc_task_import_only():
    flash("url_ecdc_task_import_only started")
    task_ecdc_import_only.apply_async()
    return redirect(url_for('ecdc.url_ecdc_tasks'))


# TODO: #167 implement url_ecdc_task_update_dimensiontables_only in europe_views.py
@app_ecdc.route('/task/update/dimension-tables/only')
def url_ecdc_task_update_dimensiontables_only():
    flash("url_ecdc_task_update_dimensiontables_only started")
    task_ecdc_update_dimension_tables_only.apply_async()
    return redirect(url_for('ecdc.url_ecdc_tasks'))


# TODO: #168 implement url_ecdc_task_update_facttable_incremental_only in europe_views.py
@app_ecdc.route('/task/update/fact-table/incremental/only')
def url_ecdc_task_update_facttable_incremental_only():
    flash("url_ecdc_task_update_facttable_incremental_only started")
    task_ecdc_update_fact_table_incremental_only.apply_async()
    return redirect(url_for('ecdc.url_ecdc_tasks'))


# TODO: #169 implement url_ecdc_task_update_facttable_initial_only in europe_views.py
@app_ecdc.route('/task/update/fact-table/initial/only')
def url_ecdc_task_update_facttable_initial_only():
    flash("url_ecdc_task_update_facttable_initial_only started")
    task_ecdc_update_fact_table_initial_only.apply_async()
    return redirect(url_for('ecdc.url_ecdc_tasks'))
