from flask import render_template, redirect, url_for, flash, Blueprint
from sqlalchemy.exc import OperationalError
from celery import states
from celery.utils.log import get_task_logger
from flask_admin.contrib.sqla import ModelView

from database import app, admin, db
from covid19.blueprints.application.application_services import user_service
from covid19.blueprints.application.application_workers import celery

from covid19.blueprints.user.user_model import UserRegion, UserCountry, UserDateReported, UserData
from covid19.blueprints.application.application_model_transient import ApplicationPage


app_user = Blueprint('user', __name__, template_folder='templates', url_prefix='/user')

# admin.add_view(ModelView(userImport, db.session, category="User"))
admin.add_view(ModelView(UserDateReported, db.session, category="User"))
admin.add_view(ModelView(UserRegion, db.session, category="User"))
admin.add_view(ModelView(UserCountry, db.session, category="User"))
admin.add_view(ModelView(UserData, db.session, category="User"))


# ---------------------------------------------------------------------------------------------------------------
#  Url Routes Frontend
# ---------------------------------------------------------------------------------------------------------------


@app_user.route('/info')
def url_user_info():
    page_info = ApplicationPage('user', "Info")
    return render_template(
        'user/user_info.html',
        page_info=page_info)


@app_user.route('/tasks')
def url_user_tasks():
    page_info = ApplicationPage('user', "Tasks")
    return render_template(
        'user/user_tasks.html',
        page_info=page_info)


@app_user.route('/date_reported/all/page/<int:page>')
@app_user.route('/date_reported/all')
def url_user_date_reported_all(page: int = 1):
    page_info = ApplicationPage('user', "Date Reported", "All")
    try:
        page_data = UserDateReported.get_all_as_page(page)
    except OperationalError:
        flash("No regions in the database.")
        page_data = None
    return render_template(
        'user/date_reported/user_date_reported_all.html',
        page_data=page_data,
        page_info=page_info)


@app_user.route('/date_reported/<int:date_reported_id>/page/<int:page>')
@app_user.route('/date_reported/<int:date_reported_id>')
def url_user_date_reported(date_reported_id: int, page: int = 1):
    date_reported = UserDateReported.get_by_id(date_reported_id)
    page_info = ApplicationPage(
        "Date Reported: " + date_reported.date_reported,
        'user',
        "data of all reported countries for User date reported " + date_reported.date_reported + " "
    )
    try:
        page_data = UserData.get_data_for_day(date_reported, page)
    except OperationalError:
        flash("No data in the database.")
        page_data = None
    return render_template(
        'user/date_reported/user_date_reported_one.html',
        user_date_reported=date_reported,
        page_data=page_data,
        page_info=page_info)


@app_user.route('/date_reported/<int:date_reported_id>/cases_new/page/<int:page>')
@app_user.route('/date_reported/<int:date_reported_id>/cases_new')
def url_user_date_reported_cases_new(date_reported_id: int, page: int = 1):
    date_reported = UserDateReported.get_by_id(date_reported_id)
    page_info = ApplicationPage(
        "Date Reported: " + date_reported.date_reported,
        'user',
        "data of all reported countries for User date reported " + date_reported.date_reported + " "
    )
    try:
        page_data = UserData.get_data_for_day_order_by_cases_new(date_reported, page)
    except OperationalError:
        flash("No data in the database.")
        page_data = None
    return render_template(
        'user/date_reported/user_date_reported_one_cases_new.html',
        user_date_reported=date_reported,
        page_data=page_data,
        page_info=page_info)


@app_user.route('/date_reported/<int:date_reported_id>/cases_cumulative/page/<int:page>')
@app_user.route('/date_reported/<int:date_reported_id>/cases_cumulative')
def url_user_date_reported_cases_cumulative(date_reported_id: int, page: int = 1):
    date_reported = UserDateReported.get_by_id(date_reported_id)
    page_info = ApplicationPage(
        "Date Reported: " + date_reported.date_reported,
        'user',
        "data of all reported countries for User date reported " + date_reported.date_reported + " "
    )
    try:
        page_data = UserData.get_data_for_day_order_by_cases_cumulative(date_reported, page)
    except OperationalError:
        flash("No data in the database.")
        page_data = None
    return render_template(
        'user/date_reported/user_date_reported_one_cases_cumulative.html',
        user_date_reported=date_reported,
        page_data=page_data,
        page_info=page_info)


