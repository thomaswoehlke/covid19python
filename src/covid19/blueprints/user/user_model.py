from sqlalchemy import and_, func
from datetime import date
from database import db, ITEMS_PER_PAGE
from sqlalchemy.orm import joinedload
from covid19.blueprints.application.application_model import ApplicationDateReported, ApplicationRegion


class UserDateReported(ApplicationDateReported):
    __tablename__ = 'usr_datereported'
    __mapper_args__ = {'concrete': True}
    __table_args__ = (
        db.UniqueConstraint('date_reported', 'datum', name="uix_usr_datereported"),
    )

    id = db.Column(db.Integer, primary_key=True)
    date_reported = db.Column(db.String(255), nullable=False, unique=True)
    year_week = db.Column(db.String(255), nullable=False)
    datum = db.Column(db.Date, nullable=False, unique=True)
    year = db.Column(db.Integer, nullable=False)
    month = db.Column(db.Integer, nullable=False)
    day_of_month = db.Column(db.Integer, nullable=False)
    day_of_week = db.Column(db.Integer, nullable=False)
    week_of_year = db.Column(db.Integer, nullable=False)

    @classmethod
    def create_new_object_factory(cls, my_date_rep):
        my_datum = date.fromisoformat(my_date_rep)
        (my_iso_year, week_number, weekday) = my_datum.isocalendar()
        my_year_week = "" + str(my_iso_year)
        if week_number < 10:
            my_year_week += "-0"
        else:
            my_year_week += "-"
        my_year_week += str(week_number)
        return UserDateReported(
            date_reported=my_date_rep,
            datum=my_datum,
            year=my_datum.year,
            month=my_datum.month,
            day_of_month=my_datum.day,
            day_of_week=weekday,
            week_of_year=week_number,
            year_week=my_year_week
        )


class UserRegion(ApplicationRegion):
    __tablename__ = 'usr_country_region'
    __mapper_args__ = {'concrete': True}
    __table_args__ = (
        db.UniqueConstraint('region', name="uix_usr_country_region"),
    )

    id = db.Column(db.Integer, primary_key=True)
    region = db.Column(db.String(255), nullable=False, unique=True)


class UserCountry(db.Model):
    __tablename__ = 'usr_country'
    __table_args__ = (
        db.UniqueConstraint('country_code', 'country', name="uix_usr_country"),
    )

    id = db.Column(db.Integer, primary_key=True)
    country_code = db.Column(db.String(255), unique=True, nullable=False)
    country = db.Column(db.String(255), unique=True, nullable=False)
    region_id = db.Column(db.Integer, db.ForeignKey('usr_country_region.id'), nullable=False)
    region = db.relationship(
        'UserRegion',
        lazy='joined',
        cascade='all, delete',
        order_by='UserRegion.region')

    def __str__(self):
        result = ""
        result += self.country_code
        result += " "
        result += self.country
        result += " "
        result += self.region.region
        result += " "
        return result

    @classmethod
    def remove_all(cls):
        for one in cls.get_all():
            db.session.delete(one)
        db.session.commit()
        return None

    @classmethod
    def get_all_as_page(cls, page):
        return db.session.query(cls)\
            .order_by(cls.country)\
            .paginate(page, per_page=ITEMS_PER_PAGE)

    @classmethod
    def get_all(cls):
        return db.session.query(cls)\
            .order_by(cls.country)\
            .all()

    @classmethod
    def get_all_as_dict(cls):
        countries = {}
        for my_country in cls.get_all():
            countries[my_country.country_code] = my_country
        return countries

    @classmethod
    def get_by_id(cls, other_id):
        return db.session.query(cls)\
            .filter(cls.id == other_id)\
            .one()

    @classmethod
    def get_germany(cls):
        return db.session.query(cls)\
            .filter(cls.country_code == 'DE')\
            .one_or_none()

    @classmethod
    def find_by_country_code_and_country_and_who_region_id(cls, i_country_code, i_country, my_region):
        return db.session.query(cls).filter(
            and_(
                cls.country_code == i_country_code,
                cls.country == i_country,
                cls.region_id == my_region.id
            )
        ).one_or_none()

    @classmethod
    def find_by_country_code(cls, i_country_code):
        return db.session.query(cls).filter(
            cls.country_code == i_country_code
        ).one_or_none()

    @classmethod
    def find_by_country(cls, i_country):
        return db.session.query(cls).filter(
            cls.country == i_country
        ).one_or_none()

    @classmethod
    def get_by_country_code(cls, i_country_code):
        return db.session.query(cls).filter(
            cls.country_code == i_country_code
        ).one()

    @classmethod
    def get_by_country(cls, i_country):
        return db.session.query(cls).filter(
            cls.country == i_country
        ).one()

    @classmethod
    def get_who_countries_for_region(cls, region, page):
        return db.session.query(cls).filter(
            cls.region == region
        ).order_by(cls.country).paginate(page, per_page=ITEMS_PER_PAGE)


