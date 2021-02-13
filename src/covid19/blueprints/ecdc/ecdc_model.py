from sqlalchemy import and_
from datetime import date
from database import db, ITEMS_PER_PAGE
from covid19.blueprints.common.application_model import ApplicationDateReported, ApplicationRegion


class EcdcDateReported(ApplicationDateReported):
    __tablename__ = 'ecdc_date_reported'
    __mapper_args__ = {
        'concrete': True
    }
    __table_args__ = (
        db.UniqueConstraint('date_reported', 'datum', name="uix_europe_date_reported"),
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
        my_date_parts = my_date_rep.split("/")
        my_year = int(my_date_parts[2])
        my_month = int(my_date_parts[1])
        my_day = int(my_date_parts[0])
        my_datum = date(my_year, my_month, my_day)
        (my_iso_year, week_number, weekday) = my_datum.isocalendar()
        my_year_week = "" + str(my_iso_year)
        if week_number < 10:
            my_year_week += "-0"
        else:
            my_year_week += "-"
        my_year_week += str(week_number)
        return EcdcDateReported(
            date_reported=my_date_rep,
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
        db.UniqueConstraint('region', name="uix_europe_continent"),
    )

    id = db.Column(db.Integer, primary_key=True)
    region = db.Column(db.String(255), nullable=False, unique=True)


class EcdcCountry(db.Model):
    __tablename__ = 'ecdc_country'
    __table_args__ = (
        db.UniqueConstraint('countries_and_territories', 'geo_id', 'country_territory_code', name="uix_europe_country"),
    )

    id = db.Column(db.Integer, primary_key=True)
    countries_and_territories = db.Column(db.String(255), nullable=False)
    pop_data_2019 = db.Column(db.String(255), nullable=False)
    geo_id = db.Column(db.String(255), nullable=False)
    country_territory_code = db.Column(db.String(255), nullable=False)

    continent_id = db.Column(db.Integer, db.ForeignKey('ecdc_continent.id'), nullable=False)
    continent = db.relationship(
        'EcdcContinent',
        lazy='subquery',
        order_by='EcdcContinent.region',
        cascade="all, delete"
    )

    def __str__(self):
        result = " " + self.geo_id + " " + self.country_territory_code + " " + self.countries_and_territories + " "
        return result

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
    def find_by(cls, countries_and_territories, geo_id, country_territory_code):
        return db.session.query(cls).filter(and_(
            (cls.countries_and_territories == countries_and_territories),
            (cls.geo_id == geo_id),
            (cls.country_territory_code == country_territory_code)
        )).one()

    @classmethod
    def find_by_continent(cls, continent, page):
        return db.session.query(cls)\
            .filter(cls.continent_id == continent.id)\
            .paginate(page, per_page=ITEMS_PER_PAGE)

    @classmethod
    def get_germany(cls):
        return db.session.query(cls) \
            .filter(cls.country_territory_code == 'DEU') \
            .one_or_none()


class EcdcData(db.Model):
    __tablename__ = 'ecdc_data'

    id = db.Column(db.Integer, primary_key=True)
    deaths_weekly = db.Column(db.Integer, nullable=False)
    cases_weekly = db.Column(db.Integer, nullable=False)
    notification_rate_per_100000_population_14days = db.Column(db.Float, nullable=False)

    europe_country_id = db.Column(db.Integer, db.ForeignKey('ecdc_country.id'), nullable=False)
    europe_country = db.relationship('EcdcCountry', lazy='joined', cascade="all, delete")

    europe_date_reported_id = db.Column(db.Integer, db.ForeignKey('ecdc_date_reported.id'), nullable=False)
    europe_date_reported = db.relationship(
        'EcdcDateReported',
        lazy='joined',
        cascade='all, delete',
        order_by='desc(EcdcDateReported.date_reported)')

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
    def find_by_date_reported(cls, europe_date_reported, page):
        #TODO: * Issue #43 /europe/date_reported
        return db.session.query(cls).filter(
            cls.europe_date_reported_id == europe_date_reported.id)\
            .order_by(cls.notification_rate_per_100000_population_14days.desc())\
            .paginate(page, per_page=ITEMS_PER_PAGE)

    @classmethod
    def find_by_date_reported_notification_rate(cls, europe_date_reported, page):
        # TODO: * Issue #43 /europe/date_reported
        return db.session.query(cls).filter(
            cls.europe_date_reported_id == europe_date_reported.id) \
            .order_by(cls.notification_rate_per_100000_population_14days.desc()) \
            .paginate(page, per_page=ITEMS_PER_PAGE)

    @classmethod
    def find_by_date_reported_deaths_weekly(cls, europe_date_reported, page):
        # TODO: * Issue #43 /europe/date_reported
        return db.session.query(cls).filter(
            cls.europe_date_reported_id == europe_date_reported.id) \
            .order_by(cls.deaths_weekly.desc()) \
            .paginate(page, per_page=ITEMS_PER_PAGE)

    @classmethod
    def find_by_date_reported_cases_weekly(cls, europe_date_reported, page):
        # TODO: * Issue #43 /europe/date_reported
        return db.session.query(cls).filter(
            cls.europe_date_reported_id == europe_date_reported.id) \
            .order_by(cls.cases_weekly.desc()) \
            .paginate(page, per_page=ITEMS_PER_PAGE)

    @classmethod
    def find_by_country(cls, europe_country, page):
        return db.session.query(cls).filter(
            cls.europe_country_id == europe_country.id)\
            .paginate(page, per_page=ITEMS_PER_PAGE)
