from flask import render_template, redirect, url_for, flash, Blueprint
from celery import states
from celery.utils.log import get_task_logger

from database import app
from covid19.services import europe_service
from covid19.workers import celery

from covid19.blueprints.europe.europe_model_import import EuropeDataImportTable
from covid19.blueprints.europe.europe_model import EuropeDateReported, EuropeContinent, EuropeCountry, EuropeData
from covid19.blueprints.common.common_model_transient import ApplicationPage


app_europe = Blueprint('europe', __name__, template_folder='templates')


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


@app_europe.route('/info')
def url_europe_info():
    page_info = ApplicationPage('Europe', "Info")
    return render_template(
        'templates/europe/europe_info.html',
        title='Europe',
        page_info=page_info)


@app_europe.route('/tasks')
def url_europe_tasks():
    page_info = ApplicationPage('Europe', "Tasks")
    return render_template(
        'templates/europe/europe_tasks.html',
        title='Europe Tasks',
        page_info=page_info)


@app_europe.route('/update/initial')
def europe_update_data():
    europe_service.download()
    task_europe_update_initial.apply_async()
    flash("europe_service.run_update started")
    return redirect(url_for('url_home'))


@app_europe.route('/imported/page/<int:page>')
@app_europe.route('/imported')
def url_europe_data_imported(page=1):
    page_info = ApplicationPage('Europe', "Last Import")
    page_data = EuropeDataImportTable.get_all_as_page(page)
    return render_template(
        'templates/europe/europe_imported.html',
        page_data=page_data,
        page_info=page_info)


@app_europe.route('/date_reported/all/page/<int:page>')
@app_europe.route('/date_reported/all')
def url_europe_date_reported_all(page=1):
    page_info = ApplicationPage('Europe', "date_reported")
    page_data = EuropeDateReported.get_all_as_page(page)
    return render_template(
        'templates/europe/date_reported/europe_date_reported_all.html',
        page_data=page_data,
        page_info=page_info)


@app_europe.route('/date_reported/<int:europe_date_reported_id>/page/<int:page>')
@app_europe.route('/date_reported/<int:europe_date_reported_id>')
@app_europe.route('/date_reported/notification_rate/<int:europe_date_reported_id>/page/<int:page>')
@app_europe.route('/date_reported/notification_rate/<int:europe_date_reported_id>')
def url_europe_date_reported_one_notification_rate(europe_date_reported_id, page=1):
    page_info = ApplicationPage('Europe', "date_reported")
    europe_date_reported = EuropeDateReported.get_by_id(europe_date_reported_id)
    page_data = EuropeData.find_by_date_reported_notification_rate(europe_date_reported, page)
    return render_template(
        'templates/europe/date_reported/europe_date_reported_one_notification_rate.html',
        europe_date_reported=europe_date_reported,
        page_data=page_data,
        page_info=page_info)


@app_europe.route('/date_reported/deaths_weekly/<int:europe_date_reported_id>/page/<int:page>')
@app_europe.route('/date_reported/deaths_weekly/<int:europe_date_reported_id>')
def url_europe_date_reported_one_deaths_weekly(europe_date_reported_id, page=1):
    page_info = ApplicationPage('Europe', "date_reported")
    europe_date_reported = EuropeDateReported.get_by_id(europe_date_reported_id)
    page_data = EuropeData.find_by_date_reported_deaths_weekly(europe_date_reported, page)
    return render_template(
        'templates/europe/date_reported/europe_date_reported_one_deaths_weekly.html',
        europe_date_reported=europe_date_reported,
        page_data=page_data,
        page_info=page_info)


@app_europe.route('/date_reported/cases_weekly/<int:europe_date_reported_id>/page/<int:page>')
@app_europe.route('/date_reported/cases_weekly/<int:europe_date_reported_id>')
def url_europe_date_reported_one_cases_weekly(europe_date_reported_id, page=1):
    page_info = ApplicationPage('Europe', "date_reported")
    europe_date_reported = EuropeDateReported.get_by_id(europe_date_reported_id)
    page_data = EuropeData.find_by_date_reported_cases_weekly(europe_date_reported, page)
    return render_template(
        'templates/europe/date_reported/europe_date_reported_one_cases_weekly.html',
        europe_date_reported=europe_date_reported,
        page_data=page_data,
        page_info=page_info)


@app_europe.route('/continent/all/page/<int:page>')
@app_europe.route('/continent/all')
def url_europe_continent_all(page=1):
    page_info = ApplicationPage('Europe', "continent")
    page_data = EuropeContinent.get_all_as_page(page)
    return render_template(
        'templates/europe/continent/europe_continent_all.html',
        page_data=page_data,
        page_info=page_info)


@app_europe.route('/continent/<int:continent_id>/page/<int:page>')
@app_europe.route('/continent/<int:continent_id>')
def url_europe_continent_one(continent_id, page=1):
    page_info = ApplicationPage('Europe', "continent")
    continent = EuropeContinent.get_by_id(continent_id)
    page_data = EuropeCountry.find_by_continent(continent, page)
    return render_template(
        'templates/europe/continent/europe_continent_one.html',
        continent=continent,
        page_data=page_data,
        page_info=page_info)


@app_europe.route('/country/all/page/<int:page>')
@app_europe.route('/country/all')
def url_europe_country_all(page=1):
    page_info = ApplicationPage('Europe', "country")
    page_data = EuropeCountry.get_all_as_page(page)
    return render_template(
        'templates/europe/country/europe_country_all.html',
        page_data=page_data,
        page_info=page_info)


@app_europe.route('/country/<int:country_id>/page/<int:page>')
@app_europe.route('/country/<int:country_id>')
def url_europe_country_one(country_id, page=1):
    page_info = ApplicationPage('Europe', "country")
    europe_country = EuropeCountry.get_by_id(country_id)
    page_data = EuropeData.find_by_country(europe_country, page)
    return render_template(
        'templates/europe/country/europe_country_one.html',
        europe_country=europe_country,
        page_data=page_data,
        page_info=page_info)


@app_europe.route('/country/germany/page/<int:page>')
@app_europe.route('/country/germany')
def url_europe_country_germany(page=1):
    page_info = ApplicationPage('Europe', "country: Germany")
    europe_country = EuropeCountry.get_germany()
    if europe_country is None:
        flash('country: Germany not found in Database', category='error')
        return redirect(url_for('url_europe_tasks'))
    page_data = EuropeData.find_by_country(europe_country, page)
    return render_template(
        'templates/europe/country/europe_country_germany.html',
        europe_country=europe_country,
        page_data=page_data,
        page_info=page_info)

