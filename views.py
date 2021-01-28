from flask import render_template, redirect, url_for, flash
from sqlalchemy.exc import OperationalError
from celery import states
from celery.utils.log import get_task_logger

from database import app
from services import who_service, europe_service, vaccination_service, admin_service, rki_service
from workers import celery

from app.oodm.who.who_model import WhoGlobalDataImportTable
from app.oodm.who.who_model import WhoRegion, WhoCountry, WhoDateReported, WhoGlobalData
from app.oodm.europe.europe_model import EuropeDataImportTable, EuropeDateReported, EuropeContinent
from app.oodm.europe.europe_model import EuropeCountry, EuropeData
from app.oodm.common.common_model_transient import ApplicationPage
from app.oodm.vaccination.vaccination_model import VaccinationGermanyTimeline

drop_and_create_data_again = True


############################################################################################
#
# WEB
#
@app.route('/home')
def url_home():
    page_info = ApplicationPage('Home', "Covid19 Data")
    return render_template(
        'page_home.html',
        page_info=page_info)


@app.route('/')
def url_root():
    return redirect(url_for('url_home'))

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


##################################################################################################################
#
# Europe
#
##################################################################################################################


@celery.task(bind=True)
def task_europe_update_initial(self):
    logger = get_task_logger(__name__)
    self.update_state(state=states.STARTED)
    logger.info("------------------------------------------------------------")
    logger.info(" Received: europe_update_task [OK] ")
    logger.info("------------------------------------------------------------")
    europe_service.run_update_initial()
    self.update_state(state=states.SUCCESS)
    result = "OK (task_europe_update_initial)"
    return result


@celery.task(bind=True)
def task_europe_update_short(self):
    logger = get_task_logger(__name__)
    self.update_state(state=states.STARTED)
    logger.info("------------------------------------------------------------")
    logger.info(" Received: task_europe_update_short [OK] ")
    logger.info("------------------------------------------------------------")
    europe_service.run_update_short()
    self.update_state(state=states.SUCCESS)
    result = "OK (task_europe_update_short)"
    return result


@app.route('/europe/info')
def url_europe_info():
    page_info = ApplicationPage('Europe', "Info")
    return render_template(
        'europe/europe_info.html',
        title='Europe',
        page_info=page_info)


@app.route('/europe/tasks')
def url_europe_tasks():
    page_info = ApplicationPage('Europe', "Tasks")
    return render_template(
        'europe/europe_tasks.html',
        title='Europe Tasks',
        page_info=page_info)


@app.route('/europe/update/initial')
def europe_update_data():
    europe_service.download()
    task_europe_update_initial.apply_async()
    flash("europe_service.run_update started")
    return redirect(url_for('url_home'))


@app.route('/europe/imported/page/<int:page>')
@app.route('/europe/imported')
def url_europe_data_imported(page=1):
    page_info = ApplicationPage('Europe', "Last Import")
    page_data = EuropeDataImportTable.get_all_as_page(page)
    return render_template(
        'europe/europe_imported.html',
        page_data=page_data,
        page_info=page_info)


@app.route('/europe/date_reported/all/page/<int:page>')
@app.route('/europe/date_reported/all')
def url_europe_date_reported_all(page=1):
    page_info = ApplicationPage('Europe', "date_reported")
    page_data = EuropeDateReported.get_all_as_page(page)
    return render_template(
        'europe/date_reported/europe_date_reported_all.html',
        page_data=page_data,
        page_info=page_info)


