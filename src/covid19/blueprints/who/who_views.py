from flask import render_template, redirect, url_for, flash, Blueprint
from sqlalchemy.exc import OperationalError
from celery import states
from celery.utils.log import get_task_logger

from database import app
from covid19.services import who_service
from covid19.workers import celery

from covid19.blueprints.who.who_model_import import WhoGlobalDataImportTable
from covid19.blueprints.who.who_model import WhoRegion, WhoCountry, WhoDateReported, WhoGlobalData
from covid19.blueprints.common.common_model_transient import ApplicationPage


app_who = Blueprint('who', __name__, template_folder='templates')


##################################################################################################################
#
# WHO
#
##################################################################################################################


@celery.task(bind=True)
def task_who_download_only(self):
    logger = get_task_logger(__name__)
    self.update_state(state=states.STARTED)
    logger.info("------------------------------------------------------------")
    logger.info(" Received: task_who_download_only [OK] ")
    logger.info("------------------------------------------------------------")
    who_service.run_download_only()
    self.update_state(state=states.SUCCESS)
    result = "OK (task_who_download_only)"
    return result


@celery.task(bind=True)
def task_who_import_only(self):
    logger = get_task_logger(__name__)
    self.update_state(state=states.STARTED)
    logger.info("------------------------------------------------------------")
    logger.info(" Received: task_who_import_only [OK] ")
    logger.info("------------------------------------------------------------")
    who_service.run_import_only()
    self.update_state(state=states.SUCCESS)
    result = "OK (task_who_import_only)"
    return result


@celery.task(bind=True)
def task_who_update_dimension_tables_only(self):
    logger = get_task_logger(__name__)
    self.update_state(state=states.STARTED)
    logger.info("------------------------------------------------------------")
    logger.info(" Received: task_who_update_dimension_tables_only [OK] ")
    logger.info("------------------------------------------------------------")
    who_service.run_update_dimension_tables_only()
    self.update_state(state=states.SUCCESS)
    result = "OK (task_who_update_dimension_tables_only)"
    return result


@celery.task(bind=True)
def task_who_update_fact_table_incremental_only(self):
    logger = get_task_logger(__name__)
    self.update_state(state=states.STARTED)
    logger.info("------------------------------------------------------------")
    logger.info(" Received: task_who_update_fact_table_incremental_only [OK] ")
    logger.info("------------------------------------------------------------")
    who_service.run_update_fact_table_incremental_only()
    self.update_state(state=states.SUCCESS)
    result = "OK (task_who_update_dimension_tables_only)"
    return result


@celery.task(bind=True)
def task_who_update_fact_table_initial_only(self):
    logger = get_task_logger(__name__)
    self.update_state(state=states.STARTED)
    logger.info("------------------------------------------------------------")
    logger.info(" Received: task_who_update_fact_table_initial_only [OK] ")
    logger.info("------------------------------------------------------------")
    who_service.run_update_fact_table_initial_only()
    self.update_state(state=states.SUCCESS)
    result = "OK (task_who_update_fact_table_initial_only)"
    return result


@celery.task(bind=True)
def task_who_update_star_schema_incremental(self):
    logger = get_task_logger(__name__)
    self.update_state(state=states.STARTED)
    logger.info("------------------------------------------------------------")
    logger.info(" Received: task_who_update_star_schema_incremental [OK] ")
    logger.info("------------------------------------------------------------")
    who_service.run_update_star_schema_incremental()
    self.update_state(state=states.SUCCESS)
    result = "OK (task_who_update_star_schema_incremental)"
    return result


@celery.task(bind=True)
def task_who_update_star_schema_initial(self):
    logger = get_task_logger(__name__)
    self.update_state(state=states.STARTED)
    logger.info("------------------------------------------------------------")
    logger.info(" Received: task_who_update_star_schema_initial [OK] ")
    logger.info("------------------------------------------------------------")
    who_service.run_update_star_schema_initial()
    self.update_state(state=states.SUCCESS)
    result = "OK (task_who_update_star_schema_incremental)"
    return result


@app_who.route('/task/download/only')
def url_task_who_download_only():
    app.logger.info("url_who_task_download_only [start]")
    who_service.run_download_only()
    flash("who_service.run_download_only ok")
    app.logger.info("url_who_task_download_only [done]")
    return redirect(url_for('who.url_who_tasks'))


@app_who.route('/task/import/only')
def url_task_who_import_only():
    app.logger.info("url_who_update_run [start]")
    task_who_import_only.apply_async()
    flash("who_service.run_update started")
    flash(message="long running background task started", category="warning")
    app.logger.info("url_who_update_run [done]")
    return redirect(url_for('who.url_who_tasks'))


