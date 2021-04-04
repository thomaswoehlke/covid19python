from flask import render_template, redirect, url_for, flash, Blueprint
from sqlalchemy.exc import OperationalError
from celery import states
from celery.utils.log import get_task_logger
from flask_admin.contrib.sqla import ModelView

from database import app, admin, db
from covid19.blueprints.application.application_services import owid_service
from covid19.blueprints.application.application_workers import celery
from covid19.blueprints.owid.owid_model import OwidDateReported, OwidData, OwidContinent, OwidCountry
from covid19.blueprints.owid.owid_model_import import OwidImport
from covid19.blueprints.application.application_model_transient import ApplicationPage


app_owid = Blueprint('owid', __name__, template_folder='templates', url_prefix='/owid ')

admin.add_view(ModelView(OwidImport, db.session, category="OWID"))
admin.add_view(ModelView(OwidDateReported, db.session, category="OWID"))
admin.add_view(ModelView(OwidData, db.session, category="OWID"))

# def task_owid_download_only(self):
# def task_owid_import_only(self):
# def task_owid_update_dimension_tables_only(self):
# def task_owid_update_fact_table_incremental_only(self):
# def task_owid_update_fact_table_initial_only(self):
# def task_owid_update_fact_table_initial_only(self):
# def task_owid_update_star_schema_incremental(self):
# def task_owid_update_star_schema_initial(self):

