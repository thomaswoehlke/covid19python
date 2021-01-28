from flask import render_template, redirect, url_for, flash
from sqlalchemy.exc import OperationalError
from celery import states
from celery.utils.log import get_task_logger

from database import app
from services import who_service, europe_service, vaccination_service, admin_service, rki_service
from workers import celery

from covid19.oodm.who.who_model import WhoGlobalDataImportTable
from covid19.oodm.who.who_model import WhoRegion, WhoCountry, WhoDateReported, WhoGlobalData
from covid19.oodm.europe.europe_model import EuropeDataImportTable, EuropeDateReported, EuropeContinent
from covid19.oodm.europe.europe_model import EuropeCountry, EuropeData
from covid19.oodm.common.common_model_transient import ApplicationPage
from covid19.oodm.vaccination.vaccination_model import VaccinationGermanyTimeline


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