@app.route('/europe/date_reported/<int:europe_date_reported_id>/page/<int:page>')
@app.route('/europe/date_reported/<int:europe_date_reported_id>')
@app.route('/europe/date_reported/notification_rate/<int:europe_date_reported_id>/page/<int:page>')
@app.route('/europe/date_reported/notification_rate/<int:europe_date_reported_id>')
def url_europe_date_reported_one_notification_rate(europe_date_reported_id, page=1):
    page_info = ApplicationPage('Europe', "date_reported")
    europe_date_reported = EuropeDateReported.get_by_id(europe_date_reported_id)
    page_data = EuropeData.find_by_date_reported_notification_rate(europe_date_reported, page)
    return render_template(
        'europe/date_reported/europe_date_reported_one_notification_rate.html',
        europe_date_reported=europe_date_reported,
        page_data=page_data,
        page_info=page_info)


@app.route('/europe/date_reported/deaths_weekly/<int:europe_date_reported_id>/page/<int:page>')
@app.route('/europe/date_reported/deaths_weekly/<int:europe_date_reported_id>')
def url_europe_date_reported_one_deaths_weekly(europe_date_reported_id, page=1):
    page_info = ApplicationPage('Europe', "date_reported")
    europe_date_reported = EuropeDateReported.get_by_id(europe_date_reported_id)
    page_data = EuropeData.find_by_date_reported_deaths_weekly(europe_date_reported, page)
    return render_template(
        'europe/date_reported/europe_date_reported_one_deaths_weekly.html',
        europe_date_reported=europe_date_reported,
        page_data=page_data,
        page_info=page_info)


@app.route('/europe/date_reported/cases_weekly/<int:europe_date_reported_id>/page/<int:page>')
@app.route('/europe/date_reported/cases_weekly/<int:europe_date_reported_id>')
def url_europe_date_reported_one_cases_weekly(europe_date_reported_id, page=1):
    page_info = ApplicationPage('Europe', "date_reported")
    europe_date_reported = EuropeDateReported.get_by_id(europe_date_reported_id)
    page_data = EuropeData.find_by_date_reported_cases_weekly(europe_date_reported, page)
    return render_template(
        'europe/date_reported/europe_date_reported_one_cases_weekly.html',
        europe_date_reported=europe_date_reported,
        page_data=page_data,
        page_info=page_info)


@app.route('/europe/continent/all/page/<int:page>')
@app.route('/europe/continent/all')
def url_europe_continent_all(page=1):
    page_info = ApplicationPage('Europe', "continent")
    page_data = EuropeContinent.get_all_as_page(page)
    return render_template(
        'europe/continent/europe_continent_all.html',
        page_data=page_data,
        page_info=page_info)


@app.route('/europe/continent/<int:continent_id>/page/<int:page>')
@app.route('/europe/continent/<int:continent_id>')
def url_europe_continent_one(continent_id, page=1):
    page_info = ApplicationPage('Europe', "continent")
    continent = EuropeContinent.get_by_id(continent_id)
    page_data = EuropeCountry.find_by_continent(continent, page)
    return render_template(
        'europe/continent/europe_continent_one.html',
        continent=continent,
        page_data=page_data,
        page_info=page_info)


@app.route('/europe/country/all/page/<int:page>')
@app.route('/europe/country/all')
def url_europe_country_all(page=1):
    page_info = ApplicationPage('Europe', "country")
    page_data = EuropeCountry.get_all_as_page(page)
    return render_template(
        'europe/country/europe_country_all.html',
        page_data=page_data,
        page_info=page_info)


@app.route('/europe/country/<int:country_id>/page/<int:page>')
@app.route('/europe/country/<int:country_id>')
def url_europe_country_one(country_id, page=1):
    page_info = ApplicationPage('Europe', "country")
    europe_country = EuropeCountry.get_by_id(country_id)
    page_data = EuropeData.find_by_country(europe_country, page)
    return render_template(
        'europe/country/europe_country_one.html',
        europe_country=europe_country,
        page_data=page_data,
        page_info=page_info)