#
# https://ourworldindata.org/grapher/covid-stringency-index?time=2020-01-26
# https://ourworldindata.org/grapher/biweekly-confirmed-covid-19-cases
#
# Biweekly change in confirmed COVID-19 cases
# Biweekly change in confirmed COVID-19 deaths
# Biweekly confirmed COVID-19 cases
# Biweekly confirmed COVID-19 cases per million people
# Biweekly confirmed COVID-19 deaths
# Biweekly confirmed COVID-19 deaths per million people
# COVID-19 Testing Policies
# COVID-19 Vaccination Policy
# COVID-19 death rate vs. Population density
# COVID-19 vaccine doses administered
# COVID-19 vaccine doses administered per 100 people
# COVID-19: Daily new confirmed cases vs cumulative cases
# COVID-19: Daily new confirmed cases vs cumulative cases
# COVID-19: Daily tests vs. Daily new confirmed cases
# COVID-19: Daily tests vs. Daily new confirmed cases per million
# COVID-19: Stringency Index
# Cancellation of public events during COVID-19 pandemic
# Case fatality rate of COVID-19 vs. Median age of the population
# Case fatality rate of the ongoing COVID-19 pandemic
# Case fatality rate vs. Tests per confirmed case
# Case fatality rate vs. Total confirmed COVID-19 deaths
# Confirmed COVID-19 deaths per million vs GDP per capita
# Confirmed COVID-19 deaths vs. Population density
# Cumulative COVID-19 tests, confirmed cases and deaths
# Cumulative COVID-19 tests, confirmed cases and deaths per million people
# Cumulative confirmed COVID-19 casesMap and country time-series
# Cumulative confirmed COVID-19 casesBy Region
# Cumulative confirmed COVID-19 cases per million vs. GDP per capita
# Cumulative confirmed COVID-19 deathsBy Region
# Cumulative confirmed COVID-19 deaths and cases
# Cumulative confirmed COVID-19 deaths vs. cases
# Daily COVID-19 tests
# Daily COVID-19 tests
# Daily COVID-19 tests per thousand people
# Daily COVID-19 tests per thousand peopleRolling 7-day average
# Daily COVID-19 vaccine doses administered
# Daily COVID-19 vaccine doses administered per 100 people
# Daily and total confirmed COVID-19 deaths
# Daily and total confirmed COVID-19 deaths per million
# Daily confirmed COVID-19 casesMap and country time-series
# Daily confirmed COVID-19 casesStacked area chart – by world region
# Daily confirmed COVID-19 cases and deaths
# Daily confirmed COVID-19 cases per million people
# Daily confirmed COVID-19 cases per million, 3-day rolling average
# Daily confirmed COVID-19 cases per million: which countries are bending the curve?Trajectories
# Daily confirmed COVID-19 cases, rolling 7-day average
# Daily confirmed COVID-19 cases: which countries are bending the curve?
# Daily confirmed COVID-19 deathsMap and time-series
# Daily confirmed COVID-19 deathsBy Region
# Daily confirmed COVID-19 deaths per million people
# Daily confirmed COVID-19 deaths per million, 3-day rolling average
# Daily confirmed COVID-19 deaths per million, rolling 7-day average
# Daily confirmed COVID-19 deaths per million: which countries are bending the curve?Trajectories
# Daily confirmed COVID-19 deaths, rolling 7-day average
# Daily confirmed COVID-19 deaths: which countries are bending the curve?Trajectories
# Daily new confirmed COVID-19 cases and deaths
# Daily new confirmed cases of COVID-19
# Daily new confirmed cases of COVID-19
# Daily new confirmed cases of COVID-19 per million people
# Daily new estimated COVID-19 infections from the ICL model
# Daily new estimated COVID-19 infections from the IHME model
# Daily new estimated COVID-19 infections from the LSHTM model
# Daily new estimated COVID-19 infections from the YYG model
# Daily new estimated infections of COVID-19
# Daily tests per thousand peopleSince total confirmed cases reached 1 per million
# Daily vs. Total confirmed COVID-19 cases
# Daily vs. Total confirmed COVID-19 cases per million people
# Daily vs. Total confirmed COVID-19 deaths per million
# Daily vs. cumulative confirmed deaths due to COVID-19
# Debt or contract relief during the COVID-19 pandemic
# Excess mortality during COVID-19: Deaths from all causes compared to previous years, all agesP-scores
# Excess mortality during COVID-19: Deaths from all causes compared to previous years, by ageP-scores
# Excess mortality during COVID-19: Number of deaths from all causes compared to previous yearsRaw death counts
# Face covering policies during the COVID-19 pandemic
# Government Response Stringency Index vs. Biweekly change in confirmed COVID-19 cases
# Grocery and pharmacy stores: How did the number of visitors change since the beginning of the pandemic?
# How did the number of visitors change since the beginning of the pandemic?
# Income support during the COVID-19 pandemic
# International travel controls during the COVID-19 pandemic
# Number of COVID-19 patients in ICU per million
# Number of COVID-19 patients in hospital
# Number of COVID-19 patients in hospital per million
# Number of COVID-19 patients in intensive care (ICU)
# Number of people fully vaccinated against COVID-19
# Number of people who received at least one dose of COVID-19 vaccine
# Number of tests per confirmed case vs. Total confirmed COVID-19 cases per million people
# Parks and outdoor spaces: How did the number of visitors change since the beginning of the pandemic?
# Per capita: COVID-19 tests vs. Confirmed deaths
# Per capita: tests for COVID-19 vs. Confirmed cases
# Public information campaigns on the COVID-19 pandemic
# Public transport closures during the COVID-19 pandemic
# Residential areas: How did the time spent at home change since the beginning of the pandemic?
# Restrictions on internal movement during the COVID-19 pandemic
# Restrictions on public gatherings in the COVID-19 pandemic
# Retail and recreation: How did the number of visitors change since the beginning of the pandemic?
# School closures during the COVID-19 pandemic
# Share of COVID-19 tests that were positiveOver time, since 5th death was confirmed
# Share of people who received at least one dose of COVID-19 vaccine
# Share of the population fully vaccinated against COVID-19
# Share of total COVID-19 tests that were positive
# Share who would get a COVID-19 vaccine if it was available to them this week
# Stay-at-home requirements during the COVID-19 pandemic
# Tests conducted per new confirmed case of COVID-19
# Tests per confirmed case – total vs. Case fatality rate
# Tests per thousand since the 100th confirmed case of COVID-19
# Tests per thousand since the 5th confirmed death due to COVID-19
# The share of COVID-19 tests that are positive
# Total COVID-19 testsLine chart
# Total COVID-19 testsMap chart
# Total COVID-19 tests conducted vs. Confirmed cases
# Total COVID-19 tests conducted vs. Confirmed casesPositive rate comparison
# Total COVID-19 tests conducted vs. Confirmed cases per million
# Total COVID-19 tests for each confirmed case
# Total COVID-19 tests for each confirmed caseBar chart
# Total COVID-19 tests per 1,000 peopleLine chart
# Total COVID-19 tests per 1,000 peopleMap chart
# Total COVID-19 tests per 1,000 peopleBar chart
# Total COVID-19 tests per 1,000 vs. GDP per capita
# Total COVID-19 tests per 1,000: how are testing rates changing?Since daily new confirmed deaths due to COVID-19 reached 0.1 per million
# Total COVID-19 tests per 1,000: how are testing rates changing?Since daily new confirmed deaths due to COVID-19 reached 0.1 per million
# Total and daily confirmed COVID-19 cases
# Total and daily confirmed COVID-19 cases per million people
# Total confirmed COVID-19 casesBy Income Group
# Total confirmed COVID-19 cases per million peopleMap and country time-series
# Total confirmed COVID-19 cases per million: how rapidly are they increasing?Trajectories
# Total confirmed COVID-19 cases vs. deaths per million
# Total confirmed COVID-19 cases, by source
# Total confirmed COVID-19 cases: how rapidly are they increasing?Trajectories
# Total confirmed COVID-19 deathsMap and country time-series
# Total confirmed COVID-19 deathsBy Income Group
# Total confirmed COVID-19 deaths and cases per million people
# Total confirmed COVID-19 deaths per million people
# Total confirmed COVID-19 deaths per million vs GDP per capita
# Total confirmed COVID-19 deaths per million: how rapidly are they increasing?
# Total confirmed COVID-19 deaths: how rapidly are they increasing?Trajectories
# Total confirmed deaths due to COVID-19 vs. Population
# Total confirmed deaths from COVID-19, by source
# Total number of COVID-19 tests per confirmed case
# Transit stations: How did the number of visitors change since the beginning of the pandemic?
# Week by week change in confirmed COVID-19 cases
# Week by week change of confirmed COVID-19 cases vs. GDP per capita
# Week by week change of confirmed COVID-19 deaths
# Week by week change of confirmed COVID-19 deaths vs. GDP per capita
# Weekly case growth rate vs. daily case rate
# Weekly confirmed COVID-19 cases
# Weekly confirmed COVID-19 cases per million people
# Weekly confirmed COVID-19 deaths
# Weekly confirmed COVID-19 deaths per million people
# Weekly death growth rate vs. daily death rate
# Weekly new ICU admissions for COVID-19
# Weekly new ICU admissions for COVID-19 per million
# Weekly new hospital admissions for COVID-19
# Weekly new hospital admissions for COVID-19 per million
# Which countries do COVID-19 contact tracing?
# Workplace closures during the COVID-19 pandemic
# Workplaces: How did the number of visitors change since the beginning of the pandemic?