@app_who.route('/task/update/dimension-tables/only')
def url_task_who_update_dimension_tables_only():
    app.logger.info("url_task_who_update_dimension_tables_only [start]")
    task_who_update_dimension_tables_only.apply_async()
    flash("task_who_update_dimension_tables_only started")
    flash(message="long running background task started", category="warning")
    app.logger.info("url_task_who_update_dimension_tables_only [done]")
    return redirect(url_for('who.url_who_tasks'))


@app_who.route('/task/update/fact-table/incremental/only')
def url_task_who_update_fact_table_incremental_only():
    app.logger.info("url_task_who_update_fact_table_incremental_only [start]")
    task_who_update_fact_table_incremental_only.apply_async()
    flash("task_who_update_fact_table_incremental_only started")
    flash(message="long running background task started", category="warning")
    app.logger.info("url_task_who_update_fact_table_incremental_only [done]")
    return redirect(url_for('who.url_who_tasks'))


@app_who.route('/task/update/fact-table/initial/only')
def url_task_who_update_fact_table_initial_only():
    app.logger.info("url_task_who_update_fact_table_initial_only [start]")
    task_who_update_fact_table_initial_only.apply_async()
    flash("task_who_update_fact_table_initial_only started")
    flash(message="long running background task started", category="warning")
    app.logger.info("url_who_task_update_full [done]")
    return redirect(url_for('who.url_who_tasks'))


@app_who.route('/task/update/star_schema/initial')
def url_task_who_update_star_schema_initial():
    app.logger.info("url_who_task_update_full [start]")
    who_service.run_download_only()
    flash("who_service.who_service_download.download_file ok")
    task_who_update_star_schema_initial.apply_async()
    flash("task_who_update_star_schema_initial started")
    flash(message="long running background task started", category="warning")
    app.logger.info("url_who_task_update_full [done]")
    return redirect(url_for('who.url_who_tasks'))


@app_who.route('/task/update/star_schema/incremental')
def url_task_who_update_star_schema_incremental():
    app.logger.info("url_task_who_update_star_schema_incremental [start]")
    who_service.run_download_only()
    flash("who_service.who_service_download.download_file ok")
    task_who_update_star_schema_incremental.apply_async()
    flash("task_who_run_update_full started")
    flash(message="long running background task started", category="warning")
    app.logger.info("url_task_who_update_star_schema_incremental [done]")
    return redirect(url_for('who.url_who_tasks'))


@app_who.route('/info')
def url_who_info():
    page_info = ApplicationPage('WHO', "Info")
    return render_template(
        'who/who_info.html',
        page_info=page_info)


@app_who.route('/tasks')
def url_who_tasks():
    page_info = ApplicationPage('WHO', "Tasks")
    return render_template(
        'who/who_tasks.html',
        page_info=page_info)


@app_who.route('/imported/page/<int:page>')
@app_who.route('/imported')
def url_who_imported(page=1):
    page_info = ApplicationPage('WHO', "Last Import")
    try:
        page_data = WhoGlobalDataImportTable.get_all_as_page(page)
    except OperationalError:
        flash("No data in the database.")
        page_data = None
    return render_template(
        'who/who_imported.html',
        page_data=page_data,
        page_info=page_info)


@app_who.route('/date_reported/all/page/<int:page>')
@app_who.route('/date_reported/all')
def url_who_date_reported_all(page=1):
    page_info = ApplicationPage('WHO', "Date Reported", "All")
    try:
        page_data = WhoDateReported.get_all_as_page(page)
    except OperationalError:
        flash("No regions in the database.")
        page_data = None
    return render_template(
        'who/date_reported/who_date_reported_all.html',
        page_data=page_data,
        page_info=page_info)


@app_who.route('/date_reported/<int:date_reported_id>/page/<int:page>')
@app_who.route('/date_reported/<int:date_reported_id>')
def url_who_date_reported(date_reported_id, page=1):
    date_reported = WhoDateReported.get_by_id(date_reported_id)
    page_info = ApplicationPage(
        "Date Reported: " + date_reported.date_reported,
        'WHO',
        "data of all reported countries for WHO date reported " + date_reported.date_reported + " "
    )
    try:
        page_data = WhoGlobalData.get_data_for_day(date_reported, page)
    except OperationalError:
        flash("No data in the database.")
        page_data = None
    return render_template(
        'who/date_reported/who_date_reported_one.html',
        who_date_reported=date_reported,
        page_data=page_data,
        page_info=page_info)


