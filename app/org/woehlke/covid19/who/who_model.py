from sqlalchemy import and_, func
from datetime import date
from database import db, ITEMS_PER_PAGE
from sqlalchemy.orm import joinedload


class WhoGlobalDataImportTable(db.Model):
    __tablename__ = 'who_global_data_import'

    id = db.Column(db.Integer, primary_key=True)
    date_reported = db.Column(db.String(255), nullable=False)
    country_code = db.Column(db.String(255), nullable=False)
    country = db.Column(db.String(255), nullable=False)
    who_region = db.Column(db.String(255), nullable=False)
    new_cases = db.Column(db.String(255), nullable=False)
    cumulative_cases = db.Column(db.String(255), nullable=False)
    new_deaths = db.Column(db.String(255), nullable=False)
    cumulative_deaths = db.Column(db.String(255), nullable=False)
    row_imported = db.Column(db.Boolean, nullable=False)

    @classmethod
    def remove_all(cls):
        # TODO: SQLalchemy instead of SQL
        db.session.execute("delete from " + cls.__tablename__)
        db.session.commit()
        return None

    @classmethod
    def get_all_as_page(cls, page):
        return db.session.query(cls).order_by(
            cls.date_reported.desc(),
            cls.country.asc()
        ).paginate(page, per_page=ITEMS_PER_PAGE)

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
        # TODO: SQLalchemy instead of SQL
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


class WhoDateReported(db.Model):
    __tablename__ = 'who_date_reported'

    id = db.Column(db.Integer, primary_key=True)
    date_reported = db.Column(db.String(255), nullable=False, unique=True)
    year_week = db.Column(db.String(255), nullable=False)
    datum = db.Column(db.Date, nullable=False, unique=True)
    year = db.Column(db.Integer, nullable=False)
    month = db.Column(db.Integer, nullable=False)
    day_of_month = db.Column(db.Integer, nullable=False)
    day_of_week = db.Column(db.Integer, nullable=False)
    week_of_year = db.Column(db.Integer, nullable=False)

    def __str__(self):
        result = ""
        if self.day_of_month < 10:
            result += "0" + str(self.day_of_month)
        else:
            result += "" + str(self.day_of_month)
        if self.month < 10:
            result += ".0" + str(self.month)
        else:
            result += "." + str(self.month)
        result += "." + str(self.year)
        return result

    def get_name_for_weekday(self):
        return self.get_names_for_weekday()[self.day_of_week]

    @classmethod
    def get_names_for_weekday(cls):
        return {1: "Montag", 2: "Dienstag", 3: "Mittwoch", 4: "Donnerstag", 5: "Freitag", 6: "Samstag",
                             7: "Sonntag"}

    @classmethod
    def create_new_object_factory(cls, my_date_rep):
        my_datum = date.fromisoformat(my_date_rep)
        (my_iso_year, week_number, weekday) = my_datum.isocalendar()
        if week_number < 10:
            my_year_week = "" + str(my_iso_year) + "-0"+str(week_number)
        else:
            my_year_week = "" + str(my_iso_year) + "-"+str(week_number)
        return WhoDateReported(
            date_reported=my_date_rep,
            datum=my_datum,
            year=my_datum.year,
            month=my_datum.month,
            day_of_month=my_datum.day,
            day_of_week=weekday,
            week_of_year=week_number,
            year_week=my_year_week
        )

    @classmethod
    def remove_all(cls):
        # TODO: SQLalchemy instead of SQL
        db.session.execute("delete from " + cls.__tablename__)
        db.session.commit()
        return None

    @classmethod
    def get_all_as_page(cls, page):
        return db.session.query(cls)\
            .order_by(cls.date_reported.desc())\
            .paginate(page, per_page=ITEMS_PER_PAGE)

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
        return db.session.query(cls)\
            .filter(cls.id == other_id)\
            .one()

    @classmethod
    def find_by_date_reported(cls, i_date_reported):
        return db.session.query(cls)\
            .filter(cls.date_reported == i_date_reported)\
            .one_or_none()


class WhoRegion(db.Model):
    __tablename__ = 'who_region'

    id = db.Column(db.Integer, primary_key=True)
    region = db.Column(db.String(255), unique=True)

    @classmethod
    def remove_all(cls):
        # TODO: SQLalchemy instead of SQL
        db.session.execute("delete from " + cls.__tablename__)
        db.session.commit()
        return None

    @classmethod
    def get_all(cls):
        return db.session.query(cls).all()

    @classmethod
    def get_all_as_page(cls, page):
        return db.session.query(cls)\
            .order_by(cls.region)\
            .paginate(page, per_page=ITEMS_PER_PAGE)

    @classmethod
    def get_all_as_dict(cls):
        regions = {}
        for my_region in cls.get_all():
            regions[my_region.region] = my_region
        return regions

    @classmethod
    def get_by_id(cls, other_id):
        return db.session.query(cls)\
            .filter(cls.id == other_id)\
            .one()

    @classmethod
    def find_by_region(cls, i_who_region):
        my_region = db.session.query(cls)\
            .filter(cls.region == i_who_region)\
            .one_or_none()
        return my_region