# ---------------------------------------------------------------------------------------------------------------
#  Url Routes Frontend
# ---------------------------------------------------------------------------------------------------------------


@app_owid.route('/info')
def url_owid_info():
    page_info = ApplicationPage('OWID', "Info")
    return render_template(
        'owid/owid_info.html',
        page_info=page_info)


@app_owid.route('/tasks')
def url_owid_tasks():
    page_info = ApplicationPage('OWID', "Tasks")
    return render_template(
        'owid/owid_tasks.html',
        page_info=page_info)


@app_owid.route('/test/page/<int:page>')
@app_owid.route('/test')
def url_owid_test(page=1):
    page_info = ApplicationPage('OWID', "Test")
    try:
        page_data = OwidImport.get_continents(page)
    except OperationalError:
        flash(message="No data in the database.", category="error")
        page_data = None
    return render_template(
        'owid/owid_test.html',
        page_data=page_data,
        page_info=page_info)


@app_owid.route('/imported/page/<int:page>')
@app_owid.route('/imported')
def url_owid_imported(page=1):
    page_info = ApplicationPage('OWID', "Last Import")
    try:
        page_data = OwidImport.get_all_as_page(page)
    except OperationalError:
        flash("No data in the database.")
        page_data = None
    return render_template(
        'owid/owid_imported.html',
        page_data=page_data,
        page_info=page_info)


@app_owid.route('/date_reported/all/page/<int:page>')
@app_owid.route('/date_reported/all')
def url_owid_date_reported_all(page: int = 1):
    page_info = ApplicationPage('OWID', "Date Reported", "All")
    try:
        page_data = OwidDateReported.get_all_as_page(page)
    except OperationalError:
        flash("No regions in the database.")
        page_data = None
    return render_template(
        'owid/date_reported/owid_date_reported_all.html',
        page_data=page_data,
        page_info=page_info)


