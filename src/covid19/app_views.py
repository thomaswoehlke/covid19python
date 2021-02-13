from flask import render_template, redirect, url_for
from database import app
from covid19.blueprints.common.common_model_transient import ApplicationPage

import covid19.blueprints.who.who_views
import covid19.blueprints.europe.europe_views
import covid19.blueprints.rki_vaccination.vaccination_views
import covid19.blueprints.rki_landkreise.rki_views
import covid19.blueprints.rki_bundeslaender.rki_views
import covid19.blueprints.admin.admin_views

from covid19.blueprints.who.who_views import app_who
from covid19.blueprints.europe.europe_views import app_europe
from covid19.blueprints.rki_vaccination.vaccination_views import app_vaccination
from covid19.blueprints.rki_landkreise.rki_views import app_rki_landkreise
from covid19.blueprints.rki_bundeslaender.rki_views import app_rki_bundeslaender
from covid19.blueprints.admin.admin_views import app_admin

app.register_blueprint(app_who, url_prefix='/who')
app.register_blueprint(app_europe, url_prefix='/europe')
app.register_blueprint(app_vaccination, url_prefix='/vaccination')
app.register_blueprint(app_rki_bundeslaender, url_prefix='/rki/bundeslaender')
app.register_blueprint(app_rki_landkreise, url_prefix='/rki/landkreise')
app.register_blueprint(app_admin, url_prefix='/admin')


############################################################################################
#
# WEB
#
@app.route('/home')
def url_home():
    page_info = ApplicationPage('Home', "Covid19 Data")
    return render_template(
        'common/page_home.html',
        page_info=page_info)


@app.route('/')
def url_root():
    return redirect(url_for('url_home'))
