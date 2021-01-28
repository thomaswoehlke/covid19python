from sqlalchemy import and_, func
from datetime import date
from database import db, ITEMS_PER_PAGE
from sqlalchemy.orm import joinedload, raiseload


class RkiGermanyDataImportTable(db.Model):
    __tablename__ = 'rki_global_data_import'

    id = db.Column(db.Integer, primary_key=True)
    date_reported = db.Column(db.String(255), nullable=False)
    country_code = db.Column(db.String(255), nullable=False)
    country = db.Column(db.String(255), nullable=False)
    who_region = db.Column(db.String(255), nullable=False)
    new_cases = db.Column(db.String(255), nullable=False)
    cumulative_cases = db.Column(db.String(255), nullable=False)
    new_deaths = db.Column(db.String(255), nullable=False)
    cumulative_deaths = db.Column(db.String(255), nullable=False)

    @classmethod
    def remove_all(cls):
        db.session.execute("delete from " + cls.__tablename__)
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
    def get_regions(cls):
        return db.session.query(cls.who_region).distinct()

    @classmethod
    def get_dates_reported(cls):
        return db.session.query(cls.date_reported).distinct()

    @classmethod
    def get_for_one_day(cls, day):
        return db.session.query(cls).filter(cls.date_reported == day).all()

    @classmethod
    def get_new_dates_as_array(cls):
        sql_query = """
            select
                date_reported
            from
                who_global_data_import
            where
                date_reported
            not in (
            select
                distinct
                    who_date_reported.date_reported
                from
                    who_global_data
                left join
                    who_date_reported
                on
                    who_global_data.date_reported_id=who_date_reported.id
            )
            group by
                who_global_data_import.date_reported
            order by date_reported desc
            """
        new_dates = []
        for item in db.session.execute(sql_query):
            new_dates.append(item['date_reported'])
        return new_dates


class RkiDateReported(db.Model):
    __tablename__ = 'rki_date_reported'

    id = db.Column(db.Integer, primary_key=True)
    date_reported = db.Column(db.String(255), nullable=False, unique=True)
    datum = db.Column(db.Date, nullable=False, unique=True)
    year = db.Column(db.Integer, nullable=False)
    month = db.Column(db.Integer, nullable=False)
    day_of_month = db.Column(db.Integer, nullable=False)
    day_of_week = db.Column(db.Integer, nullable=False)
    week_of_year = db.Column(db.Integer, nullable=False)
    year_week = db.Column(db.String(255), nullable=False, unique=True)

    @classmethod
    def create_new_object_factory(cls, my_date_rep):
        my_date_reported = my_date_rep.split('/')
        my_year = int(my_date_reported[0])
        my_month = int(my_date_reported[1])
        my_day_of_month = int(my_date_reported[2])
        my_datum = date(year=my_year, month=my_month, day=my_day_of_month)
        (my_iso_year, week_number, weekday) = my_datum.isocalendar()
        if week_number < 10:
            my_year_week = "" + str(my_year) + "-0"+str(week_number)
        else:
            my_year_week = "" + str(my_year) + "-"+str(week_number)
        return RkiDateReported(
            date_rep=my_date_rep,
            year_week=my_year_week,
            datum=my_datum,
            year=my_datum.year,
            month=my_datum.month,
            day_of_month=my_datum.day,
            day_of_week=weekday,
            week_of_year=week_number
        )

    @classmethod
    def remove_all(cls):
        db.session.execute("delete from " + cls.__tablename__)
        db.session.commit()
        return None

    @classmethod
    def get_all_as_page(cls, page):
        return db.session.query(cls).order_by(cls.date_reported.desc()).paginate(page, per_page=ITEMS_PER_PAGE)

    @classmethod
    def get_all(cls):
        return db.session.query(cls).all()

    @classmethod
    def get_all_as_dict(cls):
        dates_reported = {}
        for my_date_reported in cls.get_all():
            dates_reported[my_date_reported.date_reported] = my_date_reported
        return dates_reported

    @classmethod
    def get_by_id(cls, other_id):
        return db.session.query(cls).filter(cls.id == other_id).one()

    @classmethod
    def find_by_date_reported(cls, i_date_reported):
        return db.session.query(cls).filter(cls.date_reported == i_date_reported).one_or_none()