@app_owid.route('/date_reported/<int:date_reported_id>/page/<int:page>')
@app_owid.route('/date_reported/<int:date_reported_id>')
def url_owid_date_reported(date_reported_id: int, page: int = 1):
    date_reported = OwidDateReported.get_by_id(date_reported_id)
    page_info = ApplicationPage(
        "Date Reported: " + date_reported.date_reported,
        'OWID',
        "data of all reported countries for OWID date reported " + date_reported.date_reported + " "
    )
    try:
        page_data = OwidData.get_data_for_day(date_reported, page)
    except OperationalError:
        flash("No data in the database.")
        page_data = None
    return render_template(
        'owid/date_reported/owid_date_reported_one.html',
        owid_date_reported=date_reported,
        page_data=page_data,
        page_info=page_info)


@app_owid.route('/date_reported/<int:date_reported_id>/cases_new/page/<int:page>')
@app_owid.route('/date_reported/<int:date_reported_id>/cases_new')
def url_owid_date_reported_cases_new(date_reported_id: int, page: int = 1):
    date_reported = OwidDateReported.get_by_id(date_reported_id)
    page_info = ApplicationPage(
        "Date Reported: " + date_reported.date_reported,
        'OWID',
        "data of all reported countries for OWID date reported " + date_reported.date_reported + " "
    )
    try:
        page_data = OwidData.get_data_for_day_order_by_cases_new(date_reported, page)
    except OperationalError:
        flash("No data in the database.")
        page_data = None
    return render_template(
        'owid/date_reported/owid_date_reported_one_cases_new.html',
        owid_date_reported=date_reported,
        page_data=page_data,
        page_info=page_info)


@app_owid.route('/date_reported/<int:date_reported_id>/cases_cumulative/page/<int:page>')
@app_owid.route('/date_reported/<int:date_reported_id>/cases_cumulative')
def url_owid_date_reported_cases_cumulative(date_reported_id: int, page: int = 1):
    date_reported = OwidDateReported.get_by_id(date_reported_id)
    page_info = ApplicationPage(
        "Date Reported: " + date_reported.date_reported,
        'OWID',
        "data of all reported countries for OWID date reported " + date_reported.date_reported + " "
    )
    try:
        page_data = OwidData.get_data_for_day_order_by_cases_cumulative(date_reported, page)
    except OperationalError:
        flash("No data in the database.")
        page_data = None
    return render_template(
        'owid/date_reported/owid_date_reported_one_cases_cumulative.html',
        owid_date_reported=date_reported,
        page_data=page_data,
        page_info=page_info)


@app_owid.route('/date_reported/<int:date_reported_id>/deaths_new/page/<int:page>')
@app_owid.route('/date_reported/<int:date_reported_id>/deaths_new')
def url_owid_date_reported_deaths_new(date_reported_id: int, page: int = 1):
    date_reported = OwidDateReported.get_by_id(date_reported_id)
    page_info = ApplicationPage(
        "Date Reported: " + date_reported.date_reported,
        'OWID',
        "data of all reported countries for OWID date reported " + date_reported.date_reported + " "
    )
    try:
        page_data = OwidData.get_data_for_day_order_by_deaths_new(date_reported, page)
    except OperationalError:
        flash("No data in the database.")
        page_data = None
    return render_template(
        'owid/date_reported/owid_date_reported_one_deaths_new.html',
        owid_date_reported=date_reported,
        page_data=page_data,
        page_info=page_info)


@app_owid.route('/date_reported/<int:date_reported_id>/deaths_cumulative/page/<int:page>')
@app_owid.route('/date_reported/<int:date_reported_id>/deaths_cumulative')
def url_owid_date_reported_deaths_cumulative(date_reported_id: int, page: int = 1):
    date_reported = OwidDateReported.get_by_id(date_reported_id)
    page_info = ApplicationPage(
        "Date Reported: " + date_reported.date_reported,
        'OWID',
        "data of all reported countries for OWID date reported " + date_reported.date_reported + " "
    )
    try:
        page_data = OwidData.get_data_for_day_order_by_deaths_cumulative(date_reported, page)
    except OperationalError:
        flash("No data in the database.")
        page_data = None
    return render_template(
        'owid/date_reported/owid_date_reported_one_deaths_cumulative.html',
        owid_date_reported=date_reported,
        page_data=page_data,
        page_info=page_info)


@app_owid.route('/continent/all/page/<int:page>')
@app_owid.route('/continent/all')
def url_owid_continent_all(page: int = 1):
    page_info = ApplicationPage(
        "Continents "
        'OWID'
    )
    try:
        page_data = OwidContinent.get_all_as_page(page)
    except OperationalError:
        flash("No data in the database.")
        page_data = None
    return render_template(
        'owid/continent/owid_continent_all.html',
        page_data=page_data,
        page_info=page_info)