@app_user.route('/date_reported/<int:date_reported_id>/deaths_new/page/<int:page>')
@app_user.route('/date_reported/<int:date_reported_id>/deaths_new')
def url_user_date_reported_deaths_new(date_reported_id: int, page: int = 1):
    date_reported = UserDateReported.get_by_id(date_reported_id)
    page_info = ApplicationPage(
        "Date Reported: " + date_reported.date_reported,
        'user',
        "data of all reported countries for User date reported " + date_reported.date_reported + " "
    )
    try:
        page_data = UserData.get_data_for_day_order_by_deaths_new(date_reported, page)
    except OperationalError:
        flash("No data in the database.")
        page_data = None
    return render_template(
        'user/date_reported/user_date_reported_one_deaths_new.html',
        user_date_reported=date_reported,
        page_data=page_data,
        page_info=page_info)


@app_user.route('/date_reported/<int:date_reported_id>/deaths_cumulative/page/<int:page>')
@app_user.route('/date_reported/<int:date_reported_id>/deaths_cumulative')
def url_user_date_reported_deaths_cumulative(date_reported_id: int, page: int = 1):
    date_reported = UserDateReported.get_by_id(date_reported_id)
    page_info = ApplicationPage(
        "Date Reported: " + date_reported.date_reported,
        'user',
        "data of all reported countries for User date reported " + date_reported.date_reported + " "
    )
    try:
        page_data = UserData.get_data_for_day_order_by_deaths_cumulative(date_reported, page)
    except OperationalError:
        flash("No data in the database.")
        page_data = None
    return render_template(
        'user/date_reported/user_date_reported_one_deaths_cumulative.html',
        user_date_reported=date_reported,
        page_data=page_data,
        page_info=page_info)


@app_user.route('/region/all/page/<int:page>')
@app_user.route('/region/all')
def url_user_region_all(page: int = 1):
    page_info = ApplicationPage('user', "Region", "All")
    try:
        page_data = UserRegion.get_all_as_page(page)
    except OperationalError:
        flash("No regions in the database.")
        page_data = None
    return render_template(
        'user/region/user_region_all.html',
        page_data=page_data,
        page_info=page_info)


@app_user.route('/region/<int:region_id>/page/<int:page>')
@app_user.route('/region/<int:region_id>')
def url_user_region(region_id: int, page: int = 1):
    user_region = None
    page_info = ApplicationPage("Countries", "User Region")
    try:
        user_region = UserRegion.get_by_id(region_id)
        page_data = UserCountry.get_user_countries_for_region(user_region, page)
        page_info.title = user_region.region
        page_info.subtitle = "User Region"
        page_info.subtitle_info = "Countries of User Region " + user_region.region
    except OperationalError:
        flash("No countries of that region in the database.")
        page_data = None
    return render_template(
        'user/region/user_region_one.html',
        user_region=user_region,
        page_data=page_data,
        page_info=page_info)


@app_user.route('/country/all/page/<int:page>')
@app_user.route('/country/all')
def url_user_country_all(page: int = 1):
    page_info = ApplicationPage('user', "Countries", "All")
    try:
        page_data = UserCountry.get_all_as_page(page)
    except OperationalError:
        flash("No regions in the database.")
        page_data = None
    return render_template(
        'user/country/user_country_all.html',
        page_data=page_data,
        page_info=page_info)


@app_user.route('/country/<int:country_id>/page/<int:page>')
@app_user.route('/country/<int:country_id>')
def url_user_country(country_id: int, page: int = 1):
    user_country = UserCountry.get_by_id(country_id)
    page_data = UserData.get_data_for_country(user_country, page)
    page_info = ApplicationPage(user_country.country,
           "Country "+user_country.country_code,
           "Data per Day in Country "+user_country.country+" of User Region "+user_country.region.region)
    return render_template(
        'user/country/user_country_one.html',
        user_country=user_country,
        page_data=page_data,
        page_info=page_info)
