from flask import render_template, redirect, url_for
from database import app
from covid19.blueprints.common.common_model_transient import ApplicationPage

import covid19.blueprints.who.views_who
import covid19.blueprints.europe.views_europe
import covid19.blueprints.vaccination.views_vaccination
import covid19.blueprints.rki.views_rki
import covid19.blueprints.admin.views_admin


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