@app_owid.route('/continent/<int:continent_id>/page/<int:page>')
@app_owid.route('/continent/<int:continent_id>')
def url_owid_continent_one(continent_id: int, page: int = 1):
    owid_continent_one = OwidContinent.get_by_id(continent_id)
    page_info = ApplicationPage(
        "continent: " + owid_continent_one.region,
        'OWID',
        "countries for OWID continent " + owid_continent_one.region + " "
    )
    try:
        page_data = OwidCountry.get_countries_for_continent(owid_continent_one, page)
    except OperationalError:
        flash("No data in the database.")
        page_data = None
    return render_template(
        'owid/continent/owid_continent_one.html',
        owid_continent=owid_continent_one,
        page_data=page_data,
        page_info=page_info)


@app_owid.route('/country/all/page/<int:page>')
@app_owid.route('/country/all')
def url_owid_country_all(page: int = 1):
    page_info = ApplicationPage(
        "Continents "
        'OWID'
    )
    try:
        page_data = OwidContinent.get_all_as_page(page)
    except OperationalError:
        flash("No data in the database.")
        page_data = None
    return render_template(
        'owid/country/owid_country_all.html',
        page_data=page_data,
        page_info=page_info)


@app_owid.route('/country/<int:country_id>/page/<int:page>')
@app_owid.route('/country/<int:country_id>')
def url_owid_country_one(country_id: int, page: int = 1):
    owid_country_one = OwidCountry.get_by_id(country_id)
    page_info = ApplicationPage(
        "continent: " + owid_country_one.location,
        'OWID',
        "countries for OWID continent " + owid_country_one.region + " "
    )
    try:
        page_data = OwidData.get_data_for_country(owid_country_one, page)
    except OperationalError:
        flash("No data in the database.")
        page_data = None
    return render_template(
        'owid/country/owid_country_one.html',
        owid_country=owid_country_one,
        page_data=page_data,
        page_info=page_info)


# ----------------------------------------------------------------------------------------------------------------
#  Celery TASKS
# ----------------------------------------------------------------------------------------------------------------


@celery.task(bind=True)
def task_owid_download_only(self):
    logger = get_task_logger(__name__)
    self.update_state(state=states.STARTED)
    logger.info("------------------------------------------------------------")
    logger.info(" Received: task_owid_download_only [OK] ")
    logger.info("------------------------------------------------------------")
    owid_service.run_download_only()
    self.update_state(state=states.SUCCESS)
    result = "OK (task_owid_download_only)"
    return result


@celery.task(bind=True)
def task_owid_import_only(self):
    logger = get_task_logger(__name__)
    self.update_state(state=states.STARTED)
    logger.info("------------------------------------------------------------")
    logger.info(" Received: task_owid_import_only [OK] ")
    logger.info("------------------------------------------------------------")
    owid_service.run_import_only()
    self.update_state(state=states.SUCCESS)
    result = "OK (task_owid_import_only)"
    return result


@celery.task(bind=True)
def task_owid_update_dimension_tables_only(self):
    logger = get_task_logger(__name__)
    self.update_state(state=states.STARTED)
    logger.info("------------------------------------------------------------")
    logger.info(" Received: task_owid_update_dimension_tables_only [OK] ")
    logger.info("------------------------------------------------------------")
    owid_service.run_update_dimension_tables_only()
    self.update_state(state=states.SUCCESS)
    result = "OK (task_owid_update_dimension_tables_only)"
    return result


@celery.task(bind=True)
def task_owid_update_fact_table_incremental_only(self):
    logger = get_task_logger(__name__)
    self.update_state(state=states.STARTED)
    logger.info("------------------------------------------------------------")
    logger.info(" Received: task_owid_update_fact_table_incremental_only [OK] ")
    logger.info("------------------------------------------------------------")
    owid_service.run_update_fact_table_incremental_only()
    self.update_state(state=states.SUCCESS)
    result = "OK (task_owid_update_dimension_tables_only)"
    return result


@celery.task(bind=True)
def task_owid_update_fact_table_initial_only(self):
    logger = get_task_logger(__name__)
    self.update_state(state=states.STARTED)
    logger.info("------------------------------------------------------------")
    logger.info(" Received: task_owid_update_fact_table_initial_only [OK] ")
    logger.info("------------------------------------------------------------")
    owid_service.run_update_fact_table_initial_only()
    self.update_state(state=states.SUCCESS)
    result = "OK (task_owid_update_fact_table_initial_only)"
    return result


