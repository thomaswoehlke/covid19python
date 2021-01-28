from flask import render_template, redirect, url_for
from database import app
from app.oodm.common.common_model_transient import ApplicationPage

import views_who
import views_europe
import view_vaccination
import views_rki
import views_nrw
import view_admin


############################################################################################
#
# WEB
#
@app.route('/home')
def url_home():
    page_info = ApplicationPage('Home', "Covid19 Data")
    return render_template(
        'page_home.html',
        page_info=page_info)


@app.route('/')
def url_root():
    return redirect(url_for('url_home'))
