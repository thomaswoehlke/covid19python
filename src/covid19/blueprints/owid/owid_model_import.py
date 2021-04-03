from database import db, ITEMS_PER_PAGE


class OwidImport(db.Model):
    __tablename__ = 'import_owid'

    id = db.Column(db.Integer, primary_key=True)
    iso_code = db.Column(db.String(255), nullable=False)
    continent = db.Column(db.String(255), nullable=False)
    location = db.Column(db.String(255), nullable=False)
    date = db.Column(db.String(255), nullable=False)
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
        return db.session.query(cls).order_by(
            cls.date.desc()
        ).paginate(page, per_page=ITEMS_PER_PAGE)

    @classmethod
    def get_all(cls):
        return db.session.query(cls).order_by(
            cls.date.desc()
        ).all()

    @classmethod
    def get_by_id(cls, other_id):
        return db.session.query(cls)\
            .filter(cls.id == other_id)\
            .one()

    @classmethod
    def find_by_id(cls, other_id):
        return db.session.query(cls)\
            .filter(cls.id == other_id)\
            .one()

    @classmethod
    def get_dates(cls):
        return db.session.query(cls.date)\
            .order_by(cls.date.desc())\
            .distinct().all()

    @classmethod
    def get_for_one_day(cls, day):
        return db.session.query(cls)\
            .filter(cls.date == day)\
            .all()

    @classmethod
    def get_dates_reported_as_array(cls):
        myresultarray = []
        myresultset = db.session.query(cls.date)\
            .order_by(cls.date.desc())\
            .group_by(cls.date)\
            .distinct()
        for item, in myresultset:
            myresultarray.append(item)
        return myresultarray

    @classmethod
    def get_new_dates_reported_as_array(cls):
        return cls.get_dates_reported_as_array()

    @classmethod
    def get_continents(cls, page):
        return db.session.query(cls.continent)\
            .group_by(cls.continent) \
            .distinct()\
            .order_by(cls.continent.asc())\
            .paginate(page, per_page=ITEMS_PER_PAGE)
