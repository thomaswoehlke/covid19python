from sqlalchemy import and_
from datetime import date
from database import db, ITEMS_PER_PAGE
from covid19.blueprints.application.application_model import ApplicationDateReported, ApplicationRegion


class EcdcDateReported(ApplicationDateReported):
    __tablename__ = 'ecdc_date_reported'
    __mapper_args__ = { 'concrete': True }
    __table_args__ = (
        db.UniqueConstraint('date_reported', 'datum', name="uix_ecdc_date_reported"),
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

    def get_date_import_format_from_date_reported(self):
        my_date_parts = self.date_reported.split("-")
        my_year = my_date_parts[0]
        my_month = my_date_parts[1]
        my_day = my_date_parts[2]
        return my_day + '/' + my_month + '/' + my_year

    @classmethod
    def get_date_import_format_from_date_reported_str(cls, date_reported_str: str):
        my_date_parts = date_reported_str.split("-")
        my_year = my_date_parts[0]
        my_month = my_date_parts[1]
        my_day = my_date_parts[2]
        return my_day + '/' + my_month + '/' + my_year

    @classmethod
    def get_date_format_from_ecdc_import_fomat(cls, date_reported_ecdc_import_fomat: str):
        my_date_parts = date_reported_ecdc_import_fomat.split("/")
        my_year = my_date_parts[2]
        my_month = my_date_parts[1]
        my_day = my_date_parts[0]
        return my_year + '-' + my_month + '-' + my_day

    @classmethod
    def get_datum_parts(cls, my_date_rep: str):
        my_date_parts = my_date_rep.split('/')
        my_day = int(my_date_parts[0])
        my_month = int(my_date_parts[1])
        my_year = int(my_date_parts[2])
        datum_parts = (my_year, my_month, my_day)
        return datum_parts

    @classmethod
    def create_new_object_factory(cls, my_date_rep: str):
        (my_year, my_month, my_day) = cls.get_datum_parts(my_date_rep)
        date_reported = super().get_datum_as_str(my_year, my_month, my_day)
        my_datum = super().get_datum(my_year, my_month, my_day)
        (my_iso_year, week_number, weekday) = my_datum.isocalendar()
        my_year_week = super().my_year_week(my_iso_year, week_number)
        return EcdcDateReported(
            date_reported=date_reported,
            datum=my_datum,
            year=my_datum.year,
            month=my_datum.month,
            day_of_month=my_datum.day,
            day_of_week=weekday,
            week_of_year=week_number,
            year_week=my_year_week
        )


class EcdcContinent(ApplicationRegion):
    __tablename__ = 'ecdc_continent'
    __mapper_args__ = {'concrete': True}
    __table_args__ = (
        db.UniqueConstraint('region', name="uix_ecdc_continent"),
    )

    id = db.Column(db.Integer, primary_key=True)
    region = db.Column(db.String(255), nullable=False, unique=True)


class EcdcCountry(db.Model):
    __tablename__ = 'ecdc_country'
    __table_args__ = (
        db.UniqueConstraint('countries_and_territories', 'geo_id', 'country_territory_code', name="uix_ecdc_country"),
    )

    id = db.Column(db.Integer, primary_key=True)
    countries_and_territories = db.Column(db.String(255), nullable=False)
    pop_data_2019 = db.Column(db.String(255), nullable=False)
    geo_id = db.Column(db.String(255), nullable=False)
    country_territory_code = db.Column(db.String(255), nullable=False)

    continent_id = db.Column(db.Integer, db.ForeignKey('ecdc_continent.id'), nullable=False)
    continent = db.relationship(
        'EcdcContinent',
        lazy='subquery', cascade="all, delete",
        order_by='asc(EcdcContinent.region)'
    )

    def __str__(self):
        return " " + self.geo_id \
             + " " + self.country_territory_code \
             + " " + self.countries_and_territories \
             + " "

    @classmethod
    def remove_all(cls):
        for one in cls.get_all():
            db.session.delete(one)
        db.session.commit()
        return None

    @classmethod
    def get_all_as_page(cls, page):
        return db.session.query(cls)\
            .order_by(cls.countries_and_territories.asc())\
            .paginate(page, per_page=ITEMS_PER_PAGE)

    @classmethod
    def get_all(cls):
        return db.session.query(cls)\
            .order_by(cls.countries_and_territories.asc())\
            .all()

    @classmethod
    def get_by_id(cls, other_id: int):
        return db.session.query(cls)\
            .filter(cls.id == other_id)\
            .one()

    @classmethod
    def find_by_id(cls, other_id: int):
        return db.session.query(cls)\
            .filter(cls.id == other_id)\
            .one_or_none()

    @classmethod
    def get_by(cls, countries_and_territories: str, geo_id: str, country_territory_code: str):
        return db.session.query(cls).filter(and_(
            (cls.countries_and_territories == countries_and_territories),
            (cls.geo_id == geo_id),
            (cls.country_territory_code == country_territory_code)
        )).one()

    @classmethod
    def find_by(cls, countries_and_territories: str, geo_id: str, country_territory_code: str):
        return db.session.query(cls).filter(and_(
            (cls.countries_and_territories == countries_and_territories),
            (cls.geo_id == geo_id),
            (cls.country_territory_code == country_territory_code)
        )).one_or_none()

    @classmethod
    def find_by_continent(cls, continent: EcdcContinent, page: int):
        return db.session.query(cls)\
            .filter(cls.continent_id == continent.id)\
            .paginate(page, per_page=ITEMS_PER_PAGE)

    @classmethod
    def get_germany(cls):
        return db.session.query(cls) \
            .filter(cls.country_territory_code == 'DEU') \
            .one()

    @classmethod
    def find_germany(cls):
        return db.session.query(cls) \
            .filter(cls.country_territory_code == 'DEU') \
            .one_or_none()


class EcdcData(db.Model):
    __tablename__ = 'ecdc_data'

    id = db.Column(db.Integer, primary_key=True)
    deaths_weekly = db.Column(db.Integer, nullable=False)
    cases_weekly = db.Column(db.Integer, nullable=False)
    notification_rate_per_100000_population_14days = db.Column(db.Float, nullable=False)

    ecdc_country_id = db.Column(db.Integer, db.ForeignKey('ecdc_country.id'), nullable=False)
    ecdc_country = db.relationship(
        'EcdcCountry',
        lazy='joined', cascade="all, delete",
        order_by='asc(EcdcCountry.countries_and_territories)'
    )

    ecdc_date_reported_id = db.Column(db.Integer, db.ForeignKey('ecdc_date_reported.id'), nullable=False)
    ecdc_date_reported = db.relationship(
        'EcdcDateReported',
        lazy='joined', cascade='all, delete',
        order_by='desc(EcdcDateReported.date_reported)'
    )

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
    def get_by_id(cls, other_id: int):
        return db.session.query(cls).filter(cls.id == other_id).one()

    @classmethod
    def find_by_id(cls, other_id: int):
        return db.session.query(cls).filter(cls.id == other_id).one_or_none()

    @classmethod
    def find_by_date_reported(cls, ecdc_date_reported, page: int):
        #TODO: * Issue #43 /ecdc/date_reported
        return db.session.query(cls).filter(
            cls.ecdc_date_reported_id == ecdc_date_reported.id)\
            .order_by(cls.notification_rate_per_100000_population_14days.desc())\
            .paginate(page, per_page=ITEMS_PER_PAGE)

    @classmethod
    def find_by_date_reported_notification_rate(cls, ecdc_date_reported, page: int):
        # TODO: * Issue #43 /ecdc/date_reported
        return db.session.query(cls).filter(
            cls.ecdc_date_reported_id == ecdc_date_reported.id) \
            .order_by(cls.notification_rate_per_100000_population_14days.desc()) \
            .paginate(page, per_page=ITEMS_PER_PAGE)

    @classmethod
    def find_by_date_reported_deaths_weekly(cls, ecdc_date_reported, page: int):
        # TODO: * Issue #43 /ecdc/date_reported
        return db.session.query(cls).filter(
            cls.ecdc_date_reported_id == ecdc_date_reported.id) \
            .order_by(cls.deaths_weekly.desc()) \
            .paginate(page, per_page=ITEMS_PER_PAGE)

    @classmethod
    def find_by_date_reported_cases_weekly(cls, ecdc_date_reported, page: int):
        # TODO: * Issue #43 /ecdc/date_reported
        return db.session.query(cls).filter(
            cls.ecdc_date_reported_id == ecdc_date_reported.id) \
            .order_by(cls.cases_weekly.desc()) \
            .paginate(page, per_page=ITEMS_PER_PAGE)

    @classmethod
    def find_by_country(cls, ecdc_country, page: int):
        return db.session.query(cls).filter(
            cls.ecdc_country_id == ecdc_country.id) \
            .paginate(page, per_page=ITEMS_PER_PAGE)
