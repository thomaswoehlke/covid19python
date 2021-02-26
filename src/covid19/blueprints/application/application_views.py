from flask import render_template, redirect, url_for, Blueprint
from flask_admin.contrib.sqla import ModelView

from database import app, admin, db
from covid19.blueprints.application.application_model_transient import ApplicationPage

import covid19.blueprints.admin.admin_views
import covid19.blueprints.ecdc.ecdc_views
import covid19.blueprints.rki_bundeslaender.rki_bundeslaender_views
import covid19.blueprints.rki_landkreise.rki_landkreise_views
import covid19.blueprints.rki_vaccination.rki_vaccination_views
import covid19.blueprints.who.who_views


from covid19.blueprints.admin.admin_views import app_admin
from covid19.blueprints.ecdc.ecdc_views import app_ecdc
from covid19.blueprints.rki_bundeslaender.rki_bundeslaender_views import app_rki_bundeslaender
from covid19.blueprints.rki_landkreise.rki_landkreise_views import app_rki_landkreise
from covid19.blueprints.rki_vaccination.rki_vaccination_views import app_rki_vaccination
from covid19.blueprints.who.who_views import app_who
from covid19.blueprints.owid.owid_views import app_owid

app_application = Blueprint('application', __name__, template_folder='templates', url_prefix='/')

app.register_blueprint(app_admin, url_prefix='/admin')
app.register_blueprint(app_application, url_prefix='/application')
app.register_blueprint(app_ecdc, url_prefix='/ecdc')
app.register_blueprint(app_rki_bundeslaender, url_prefix='/rki/bundeslaender')
app.register_blueprint(app_rki_landkreise, url_prefix='/rki/landkreise')
app.register_blueprint(app_rki_vaccination, url_prefix='/rki/vaccination')
app.register_blueprint(app_who, url_prefix='/who')
app.register_blueprint(app_owid, url_prefix='/owid')

############################################################################################
#
# WEB
#
@app.route('/home')
def url_home():
    page_info = ApplicationPage('Home', "Covid19 Data")
    return render_template(
        'application/page_home.html',
        page_info=page_info)


@app.route('/')
def url_root():
    return redirect(url_for('url_home'))