@app_who.route('/date_reported/<int:date_reported_id>/cases_new/page/<int:page>')
@app_who.route('/date_reported/<int:date_reported_id>/cases_new')
def url_who_date_reported_cases_new(date_reported_id, page=1):
    date_reported = WhoDateReported.get_by_id(date_reported_id)
    page_info = ApplicationPage(
        "Date Reported: " + date_reported.date_reported,
        'WHO',
        "data of all reported countries for WHO date reported " + date_reported.date_reported + " "
    )
    try:
        page_data = WhoGlobalData.get_data_for_day_order_by_cases_new(date_reported, page)
    except OperationalError:
        flash("No data in the database.")
        page_data = None
    return render_template(
        'who/date_reported/who_date_reported_one_cases_new.html',
        who_date_reported=date_reported,
        page_data=page_data,
        page_info=page_info)


@app_who.route('/date_reported/<int:date_reported_id>/cases_cumulative/page/<int:page>')
@app_who.route('/date_reported/<int:date_reported_id>/cases_cumulative')
def url_who_date_reported_cases_cumulative(date_reported_id, page=1):
    date_reported = WhoDateReported.get_by_id(date_reported_id)
    page_info = ApplicationPage(
        "Date Reported: " + date_reported.date_reported,
        'WHO',
        "data of all reported countries for WHO date reported " + date_reported.date_reported + " "
    )
    try:
        page_data = WhoGlobalData.get_data_for_day_order_by_cases_cumulative(date_reported, page)
    except OperationalError:
        flash("No data in the database.")
        page_data = None
    return render_template(
        'who/date_reported/who_date_reported_one_cases_cumulative.html',
        who_date_reported=date_reported,
        page_data=page_data,
        page_info=page_info)


@app_who.route('/date_reported/<int:date_reported_id>/deaths_new/page/<int:page>')
@app_who.route('/date_reported/<int:date_reported_id>/deaths_new')
def url_who_date_reported_deaths_new(date_reported_id, page=1):
    date_reported = WhoDateReported.get_by_id(date_reported_id)
    page_info = ApplicationPage(
        "Date Reported: " + date_reported.date_reported,
        'WHO',
        "data of all reported countries for WHO date reported " + date_reported.date_reported + " "
    )
    try:
        page_data = WhoGlobalData.get_data_for_day_order_by_deaths_new(date_reported, page)
    except OperationalError:
        flash("No data in the database.")
        page_data = None
    return render_template(
        'who/date_reported/who_date_reported_one_deaths_new.html',
        who_date_reported=date_reported,
        page_data=page_data,
        page_info=page_info)


@app_who.route('/date_reported/<int:date_reported_id>/deaths_cumulative/page/<int:page>')
@app_who.route('/date_reported/<int:date_reported_id>/deaths_cumulative')
def url_who_date_reported_deaths_cumulative(date_reported_id, page=1):
    date_reported = WhoDateReported.get_by_id(date_reported_id)
    page_info = ApplicationPage(
        "Date Reported: " + date_reported.date_reported,
        'WHO',
        "data of all reported countries for WHO date reported " + date_reported.date_reported + " "
    )
    try:
        page_data = WhoGlobalData.get_data_for_day_order_by_deaths_cumulative(date_reported, page)
    except OperationalError:
        flash("No data in the database.")
        page_data = None
    return render_template(
        'who/date_reported/who_date_reported_one_deaths_cumulative.html',
        who_date_reported=date_reported,
        page_data=page_data,
        page_info=page_info)


@app_who.route('/region/all/page/<int:page>')
@app_who.route('/region/all')
def url_who_region_all(page=1):
    page_info = ApplicationPage('WHO', "Region", "All")
    try:
        page_data = WhoRegion.get_all_as_page(page)
    except OperationalError:
        flash("No regions in the database.")
        page_data = None
    return render_template(
        'who/region/who_region_all.html',
        page_data=page_data,
        page_info=page_info)


@app_who.route('/region/<int:region_id>/page/<int:page>')
@app_who.route('/region/<int:region_id>')
def url_who_region(region_id, page=1):
    who_region = None
    page_info = ApplicationPage("Countries", "WHO Region")
    try:
        who_region = WhoRegion.get_by_id(region_id)
        page_data = WhoCountry.get_who_countries_for_region(who_region, page)
        page_info.title = who_region.region
        page_info.subtitle = "WHO Region"
        page_info.subtitle_info = "Countries of WHO Region " + who_region.region
    except OperationalError:
        flash("No countries of that region in the database.")
        page_data = None
    return render_template(
        'who/region/who_region_one.html',
        who_region=who_region,
        page_data=page_data,
        page_info=page_info)