class UserData(db.Model):
    __tablename__ = 'usr'

    id = db.Column(db.Integer, primary_key=True)
    cases_new = db.Column(db.Integer, nullable=False)
    cases_cumulative = db.Column(db.Integer, nullable=False)
    deaths_new = db.Column(db.Integer, nullable=False)
    deaths_cumulative = db.Column(db.Integer, nullable=False)
    date_reported_id = db.Column(db.Integer,
        db.ForeignKey('usr_datereported.id'), nullable=False)
    date_reported = db.relationship(
        'UserDateReported',
        lazy='joined',
        cascade='all, delete',
        order_by='desc(UserDateReported.date_reported)')
    country_id = db.Column(db.Integer,
        db.ForeignKey('usr_country.id'), nullable=False)
    country = db.relationship(
        'UserCountry',
        lazy='joined',
        cascade='all, delete',
        order_by='asc(UserCountry.country)')

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

    @classmethod
    def find_one_or_none_by_date_and_country(cls, my_date_reported, my_country):
        return db.session.query(cls).filter(
            and_(
                cls.date_reported_id == my_date_reported.id,
                cls.country_id == my_country.id
            )
        ).one_or_none()

    @classmethod
    def get_data_for_country(cls, user_country, page):
        return db.session.query(cls).filter(
            cls.country_id == user_country.id
        ).populate_existing().options(
            joinedload(cls.country).joinedload(UserCountry.region),
            joinedload(cls.date_reported)
        ).paginate(page, per_page=ITEMS_PER_PAGE)

    @classmethod
    def get_data_for_day(cls, date_reported, page):
        return db.session.query(cls).filter(
                cls.date_reported_id == date_reported.id
            ).populate_existing().options(
                joinedload(cls.country).joinedload(UserCountry.region),
                joinedload(cls.date_reported)
            ).order_by(
                cls.deaths_new.desc(),
                cls.cases_new.desc(),
                cls.deaths_cumulative.desc(),
                cls.cases_cumulative.desc()
            ).paginate(page, per_page=ITEMS_PER_PAGE)

    @classmethod
    def get_data_for_day_order_by_cases_new(cls, date_reported, page):
        return db.session.query(cls).filter(
                cls.date_reported_id == date_reported.id
            ).populate_existing().options(
                joinedload(cls.country).joinedload(UserCountry.region),
                joinedload(cls.date_reported)
            ).order_by(
                cls.cases_new.desc()
            ).paginate(page, per_page=ITEMS_PER_PAGE)

    @classmethod
    def get_data_for_day_order_by_cases_cumulative(cls, date_reported, page):
        return db.session.query(cls).filter(
                cls.date_reported_id == date_reported.id
            ).populate_existing().options(
                joinedload(cls.country).joinedload(UserCountry.region),
                joinedload(cls.date_reported)
            ).order_by(
                cls.cases_cumulative.desc()
            ).paginate(page, per_page=ITEMS_PER_PAGE)

    @classmethod
    def get_data_for_day_order_by_deaths_new(cls, date_reported, page):
        return db.session.query(cls).filter(
                cls.date_reported_id == date_reported.id
            ).populate_existing().options(
                joinedload(cls.country).joinedload(UserCountry.region),
                joinedload(cls.date_reported)
            ).order_by(
                cls.deaths_new.desc()
            ).paginate(page, per_page=ITEMS_PER_PAGE)

    @classmethod
    def get_data_for_day_order_by_deaths_cumulative(cls, date_reported, page):
        return db.session.query(cls).filter(
                cls.date_reported_id == date_reported.id
            ).populate_existing().options(
                joinedload(cls.country).joinedload(UserCountry.region),
                joinedload(cls.date_reported)
            ).order_by(
                cls.deaths_cumulative.desc()
            ).paginate(page, per_page=ITEMS_PER_PAGE)

    @classmethod
    def get_data_for_country_order_by_cases_new(cls, user_country, page):
        return db.session.query(cls).filter(
            cls.country_id == user_country.id
        ).populate_existing().options(
            joinedload(cls.country).joinedload(UserCountry.region),
            joinedload(cls.date_reported)
        ).order_by(
            cls.cases_new.desc()
        ).paginate(page, per_page=ITEMS_PER_PAGE)

    @classmethod
    def get_data_for_country_order_by_cases_cumulative(cls, user_country, page):
        return db.session.query(cls).filter(
            cls.country_id == user_country.id
        ).populate_existing().options(
            joinedload(cls.country).joinedload(UserCountry.region),
            joinedload(cls.date_reported)
        ).order_by(
            cls.cases_cumulative.desc()
        ).paginate(page, per_page=ITEMS_PER_PAGE)

    @classmethod
    def get_data_for_country_order_by_deaths_new(cls, user_country, page):
        return db.session.query(cls).filter(
            cls.country_id == user_country.id
        ).populate_existing().options(
            joinedload(cls.country).joinedload(UserCountry.region),
            joinedload(cls.date_reported)
        ).order_by(
            cls.deaths_new.desc()
        ).paginate(page, per_page=ITEMS_PER_PAGE)

    @classmethod
    def get_data_for_country_order_by_deaths_cumulative(cls, user_country, page):
        return db.session.query(cls).filter(
            cls.country_id == user_country.id
        ).populate_existing().options(
            joinedload(cls.country).joinedload(UserCountry.region),
            joinedload(cls.date_reported)
        ).order_by(
            cls.deaths_cumulative.desc()
        ).paginate(page, per_page=ITEMS_PER_PAGE)