class RkiRegion(db.Model):
    __tablename__ = 'rki_region'

    id = db.Column(db.Integer, primary_key=True)
    region = db.Column(db.String(255), unique=True)

    @classmethod
    def remove_all(cls):
        db.session.execute("delete from " + cls.__tablename__)
        db.session.commit()
        return None

    @classmethod
    def get_all(cls):
        return db.session.query(cls).all()

    @classmethod
    def get_all_as_page(cls, page):
        return db.session.query(cls).order_by(cls.region).paginate(page, per_page=ITEMS_PER_PAGE)

    @classmethod
    def get_all_as_dict(cls):
        regions = {}
        for my_region in cls.get_all():
            regions[my_region.region] = my_region
        return regions

    @classmethod
    def get_by_id(cls, other_id):
        return db.session.query(cls).filter(cls.id == other_id).one()

    @classmethod
    def find_by_region(cls, i_who_region):
        my_region = db.session.query(cls).filter(cls.region == i_who_region).one_or_none()
        return my_region


class RkiCountry(db.Model):
    __tablename__ = 'rki_country'

    id = db.Column(db.Integer, primary_key=True)
    country_code = db.Column(db.String(255), unique=True, nullable=False)
    country = db.Column(db.String(255), unique=True, nullable=False)
    region_id = db.Column(db.Integer, db.ForeignKey('who_region.id'), nullable=False)
    region = db.relationship(
        'WhoRegion',
        lazy='subquery',
        order_by='WhoRegion.region')

    @classmethod
    def remove_all(cls):
        db.session.execute("delete from " + cls.__tablename__)
        db.session.commit()
        return None

    @classmethod
    def get_all_as_page(cls, page):
        return db.session.query(cls).order_by(cls.country).paginate(page, per_page=ITEMS_PER_PAGE)

    @classmethod
    def get_all(cls):
        return db.session.query(cls).order_by(cls.country).all()

    @classmethod
    def get_all_as_dict(cls):
        countries = {}
        for my_country in cls.get_all():
            countries[my_country.country_code] = my_country
        return countries

    @classmethod
    def get_by_id(cls, other_id):
        return db.session.query(cls).filter(cls.id == other_id).one()

    @classmethod
    def get_germany(cls):
        return db.session.query(cls).filter(cls.country_code == 'DE').one()

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
    def get_who_countries_for_region(cls, region, page):
        return db.session.query(cls).filter(
            cls.region == region
        ).order_by(cls.country).paginate(page, per_page=ITEMS_PER_PAGE)


class RkiGermanyData(db.Model):
    __tablename__ = 'rki_global_data'

    id = db.Column(db.Integer, primary_key=True)
    cases_new = db.Column(db.Integer, nullable=False)
    cases_cumulative = db.Column(db.Integer, nullable=False)
    deaths_new = db.Column(db.Integer, nullable=False)
    deaths_cumulative = db.Column(db.Integer, nullable=False)
    date_reported_id = db.Column(db.Integer,
        db.ForeignKey('who_date_reported.id'), nullable=False)
    date_reported = db.relationship(
        'WhoDateReported', lazy='joined', order_by='desc(WhoDateReported.date_reported)')
    country_id = db.Column(db.Integer,
        db.ForeignKey('who_country.id'), nullable=False)
    country = db.relationship(
        'WhoCountry', lazy='joined', order_by='asc(WhoCountry.country)')

    @classmethod
    def remove_all(cls):
        db.session.execute("delete from " + cls.__tablename__)
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
    def get_data_for_country(cls, who_country, page):
        return db.session.query(cls).filter(
            cls.country_id == who_country.id
        ).populate_existing().options(
            joinedload(cls.country).subqueryload(RkiCountry.region),
            joinedload(cls.date_reported)
        ).paginate(page, per_page=ITEMS_PER_PAGE)

    @classmethod
    def get_data_for_day(cls, date_reported, page):
        return db.session.query(cls).filter(
                cls.date_reported_id == date_reported.id
            ).populate_existing().options(
                joinedload(cls.country).subqueryload(RkiCountry.region),
                joinedload(cls.date_reported)
            ).order_by(
                cls.deaths_new.desc(),
                cls.cases_new.desc(),
                cls.deaths_cumulative.desc(),
                cls.cases_cumulative.desc()
            ).paginate(page, per_page=ITEMS_PER_PAGE)