@app.route('/europe/country/germany/page/<int:page>')
@app.route('/europe/country/germany')
def url_europe_country_germany(page=1):
    page_info = ApplicationPage('Europe', "country: Germany")
    europe_country = EuropeCountry.get_germany()
    if europe_country is None:
        flash('country: Germany not found in Database', category='error')
        return redirect(url_for('url_europe_tasks'))
    page_data = EuropeData.find_by_country(europe_country, page)
    return render_template(
        'europe/country/europe_country_germany.html',
        europe_country=europe_country,
        page_data=page_data,
        page_info=page_info)


##################################################################################################################
#
# Vaccination
#
##################################################################################################################


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


@app.route('/vaccination/info')
def url_vaccination_info():
    page_info = ApplicationPage('Vaccination', "Info")
    return render_template(
        'vaccination/vaccination_info.html',
        page_info=page_info)


@app.route('/vaccination/tasks')
def url_vaccination_tasks():
    page_info = ApplicationPage('Vaccination', "Tasks")
    return render_template(
        'vaccination/vaccination_tasks.html',
        page_info=page_info)


@app.route('/vaccination/update/initial')
def url_vaccination_update_data():
    vaccination_service.run_download()
    flash("vaccination_service.run_download done")
    task_vaccination_update_initial.apply_async()
    flash("vaccination_service.run_update started")
    return redirect(url_for('url_vaccination_tasks'))


@app.route('/vaccination/timeline/germany/page/<int:page>')
@app.route('/vaccination/timeline/germany')
def url_vaccination_timeline_germany(page=1):
    page_info = ApplicationPage('Vaccination', "Germany Timeline")
    page_data = VaccinationGermanyTimeline.get_all_as_page(page)
    return render_template(
        'vaccination/vaccination_timeline_germany.html',
        page_data=page_data,
        page_info=page_info)


##################################################################################################################
#
# RKI
#
##################################################################################################################
@app.route('/rki/info')
def url_rki_info():
    page_info = ApplicationPage('RKI', "Info")
    return render_template(
        'rki/rki_info.html',
        page_info=page_info)


@app.route('/rki/tasks')
def url_rki_tasks():
    page_info = ApplicationPage('RKI', "Tasks")
    return render_template(
        'rki/rki_tasks.html',
        page_info=page_info)


@app.route('/rki/imported/page/<int:page>')
@app.route('/rki/imported')
def url_rki_imported(page=1):
    page_info = ApplicationPage('RKI', "Last Import")
    try:
        page_data = WhoGlobalDataImportTable.get_all_as_page(page)
    except OperationalError:
        flash("No data in the database.")
        page_data = None
    return render_template(
        'rki/rki_imported.html',
        page_data=page_data,
        page_info=page_info)


##################################################################################################################
#
# NRW
#
##################################################################################################################
@app.route('/nrw/info')
def url_nrw_info():
    page_info = ApplicationPage('NRW', "Info")
    return render_template(
        'nrw/nrw_info.html',
        page_info=page_info)


@app.route('/nrw/tasks')
def url_nrw_tasks():
    page_info = ApplicationPage('NRW', "Tasks")
    return render_template(
        'nrw/nrw_tasks.html',
        page_info=page_info)


@app.route('/nrw/imported/<int:page>')
@app.route('/nrw/imported')
def url_nrw_imported(page=1):
    page_info = ApplicationPage('NRW', "Last Import")
    try:
        who_imported_all = WhoGlobalDataImportTable.get_all_as_page(page)
    except OperationalError:
        flash("No data in the database.")
        who_imported_all = None
    return render_template(
        'nrw/nrw_imported.html',
        page_data=who_imported_all,
        page_info=page_info)


@app.route('/nrw/bochum/<int:page>')
@app.route('/nrw/bochum')
def url_nrw_bochum(page=1):
    page_info = ApplicationPage('NRW', "Bochum")
    who_country = WhoCountry.get_germany()
    list_who_global_data = WhoGlobalData.get_data_for_country(who_country, page)
    return render_template(
        'nrw/nrw_stadt.html',
        who_country=who_country,
        page_data=list_who_global_data,
        page_info=page_info)


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
