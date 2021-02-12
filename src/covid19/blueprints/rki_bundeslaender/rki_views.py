from flask import render_template, redirect, url_for, flash, Blueprint
from sqlalchemy.exc import OperationalError

from database import app

from covid19.blueprints.common.common_model import RkiDateReported, RkiRegion, RkiCountry

from covid19.blueprints.rki_bundeslaender.rki_model import RkiBundeslaender
from covid19.blueprints.rki_bundeslaender.rki_model_import import RkiBundeslaenderImport


from covid19.blueprints.common.common_model_transient import ApplicationPage

drop_and_create_data_again = True


app_rki_bundeslaender = Blueprint('/rki/bundeslaender', __name__, template_folder='templates')


##################################################################################################################
#
# RKI
#
##################################################################################################################
@app_rki_bundeslaender.route('/info')
def url_rki_info():
    page_info = ApplicationPage('RKI', "Info")
    return render_template(
        'rki/rki_info.html',
        page_info=page_info)


@app_rki_bundeslaender.route('/tasks')
def url_rki_tasks():
    page_info = ApplicationPage('RKI', "Tasks")
    return render_template(
        'rki/rki_tasks.html',
        page_info=page_info)


@app_rki_bundeslaender.route('/imported/page/<int:page>')
@app_rki_bundeslaender.route('/imported')
def url_rki_bundeslaender_imported(page=1):
    page_info = ApplicationPage('RKI', "Last Import")
    try:
        page_data = RkiBundeslaenderImport.get_all_as_page(page)
    except OperationalError:
        flash("No data in the database.")
        page_data = None
    return render_template(
        'rki/rki_bundeslaender_imported.html',
        page_data=page_data,
        page_info=page_info)


# TODO #146 add Tasks and URLs for starting Tasks to rki_views


@app_rki_bundeslaender.route('/task/update/star_schema/initial')
def url_rki_bundeslaender_task_update_starschema_initial():
    app.logger.info("url_rki_bundeslaender_task_update_starschema_initial [start]")
    # TODO: implement url_rki_bundeslaender_task_update_starschema_initial in rki_views.py
    return redirect(url_for('who.url_who_tasks'))


@app_rki_bundeslaender.route('/task/update/star_schema/incremental')
def url_rki_bundeslaender_task_update_starschema_incremental():
    app.logger.info("url_rki_bundeslaender_task_update_starschema_incremental [start]")
    # TODO: implement url_rki_bundeslaender_task_update_starschema_incremental in rki_views.py
    return redirect(url_for('who.url_who_tasks'))


@app_rki_bundeslaender.route('/task/download/only')
def url_rki_bundeslaender_task_download_only():
    app.logger.info("url_rki_bundeslaender_task_download_only [start]")
    # TODO: implement url_rki_bundeslaender_task_download_only in rki_views.py
    return redirect(url_for('who.url_who_tasks'))


@app_rki_bundeslaender.route('/task/import/only')
def url_rki_bundeslaender_task_import_only():
    app.logger.info("url_rki_bundeslaender_task_import_only [start]")
    # TODO: implement url_rki_bundeslaender_task_import_only in rki_views.py
    return redirect(url_for('who.url_who_tasks'))


@app_rki_bundeslaender.route('/task/update/dimension-tables/only')
def url_rki_bundeslaender_task_update_dimensiontables_only():
    app.logger.info("url_rki_bundeslaender_task_update_dimensiontables_only [start]")
    # TODO: implement in rki_views.py
    return redirect(url_for('who.url_who_tasks'))


@app_rki_bundeslaender.route('/task/update/fact-table/incremental/only')
def url_rki_bundeslaender_task_update_facttable_incremental_only():
    app.logger.info("url_rki_bundeslaender_task_update_facttable_incremental_only [start]")
    # TODO: implement in rki_views.py
    return redirect(url_for('who.url_who_tasks'))


@app_rki_bundeslaender.route('/task/update/fact-table/initial/only')
def url_rki_bundeslaender_task_update_facttable_initial_only():
    app.logger.info("url_rki_bundeslaender_task_update_facttable_initial_only [start]")
    # TODO: implement in rki_views.py
    return redirect(url_for('who.url_who_tasks'))
