from flask_sqlalchemy import Pagination
from sqlalchemy import and_, func
from database import db, ITEMS_PER_PAGE


class WhoRegion(db.Model):
    __tablename__ = 'who_region'

    id = db.Column(db.Integer, primary_key=True)
    who_region = db.Column(db.String(255), unique=True, nullable=False)

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
        return db.session.query(cls).order_by(cls.who_region).paginate(page, per_page=ITEMS_PER_PAGE)

    @classmethod
    def get_all_as_dict(cls):
        regions = {}
        for my_region in cls.get_all():
            regions[my_region.who_region] = my_region
        return regions

    @classmethod
    def get_by_id(cls, other_id):
        return db.session.query(cls).filter(cls.id == other_id).one()

    @classmethod
    def find_by_region(cls, i_who_region):
        my_region = db.session.query(cls).filter(cls.who_region == i_who_region).one_or_none()
        return my_region


class WhoDateReported(db.Model):
    __tablename__ = 'who_date_reported'

    id = db.Column(db.Integer, primary_key=True)
    date_reported = db.Column(db.String(255), unique=True, nullable=False)

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

    @classmethod
    def get_joungest_date(cls):
        return db.session.query(func.max(cls.date_reported)).one_or_none()


class WhoCountry(db.Model):
    __tablename__ = 'who_country'

    id = db.Column(db.Integer, primary_key=True)
    country_code = db.Column(db.String(255), unique=True, nullable=False)
    country = db.Column(db.String(255), unique=False, nullable=False)
    who_region_id = db.Column(db.Integer, db.ForeignKey('who_region.id'), nullable=False)
    who_region = db.relationship('WhoRegion', lazy='joined')

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
                cls.who_region_id == my_region.id
            )
        ).one_or_none()

    @classmethod
    def get_who_countries_for_region(cls, region, page):
        return db.session.query(cls).filter(
            cls.who_region == region
        ).order_by(cls.country).paginate(page, per_page=ITEMS_PER_PAGE)


class WhoGlobalData(db.Model):
    __tablename__ = 'who_global_data'

    id = db.Column(db.Integer, primary_key=True)
    cases_new = db.Column(db.Integer, nullable=False)
    cases_cumulative = db.Column(db.Integer, nullable=False)
    deaths_new = db.Column(db.Integer, nullable=False)
    deaths_cumulative = db.Column(db.Integer, nullable=False)

    date_reported_id = db.Column(db.Integer, db.ForeignKey('who_date_reported.id'), nullable=False)
    date_reported = db.relationship('WhoDateReported', lazy='joined')

    country_id = db.Column(db.Integer, db.ForeignKey('who_country.id'), nullable=False)
    country = db.relationship('WhoCountry', lazy='joined')

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
                cls.who_date_reported_id == my_date_reported.id,
                cls.who_country_id == my_country.id
            )
        ).one_or_none()

    @classmethod
    def get_data_for_country(cls, who_country, page):
        sql_query_parameter = {
            "country_id": who_country.id
        }
        sql_query = """
                   select * from who_global_data
                   left join who_date_reported 
                   on who_global_data.who_date_reported_id = who_date_reported.id
                   where who_country_id = :country_id 
                   order by who_date_reported.date_reported DESC
                   """
        total_items = db.session.execute(sql_query, sql_query_parameter)
        total = len(total_items.fetchall())
        offset = ITEMS_PER_PAGE*(page-1)
        sql_query_page_parameter = {
            'country_id': who_country.id,
            'ITEMS_PER_PAGE': ITEMS_PER_PAGE,
            'OFFSET_FOR_PAGE': offset
        }
        sql_query_page = """
                       select * from who_global_data
                       left join who_date_reported 
                       on who_global_data.who_date_reported_id = who_date_reported.id
                       where who_country_id = :country_id 
                       order by who_date_reported.date_reported DESC
                       limit :ITEMS_PER_PAGE
                       offset :OFFSET_FOR_PAGE
                       """
        items_page = db.session.execute(sql_query_page, sql_query_page_parameter)
        p = Pagination(sql_query, page, ITEMS_PER_PAGE, total, items_page)
        return p

    @classmethod
    def get_data_for_day(cls, date_reported, page):
        return db.session.query(cls)\
            .filter(cls.who_date_reported_id == date_reported.id)\
            .order_by(
                cls.deaths_new.desc(),
                cls.cases_new.desc(),
                cls.deaths_cumulative.desc(),
                cls.cases_cumulative.desc())\
            .paginate(page, per_page=ITEMS_PER_PAGE)


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
    def get_jounger_dates(cls, joungest_date_old):
        return db.session.query(cls).filter(cls.date_reported > joungest_date_old).all()

    @classmethod
    def get_new_dates_reported_as_dict(cls):
        new_dates_reported = []
        joungest_date_old = WhoDateReported.get_joungest_date()
        jounger_dates = None
        if joungest_date_old is None:
            jounger_dates = cls.get_dates_reported()
        else:
            jounger_dates = cls.get_jounger_dates(joungest_date_old)
        for jounger_date in jounger_dates:
            new_dates_reported.append(jounger_date.date_reported)
        return new_dates_reported

    @classmethod
    def get_for_one_day(cls, day):
        return db.session.query(cls).filter(cls.date_reported == day).all()
