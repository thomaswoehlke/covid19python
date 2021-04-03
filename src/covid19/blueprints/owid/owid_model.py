from sqlalchemy import and_, func
from datetime import date
from database import db, ITEMS_PER_PAGE
from sqlalchemy.orm import joinedload
from covid19.blueprints.application.application_model import ApplicationDateReported


class OwidDateReported(ApplicationDateReported):
    __tablename__ = 'owid_date_reported'
    __mapper_args__ = {'concrete': True}
    __table_args__ = (
        db.UniqueConstraint('date_reported', 'datum', name="uix_owid_date_reported"),
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
        return OwidDateReported(
            date_reported=my_date_rep,
            datum=my_datum,
            year=my_datum.year,
            month=my_datum.month,
            day_of_month=my_datum.day,
            day_of_week=weekday,
            week_of_year=week_number,
            year_week=my_year_week
        )


class OwidContinent(db.Model):
    __tablename__ = 'owid_country_continent'

    id = db.Column(db.Integer, primary_key=True)
    continent = db.Column(db.String(255), nullable=False, unique=True)

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


class OwidCountry(db.Model):
    __tablename__ = 'owid_country'

    id = db.Column(db.Integer, primary_key=True)
    continent_id = db.Column(db.Integer,
        db.ForeignKey('owid_country_continent.id'), nullable=False)
    continent = db.relationship(
        'OwidContinent',
        lazy='joined',
        cascade='all, delete',
        order_by='desc(OwidContinent.continent)')
    iso_code = db.Column(db.String(255), nullable=False)
    location = db.Column(db.String(255), nullable=False)
    stringency_index = db.Column(db.String(255), nullable=False)
    population = db.Column(db.String(255), nullable=False)
    population_density = db.Column(db.String(255), nullable=False)
    median_age = db.Column(db.String(255), nullable=False)
    aged_65_older = db.Column(db.String(255), nullable=False)
    aged_70_older = db.Column(db.String(255), nullable=False)
    gdp_per_capita = db.Column(db.String(255), nullable=False)
    extreme_poverty = db.Column(db.String(255), nullable=False)
    cardiovasc_death_rate = db.Column(db.String(255), nullable=False)
    diabetes_prevalence = db.Column(db.String(255), nullable=False)
    female_smokers = db.Column(db.String(255), nullable=False)
    male_smokers = db.Column(db.String(255), nullable=False)
    handwashing_facilities = db.Column(db.String(255), nullable=False)
    hospital_beds_per_thousand = db.Column(db.String(255), nullable=False)
    life_expectancy = db.Column(db.String(255), nullable=False)
    human_development_index = db.Column(db.String(255), nullable=False)

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


class OwidData(db.Model):
    __tablename__ = 'owid'

    id = db.Column(db.Integer, primary_key=True)
    date_reported_id = db.Column(db.Integer,
        db.ForeignKey('owid_date_reported.id'), nullable=False)
    date_reported = db.relationship(
        'OwidDateReported',
        lazy='joined',
        cascade='all, delete',
        order_by='desc(OwidDateReported.date_reported)')
    country_id = db.Column(db.Integer,
        db.ForeignKey('owid_country.id'), nullable=False)
    country = db.relationship(
        'OwidCountry',
        lazy='joined',
        cascade='all, delete',
        order_by='desc(OwidCountry.location)')
    total_cases = db.Column(db.String(255), nullable=False)
    new_cases = db.Column(db.String(255), nullable=False)
    new_cases_smoothed = db.Column(db.String(255), nullable=False)
    total_deaths = db.Column(db.String(255), nullable=False)
    new_deaths = db.Column(db.String(255), nullable=False)
    new_deaths_smoothed = db.Column(db.String(255), nullable=False)
    total_cases_per_million = db.Column(db.String(255), nullable=False)
    new_cases_per_million = db.Column(db.String(255), nullable=False)
    new_cases_smoothed_per_million = db.Column(db.String(255), nullable=False)
    total_deaths_per_million = db.Column(db.String(255), nullable=False)
    new_deaths_per_million = db.Column(db.String(255), nullable=False)
    new_deaths_smoothed_per_million = db.Column(db.String(255), nullable=False)
    reproduction_rate = db.Column(db.String(255), nullable=False)
    icu_patients = db.Column(db.String(255), nullable=False)
    icu_patients_per_million = db.Column(db.String(255), nullable=False)
    hosp_patients = db.Column(db.String(255), nullable=False)
    hosp_patients_per_million = db.Column(db.String(255), nullable=False)
    weekly_icu_admissions = db.Column(db.String(255), nullable=False)
    weekly_icu_admissions_per_million = db.Column(db.String(255), nullable=False)
    weekly_hosp_admissions = db.Column(db.String(255), nullable=False)
    weekly_hosp_admissions_per_million = db.Column(db.String(255), nullable=False)
    new_tests = db.Column(db.String(255), nullable=False)
    total_tests = db.Column(db.String(255), nullable=False)
    total_tests_per_thousand = db.Column(db.String(255), nullable=False)
    new_tests_per_thousand = db.Column(db.String(255), nullable=False)
    new_tests_smoothed = db.Column(db.String(255), nullable=False)
    new_tests_smoothed_per_thousand = db.Column(db.String(255), nullable=False)
    positive_rate = db.Column(db.String(255), nullable=False)
    tests_per_case = db.Column(db.String(255), nullable=False)
    tests_units = db.Column(db.String(255), nullable=False)
    total_vaccinations = db.Column(db.String(255), nullable=False)
    people_vaccinated = db.Column(db.String(255), nullable=False)
    people_fully_vaccinated = db.Column(db.String(255), nullable=False)
    new_vaccinations = db.Column(db.String(255), nullable=False)
    new_vaccinations_smoothed = db.Column(db.String(255), nullable=False)
    total_vaccinations_per_hundred = db.Column(db.String(255), nullable=False)
    people_vaccinated_per_hundred = db.Column(db.String(255), nullable=False)
    people_fully_vaccinated_per_hundred = db.Column(db.String(255), nullable=False)
    new_vaccinations_smoothed_per_million = db.Column(db.String(255), nullable=False)
    stringency_index = db.Column(db.String(255), nullable=False)

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
    def get_data_for_day(cls, date_reported, page):
        return db.session.query(cls).filter(
                cls.date_reported_id == date_reported.id
            ).populate_existing().options(
                joinedload(cls.date_reported)
            ).order_by(
                cls.new_deaths.desc(),
                cls.new_cases.desc(),
                cls.new_deaths_per_million.desc(),
                cls.new_cases_per_million.desc()
            ).paginate(page, per_page=ITEMS_PER_PAGE)

    @classmethod
    def get_data_for_day_order_by_deaths_new(cls, date_reported, page):
        pass

    @classmethod
    def get_data_for_day_order_by_deaths_cumulative(cls, date_reported, page):
        pass

    @classmethod
    def get_data_for_day_order_by_cases_cumulative(cls, date_reported, page):
        pass

    @classmethod
    def get_data_for_day_order_by_cases_new(cls, date_reported, page):
        pass
