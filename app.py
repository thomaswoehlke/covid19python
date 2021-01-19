from logging.config import dictConfig
from flask import render_template, redirect, url_for, flash
from sqlalchemy.exc import OperationalError
from database import db, app, my_logging_config
from org.woehlke.covid19.who.who_model import WhoGlobalDataImportTable
from org.woehlke.covid19.who.who_model import WhoRegion, WhoCountry, WhoDateReported, WhoGlobalData
from org.woehlke.covid19.who.who_service import WhoService
from org.woehlke.covid19.europe.europe_model import EuropeDataImportTable
from org.woehlke.covid19.europe.europe_service import EuropeService
from org.woehlke.covid19.admin.admin_service import AdminService
from server_mq import who_run_update_task, who_update_short_task, who_update_initial_task
from server_mq import alive_message_task
from server_mq import europe_update_task

drop_and_create_data_again = True

class ApplicationPage:

    def __init__(self, default_title, default_subtitle=None, default_subtitle_info=None):
        self.title = default_title
        self.subtitle = default_subtitle
        self.subtitle_info = default_subtitle_info
        if self.subtitle is None:
            self.subtitle = """This is a simple hero unit, a simple jumbotron-style component 
                            for calling extra attention to featured content or information."""
        if self.subtitle_info is None:
            self.subtitle_info = """It uses utility classes for typography and spacing 
                    to space content out within the larger container."""


@app.route('/home')
def home():
    page_info = ApplicationPage('Home', "Covid19 Data")
    return render_template(
        'page_home.html',
        page_info=page_info)


@app.route('/')
def url_root():
    return redirect(url_for('home'))


#
# WHO
#
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
        'who/who_date_reported_all.html',
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
        'who/who_date_reported_one.html',
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
        'who/who_region_all.html',
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
        'who/who_region_one.html',
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
        'who/who_country_all.html',
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
        'who/who_country_one.html',
        who_country=who_country,
        page_data=page_data,
        page_info=page_info)


@app.route('/who/germany/page/<int:page>')
@app.route('/who/germany')
def url_who_germany(page=1):
    page_info = ApplicationPage('WHO', "Germany")
    who_country_germany = WhoCountry.get_germany()
    page_data = WhoGlobalData.get_data_for_country(who_country_germany, page)
    return render_template(
        'who/who_country_germany.html',
        who_country=who_country_germany,
        page_data=page_data,
        page_info=page_info)


@app.route('/who/update')
def url_who_update_run():
    app.logger.info("url_who_update_run [start]")
    who_service.who_service_download.download_file()
    who_run_update_task.apply_async()
    flash("who_service.run_update started")
    flash(message="long running background task started", category="warning")
    app.logger.info("url_who_update_run [done]")
    return redirect(url_for('home'))


@app.route('/who/update/short')
def url_who_update_short_run():
    who_service.who_service_download.download_file()
    who_update_short_task.apply_async()
    flash("who_service.run_update_short started")
    flash(message="long running background task started", category="warning")
    return redirect(url_for('home'))


@app.route('/who/update/initial')
def url_who_update_initial_run():
    who_service.who_service_download.download_file()
    who_update_initial_task.apply_async()
    flash("who_service.run_update_short started")
    flash(message="long running background task started", category="warning")
    return redirect(url_for('home'))


@app.route('/test/who/update/countries')
def url_update_data_countries():
    who_service.run_update_countries()
    flash("who_service.run_update_countries started")
    return redirect(url_for('home'))


#
# Europe
#
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


@app.route('/europe/update')
def europe_update_data():
    europe_service.download()
    europe_update_task.apply_async()
    flash("europe_service.run_update started")
    return redirect(url_for('home'))


@app.route('/europe/imported/page/<int:page>')
@app.route('/europe/imported')
def url_europe_data_imported(page=1):
    page_info = ApplicationPage('Europe', "Last Import")
    page_data = EuropeDataImportTable.get_all_as_page(page)
    return render_template(
        'europe/europe_imported.html',
        page_data=page_data,
        page_info=page_info)


#
# NRW
#
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


@app.route('/test/alive_message')
def url_alive_message_start():
    app.logger.info("url_alive_message_start [start]")
    alive_message_task.apply_async()
    flash("alive_message_task started")
    app.logger.info("url_alive_message_start [done]")
    return redirect(url_for('home'))


@app.route('/admin/database/dump')
def url_admin_database_dump():
    app.logger.info("url_admin_database_dump [start]")
    admin_service.run_admin_database_dump()
    flash("admin_service.run_admin_database_dump started")
    app.logger.info("url_admin_database_dump [done]")
    return redirect(url_for('home'))


@app.route('/admin/database/import')
def url_admin_database_import():
    app.logger.info("url_admin_database_import [start]")
    admin_service.run_admin_database_import()
    flash("admin_service.run_admin_database_import started")
    app.logger.info("url_admin_database_import [done]")
    return redirect(url_for('home'))


@app.route('/admin/database/drop')
def url_admin_database_drop():
    app.logger.info("url_admin_database_drop [start]")
    admin_service.run_admin_database_drop()
    if drop_and_create_data_again:
        europe_service.download()
        europe_update_task.apply_async()
        who_service.run_download()
        who_update_initial_task.apply_async()
    flash("admin_service.run_admin_database_drop started")
    app.logger.info("url_admin_database_drop [done]")
    return redirect(url_for('home'))


if __name__ == '__main__':
    dictConfig(my_logging_config)
    db.create_all()
    who_service = WhoService(db)
    europe_service = EuropeService(db)
    admin_service = AdminService(db)
    app.run(debug=True)