@celery.task(bind=True)
def task_owid_update_star_schema_incremental(self):
    logger = get_task_logger(__name__)
    self.update_state(state=states.STARTED)
    logger.info("------------------------------------------------------------")
    logger.info(" Received: task_owid_update_star_schema_incremental [OK] ")
    logger.info("------------------------------------------------------------")
    owid_service.run_update_star_schema_incremental()
    self.update_state(state=states.SUCCESS)
    result = "OK (task_owid_update_star_schema_incremental)"
    return result


@celery.task(bind=True)
def task_owid_update_star_schema_initial(self):
    logger = get_task_logger(__name__)
    self.update_state(state=states.STARTED)
    logger.info("------------------------------------------------------------")
    logger.info(" Received: task_owid_update_star_schema_initial [OK] ")
    logger.info("------------------------------------------------------------")
    owid_service.run_update_star_schema_initial()
    self.update_state(state=states.SUCCESS)
    result = "OK (task_owid_update_star_schema_incremental)"
    return result


# ----------------------------------------------------------------------------------------------------------------
#  URL Routes for Celery TASKS
# ----------------------------------------------------------------------------------------------------------------


@app_owid.route('/task/download/only')
def url_task_owid_download_only():
    app.logger.info("url_owid_task_download_only [start]")
    owid_service.run_download_only()
    flash("owid_service.run_download_only ok")
    app.logger.info("url_owid_task_download_only [done]")
    return redirect(url_for('owid.url_owid_tasks'))


@app_owid.route('/task/import/only')
def url_task_owid_import_only():
    app.logger.info("url_owid_update_run [start]")
    task_owid_import_only.apply_async()
    flash("owid_service.run_update started")
    flash(message="long running background task started", category="warning")
    app.logger.info("url_owid_update_run [done]")
    return redirect(url_for('owid.url_owid_tasks'))


@app_owid.route('/task/update/dimension-tables/only')
def url_task_owid_update_dimension_tables_only():
    app.logger.info("url_task_owid_update_dimension_tables_only [start]")
    task_owid_update_dimension_tables_only.apply_async()
    flash("task_owid_update_dimension_tables_only started")
    flash(message="long running background task started", category="warning")
    app.logger.info("url_task_owid_update_dimension_tables_only [done]")
    return redirect(url_for('owid.url_owid_tasks'))


@app_owid.route('/task/update/fact-table/incremental/only')
def url_task_owid_update_fact_table_incremental_only():
    app.logger.info("url_task_owid_update_fact_table_incremental_only [start]")
    task_owid_update_fact_table_incremental_only.apply_async()
    flash("task_owid_update_fact_table_incremental_only started")
    flash(message="long running background task started", category="warning")
    app.logger.info("url_task_owid_update_fact_table_incremental_only [done]")
    return redirect(url_for('owid.url_owid_tasks'))


@app_owid.route('/task/update/fact-table/initial/only')
def url_task_owid_update_fact_table_initial_only():
    app.logger.info("url_task_owid_update_fact_table_initial_only [start]")
    task_owid_update_fact_table_initial_only.apply_async()
    flash("task_owid_update_fact_table_initial_only started")
    flash(message="long running background task started", category="warning")
    app.logger.info("url_owid_task_update_full [done]")
    return redirect(url_for('owid.url_owid_tasks'))


@app_owid.route('/task/update/star_schema/initial')
def url_task_owid_update_star_schema_initial():
    app.logger.info("url_owid_task_update_full [start]")
    owid_service.run_download_only()
    flash("owid_service.service_download.download_file ok")
    task_owid_update_star_schema_initial.apply_async()
    flash(message="long running background task started", category="warning")
    app.logger.info("url_owid_task_update_full [done]")
    return redirect(url_for('owid.url_owid_tasks'))


@app_owid.route('/task/update/star_schema/incremental')
def url_task_owid_update_star_schema_incremental():
    app.logger.info("url_task_owid_update_star_schema_incremental [start]")
    owid_service.run_download_only()
    flash("owid_service.service_download.download_file ok")
    task_owid_update_star_schema_incremental.apply_async()
    flash("task_owid_run_update_full started")
    flash(message="long running background task started", category="warning")
    app.logger.info("url_task_owid_update_star_schema_incremental [done]")
    return redirect(url_for('owid.url_owid_tasks'))
