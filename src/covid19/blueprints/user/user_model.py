from sqlalchemy import and_, func
from datetime import date
from database import db, ITEMS_PER_PAGE
from sqlalchemy.orm import joinedload
from flask_login import UserMixin, AnonymousUserMixin
from wtforms import Form, BooleanField, StringField, validators
from werkzeug.security import generate_password_hash, check_password_hash
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from covid19.blueprints.application.application_model import ApplicationDateReported, ApplicationRegion


class User(UserMixin, db.Model):
    __tablename__ = 'usr'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.Unicode, nullable=False, unique=True)
    password_hash = db.Column(db.String, nullable=False)
    name = db.Column(db.String(1000), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    @classmethod
    def remove_all(cls):
        for one in cls.get_all():
            db.session.delete(one)
        db.session.commit()
        return None

    @classmethod
    def get_all_as_page(cls, page):
        return db.session.query(cls).paginate(page, per_page=ITEMS_PER_PAGE)

    @classmethod
    def get_all(cls):
        return db.session.query(cls).all()

    @classmethod
    def get_by_id(cls, other_id):
        return db.session.query(cls).filter(cls.id == other_id).one()


class AnonymousUserValueObject(AnonymousUserMixin):
    pass


class LoginForm(Form):
    email = StringField('Email Address', [validators.Length(min=6, max=35), validators.Email(), validators.InputRequired()])
    password = StringField('Password', [validators.Length(min=6, max=35), validators.InputRequired()])
    accept_rules = BooleanField('I accept the site rules', [validators.InputRequired()])

    def validate_on_submit(self):
        if self.email is None:
            return False
        if self.password is None:
            return False
        if self.accept_rules is None:
            return False
        return True

