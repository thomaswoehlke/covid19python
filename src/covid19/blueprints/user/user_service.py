from flask import flash
from flask_login import login_manager
from werkzeug.security import generate_password_hash, check_password_hash

from database import app
from covid19.blueprints.user.user_model import User, LoginForm


class UserService:
    def __init__(self, database):
        app.logger.debug("------------------------------------------------------------")
        app.logger.debug(" User Service [init]")
        app.logger.debug("------------------------------------------------------------")
        self.__database = database
        app.logger.debug("------------------------------------------------------------")
        app.logger.info(" User Service [ready]")

    def get_user_from_login_form(self, form: LoginForm):
        user = User()
        user.email = form.email
        user.password = form.password
        return user

