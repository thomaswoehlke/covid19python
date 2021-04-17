from flask import render_template, redirect, url_for, flash, Blueprint
from sqlalchemy.exc import OperationalError
from celery import states
from celery.utils.log import get_task_logger
from flask_admin.contrib.sqla import ModelView
from flask_login import AnonymousUserMixin, login_required, login_user, logout_user
import flask


from database import app, admin, db, login_manager
from covid19.blueprints.application.application_services import user_service
from covid19.blueprints.application.application_workers import celery

from covid19.blueprints.user.user_model import User, LoginForm
from covid19.blueprints.application.application_model_transient import ApplicationPage


app_user = Blueprint('usr', __name__, template_folder='templates', url_prefix='/usr')

admin.add_view(ModelView(User, db.session, category="usr"))


# ---------------------------------------------------------------------------------------------------------------
# URLs Login and Logout
# ---------------------------------------------------------------------------------------------------------------

@app_user.route('/login', methods=['GET'])
def loginForm():
    page_info = ApplicationPage('usr', "Login")
    # Here we use a class of some kind to represent and validate our
    # client-side form data. For example, WTForms is a library that will
    # handle this for us, and we use a custom LoginForm to validate.
    form = LoginForm()
    return flask.render_template('usr/login.html', form=form, page_info=page_info)

@app_user.route('/login', methods=['POST'])
def login():
    # Here we use a class of some kind to represent and validate our
    # client-side form data. For example, WTForms is a library that will
    # handle this for us, and we use a custom LoginForm to validate.
    form = LoginForm()
    if form.validate_on_submit():
        # Login and validate the usr.
        # usr should be an instance of your `User` class
        user = user_service.get_user_from_login_form(form)
        login_user(user)
        flash('Logged in successfully.')
        next = flask.request.args.get('next')
        # is_safe_url should check if the url is safe for redirects.
        # See http://flask.pocoo.org/snippets/62/ for an example.
        if not is_safe_url(next):
            return flask.abort(400)

        return flask.redirect(next or flask.url_for('index'))
    return flask.render_template('usr/login.html', form=form)

@app_user.route("/settings")
@login_required
def settings():
    pass

@app_user.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect("usr.login")

@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)

@login_manager.unauthorized_handler
def unauthorized():
    flash("not authorized")
    return redirect("usr.login")

# ---------------------------------------------------------------------------------------------------------------
#  Url Routes Frontend
# ---------------------------------------------------------------------------------------------------------------


@app_user.route('/info')
def url_user_info():
    page_info = ApplicationPage('usr', "Info")
    return render_template(
        'usr/user_info.html',
        page_info=page_info)


@app_user.route('/tasks')
def url_user_tasks():
    page_info = ApplicationPage('usr', "Tasks")
    return render_template(
        'usr/user_tasks.html',
        page_info=page_info)
