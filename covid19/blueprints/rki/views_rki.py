from flask import render_template, redirect, url_for, flash, Blueprint
from sqlalchemy.exc import OperationalError

from database import app

from covid19.blueprints.who.who_model_import import WhoGlobalDataImportTable
from covid19.blueprints.common.common_model_transient import ApplicationPage

drop_and_create_data_again = True


app_rki = Blueprint('rki', __name__, template_folder='templates', static_folder='static')


##################################################################################################################
#
# RKI
#
##################################################################################################################
@app_rki.route('/rki/info')
def url_rki_info():
    page_info = ApplicationPage('RKI', "Info")
    return render_template(
        'rki/rki_info.html',
        page_info=page_info)


@app_rki.route('/rki/tasks')
def url_rki_tasks():
    page_info = ApplicationPage('RKI', "Tasks")
    return render_template(
        'rki/rki_tasks.html',
        page_info=page_info)


@app_rki.route('/rki/imported/page/<int:page>')
@app_rki.route('/rki/imported')
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
