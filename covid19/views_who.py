from flask import render_template, redirect, url_for, flash
from sqlalchemy.exc import OperationalError
from celery import states
from celery.utils.log import get_task_logger

from database import app
from covid19.services import who_service, europe_service, vaccination_service, admin_service, rki_service
from covid19.workers import celery

from covid19.oodm.who.who_model import WhoGlobalDataImportTable
from covid19.oodm.who.who_model import WhoRegion, WhoCountry, WhoDateReported, WhoGlobalData
from covid19.oodm.europe.europe_model import EuropeDataImportTable, EuropeDateReported, EuropeContinent
from covid19.oodm.europe.europe_model import EuropeCountry, EuropeData
from covid19.oodm.common.common_model_transient import ApplicationPage
from covid19.oodm.vaccination.vaccination_model import VaccinationGermanyTimeline


##################################################################################################################
#
# WHO
#
##################################################################################################################


@celery.task(bind=True)
def task_who_run_update(self, import_file=True):
    logger = get_task_logger(__name__)
    self.update_state(state=states.STARTED)
    logger.info("------------------------------------------------------------")
    logger.info(" Received: task_who_run_update [OK] ")
    logger.info("------------------------------------------------------------")
    who_service.run_update(import_file)
    self.update_state(state=states.SUCCESS)
    result = "OK (task_who_run_update)"
    return result


@celery.task(bind=True)
def task_who_update_short(self):
    logger = get_task_logger(__name__)
    self.update_state(state=states.STARTED)
    logger.info("------------------------------------------------------------")
    logger.info(" Received: task_who_update_short [OK] ")
    logger.info("------------------------------------------------------------")
    who_service.run_update_short()
    self.update_state(state=states.SUCCESS)
    result = "OK (task_who_update_short)"
    return result


@celery.task(bind=True)
def task_who_update_initial(self):
    logger = get_task_logger(__name__)
    self.update_state(state=states.STARTED)
    logger.info("------------------------------------------------------------")
    logger.info(" Received: task_who_update_initial [OK] ")
    logger.info("------------------------------------------------------------")
    who_service.run_update_initial()
    self.update_state(state=states.SUCCESS)
    result = "OK (task_who_update_initial)"
    return result


@app.route('/who/info')
def url_who_info():
    page_info = ApplicationPage('WHO', "Info")
    return render_template(
        'who/who_info.html',
        page_info=page_info)


@app.route('/who/tasks')
def url_who_tasks():
    page_info = ApplicationPage('WHO', "Tasks")
    return render_template(
        'who/who_tasks.html',
        page_info=page_info)


@app.route('/who/imported/page/<int:page>')
@app.route('/who/imported')
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


@app.route('/who/date_reported/all/page/<int:page>')
@app.route('/who/date_reported/all')
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


@app.route('/who/date_reported/<int:date_reported_id>/page/<int:page>')
@app.route('/who/date_reported/<int:date_reported_id>')
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


@app.route('/who/date_reported/<int:date_reported_id>/cases_new/page/<int:page>')
@app.route('/who/date_reported/<int:date_reported_id>/cases_new')
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


@app.route('/who/date_reported/<int:date_reported_id>/cases_cumulative/page/<int:page>')
@app.route('/who/date_reported/<int:date_reported_id>/cases_cumulative')
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


@app.route('/who/date_reported/<int:date_reported_id>/deaths_new/page/<int:page>')
@app.route('/who/date_reported/<int:date_reported_id>/deaths_new')
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


@app.route('/who/date_reported/<int:date_reported_id>/deaths_cumulative/page/<int:page>')
@app.route('/who/date_reported/<int:date_reported_id>/deaths_cumulative')
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


@app.route('/who/region/all/page/<int:page>')
@app.route('/who/region/all')
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


@app.route('/who/region/<int:region_id>/page/<int:page>')
@app.route('/who/region/<int:region_id>')
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


@app.route('/who/country/all/page/<int:page>')
@app.route('/who/country/all')
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


@app.route('/who/country/<int:country_id>/page/<int:page>')
@app.route('/who/country/<int:country_id>')
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


@app.route('/who/country/<int:country_id>/cases_new/page/<int:page>')
@app.route('/who/country/<int:country_id>/cases_new')
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


@app.route('/who/country/<int:country_id>/cases_cumulative/page/<int:page>')
@app.route('/who/country/<int:country_id>/cases_cumulative')
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


@app.route('/who/country/<int:country_id>/deaths_new/page/<int:page>')
@app.route('/who/country/<int:country_id>/deaths_new')
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


@app.route('/who/country/<int:country_id>/deaths_cumulative/page/<int:page>')
@app.route('/who/country/<int:country_id>/deaths_cumulative')
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


@app.route('/who/germany/page/<int:page>')
@app.route('/who/germany')
def url_who_germany(page=1):
    page_info = ApplicationPage('WHO', "Germany")
    who_country_germany = WhoCountry.get_germany()
    if who_country_germany is None:
        flash('country: Germany not found in Database', category='error')
        return redirect(url_for('url_who_tasks'))
    page_data = WhoGlobalData.get_data_for_country(who_country_germany, page)
    return render_template(
        'who/country/who_country_germany.html',
        who_country=who_country_germany,
        page_data=page_data,
        page_info=page_info)


@app.route('/who/update')
def url_who_update_run():
    app.logger.info("url_who_update_run [start]")
    who_service.who_service_download.download_file()
    task_who_run_update.apply_async()
    flash("who_service.run_update started")
    flash(message="long running background task started", category="warning")
    app.logger.info("url_who_update_run [done]")
    return redirect(url_for('url_home'))


@app.route('/who/update/short')
def url_who_update_short_run():
    who_service.who_service_download.download_file()
    task_who_update_short.apply_async()
    flash("who_service.run_update_short started")
    flash(message="long running background task started", category="warning")
    return redirect(url_for('url_home'))


@app.route('/who/update/initial')
def url_who_update_initial_run():
    who_service.who_service_download.download_file()
    task_who_update_initial.apply_async()
    flash("who_service.run_update_short started")
    flash(message="long running background task started", category="warning")
    return redirect(url_for('url_home'))