class WhoCountry(db.Model):
    __tablename__ = 'who_country'

    id = db.Column(db.Integer, primary_key=True)
    country_code = db.Column(db.String(255), unique=True, nullable=False)
    country = db.Column(db.String(255), unique=True, nullable=False)
    region_id = db.Column(db.Integer, db.ForeignKey('who_region.id'), nullable=False)
    region = db.relationship(
        'WhoRegion',
        lazy='joined',
        order_by='WhoRegion.region')

    @classmethod
    def remove_all(cls):
        # TODO: SQLalchemy instead of SQL
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
    def get_who_countries_for_region(cls, region, page):
        return db.session.query(cls).filter(
            cls.region == region
        ).order_by(cls.country).paginate(page, per_page=ITEMS_PER_PAGE)


class WhoGlobalData(db.Model):
    __tablename__ = 'who_global_data'

    id = db.Column(db.Integer, primary_key=True)
    cases_new = db.Column(db.Integer, nullable=False)
    cases_cumulative = db.Column(db.Integer, nullable=False)
    deaths_new = db.Column(db.Integer, nullable=False)
    deaths_cumulative = db.Column(db.Integer, nullable=False)
    date_reported_id = db.Column(db.Integer,
        db.ForeignKey('who_date_reported.id'), nullable=False)
    date_reported = db.relationship(
        'WhoDateReported',
        lazy='joined',
        order_by='desc(WhoDateReported.date_reported)')
    country_id = db.Column(db.Integer,
        db.ForeignKey('who_country.id'), nullable=False)
    country = db.relationship(
        'WhoCountry',
        lazy='joined',
        order_by='asc(WhoCountry.country)')

    @classmethod
    def remove_all(cls):
        # TODO: SQLalchemy instead of SQL
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
            joinedload(cls.country).joinedload(WhoCountry.region),
            joinedload(cls.date_reported)
        ).paginate(page, per_page=ITEMS_PER_PAGE)

    @classmethod
    def get_data_for_day(cls, date_reported, page):
        return db.session.query(cls).filter(
                cls.date_reported_id == date_reported.id
            ).populate_existing().options(
                joinedload(cls.country).joinedload(WhoCountry.region),
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
                joinedload(cls.country).joinedload(WhoCountry.region),
                joinedload(cls.date_reported)
            ).order_by(
                cls.cases_new.desc()
            ).paginate(page, per_page=ITEMS_PER_PAGE)

    @classmethod
    def get_data_for_day_order_by_cases_cumulative(cls, date_reported, page):
        return db.session.query(cls).filter(
                cls.date_reported_id == date_reported.id
            ).populate_existing().options(
                joinedload(cls.country).joinedload(WhoCountry.region),
                joinedload(cls.date_reported)
            ).order_by(
                cls.cases_cumulative.desc()
            ).paginate(page, per_page=ITEMS_PER_PAGE)

    @classmethod
    def get_data_for_day_order_by_deaths_new(cls, date_reported, page):
        return db.session.query(cls).filter(
                cls.date_reported_id == date_reported.id
            ).populate_existing().options(
                joinedload(cls.country).joinedload(WhoCountry.region),
                joinedload(cls.date_reported)
            ).order_by(
                cls.deaths_new.desc()
            ).paginate(page, per_page=ITEMS_PER_PAGE)

    @classmethod
    def get_data_for_day_order_by_deaths_cumulative(cls, date_reported, page):
        return db.session.query(cls).filter(
                cls.date_reported_id == date_reported.id
            ).populate_existing().options(
                joinedload(cls.country).joinedload(WhoCountry.region),
                joinedload(cls.date_reported)
            ).order_by(
                cls.deaths_cumulative.desc()
            ).paginate(page, per_page=ITEMS_PER_PAGE)

    @classmethod
    def get_data_for_country_order_by_cases_new(cls, who_country, page):
        return db.session.query(cls).filter(
            cls.country_id == who_country.id
        ).populate_existing().options(
            joinedload(cls.country).joinedload(WhoCountry.region),
            joinedload(cls.date_reported)
        ).order_by(
            cls.cases_new.desc()
        ).paginate(page, per_page=ITEMS_PER_PAGE)

    @classmethod
    def get_data_for_country_order_by_cases_cumulative(cls, who_country, page):
        return db.session.query(cls).filter(
            cls.country_id == who_country.id
        ).populate_existing().options(
            joinedload(cls.country).joinedload(WhoCountry.region),
            joinedload(cls.date_reported)
        ).order_by(
            cls.cases_cumulative.desc()
        ).paginate(page, per_page=ITEMS_PER_PAGE)

    @classmethod
    def get_data_for_country_order_by_deaths_new(cls, who_country, page):
        return db.session.query(cls).filter(
            cls.country_id == who_country.id
        ).populate_existing().options(
            joinedload(cls.country).joinedload(WhoCountry.region),
            joinedload(cls.date_reported)
        ).order_by(
            cls.deaths_new.desc()
        ).paginate(page, per_page=ITEMS_PER_PAGE)

    @classmethod
    def get_data_for_country_order_by_deaths_cumulative(cls, who_country, page):
        return db.session.query(cls).filter(
            cls.country_id == who_country.id
        ).populate_existing().options(
            joinedload(cls.country).joinedload(WhoCountry.region),
            joinedload(cls.date_reported)
        ).order_by(
            cls.deaths_cumulative.desc()
        ).paginate(page, per_page=ITEMS_PER_PAGE)