@app_who.route('/country/all/page/<int:page>')
@app_who.route('/country/all')
def url_who_country_all(page=1):
    page_info = ApplicationPage('WHO', "Countries", "All")
    try:
        page_data = WhoCountry.get_all_as_page(page)
    except OperationalError:
        flash("No regions in the database.")
        page_data = None
    return render_template(
        'who/country/who_country_all.html',
        page_data=page_data,
        page_info=page_info)


@app_who.route('/country/<int:country_id>/page/<int:page>')
@app_who.route('/country/<int:country_id>')
def url_who_country(country_id, page=1):
    who_country = WhoCountry.get_by_id(country_id)
    page_data = WhoGlobalData.get_data_for_country(who_country, page)
    page_info = ApplicationPage(who_country.country,
           "Country "+who_country.country_code,
           "Data per Day in Country "+who_country.country+" of WHO Region "+who_country.region.region)
    return render_template(
        'who/country/who_country_one.html',
        who_country=who_country,
        page_data=page_data,
        page_info=page_info)


@app_who.route('/country/<int:country_id>/cases_new/page/<int:page>')
@app_who.route('/country/<int:country_id>/cases_new')
def url_who_country_cases_new(country_id, page=1):
    who_country = WhoCountry.get_by_id(country_id)
    page_data = WhoGlobalData.get_data_for_country_order_by_cases_new(who_country, page)
    page_info = ApplicationPage(who_country.country,
           "Country "+who_country.country_code,
           "Data per Day in Country "+who_country.country+" of WHO Region "+who_country.region.region)
    return render_template(
        'who/country/who_country_one_cases_new.html',
        who_country=who_country,
        page_data=page_data,
        page_info=page_info)


@app_who.route('/country/<int:country_id>/cases_cumulative/page/<int:page>')
@app_who.route('/country/<int:country_id>/cases_cumulative')
def url_who_country_cases_cumulative(country_id, page=1):
    who_country = WhoCountry.get_by_id(country_id)
    page_data = WhoGlobalData.get_data_for_country_order_by_cases_cumulative(who_country, page)
    page_info = ApplicationPage(who_country.country,
           "Country "+who_country.country_code,
           "Data per Day in Country "+who_country.country+" of WHO Region "+who_country.region.region)
    return render_template(
        'who/country/who_country_one_cases_cumulative.html',
        who_country=who_country,
        page_data=page_data,
        page_info=page_info)


@app_who.route('/country/<int:country_id>/deaths_new/page/<int:page>')
@app_who.route('/country/<int:country_id>/deaths_new')
def url_who_country_deaths_new(country_id, page=1):
    who_country = WhoCountry.get_by_id(country_id)
    page_data = WhoGlobalData.get_data_for_country_order_by_deaths_new(who_country, page)
    page_info = ApplicationPage(who_country.country,
           "Country "+who_country.country_code,
           "Data per Day in Country "+who_country.country+" of WHO Region "+who_country.region.region)
    return render_template(
        'who/country/who_country_one_deaths_new.html',
        who_country=who_country,
        page_data=page_data,
        page_info=page_info)


@app_who.route('/country/<int:country_id>/deaths_cumulative/page/<int:page>')
@app_who.route('/country/<int:country_id>/deaths_cumulative')
def url_who_country_deaths_cumulative(country_id, page=1):
    who_country = WhoCountry.get_by_id(country_id)
    page_data = WhoGlobalData.get_data_for_country_order_by_deaths_cumulative(who_country, page)
    page_info = ApplicationPage(who_country.country,
           "Country "+who_country.country_code,
           "Data per Day in Country "+who_country.country+" of WHO Region "+who_country.region.region)
    return render_template(
        'who/country/who_country_one_deaths_cumulative.html',
        who_country=who_country,
        page_data=page_data,
        page_info=page_info)


@app_who.route('/germany/page/<int:page>')
@app_who.route('/germany')
def url_who_germany(page=1):
    page_info = ApplicationPage('WHO', "Germany")
    who_country_germany = WhoCountry.get_germany()
    if who_country_germany is None:
        flash('country: Germany not found in Database', category='error')
        return redirect(url_for('who.url_who_tasks'))
    page_data = WhoGlobalData.get_data_for_country(who_country_germany, page)
    return render_template(
        'who/country/who_country_germany.html',
        who_country=who_country_germany,
        page_data=page_data,
        page_info=page_info)
