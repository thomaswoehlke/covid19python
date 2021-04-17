from flask import render_template, redirect, url_for, flash, Blueprint
from sqlalchemy.exc import OperationalError
from celery import states
from celery.utils.log import get_task_logger
from flask_admin.contrib.sqla import ModelView
from flask_login import AnonymousUserMixin, login_required, login_user, logout_user
from flask_login import current_user, login_user
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
def login_form():
    page_info = ApplicationPage('usr', "Login")
    if current_user.is_authenticated:
        return redirect(url_for('usr.profile'))
    form = LoginForm()
    return flask.render_template('usr/login.html', form=form, page_info=page_info)


@app_user.route('/login', methods=['POST'])
def login():
    page_info = ApplicationPage('usr', "Login")
    if current_user.is_authenticated:
        return redirect(url_for('usr.profile'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('usr.login'))
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('usr.profile'))
    return flask.render_template('usr/login.html', form=form, page_info=page_info)


@app_user.route("/profile")
@login_required
def profile():
    page_info = ApplicationPage('usr', "profile")
    return flask.render_template('usr/profile.html', page_info=page_info)


@app_user.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('usr.login'))


@login_manager.user_loader
def load_user(user_id):
    return User.get_by_id(user_id)


@login_manager.unauthorized_handler
def unauthorized():
    flash("not authorized")
    return redirect(url_for('usr.login'))

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
