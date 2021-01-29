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
