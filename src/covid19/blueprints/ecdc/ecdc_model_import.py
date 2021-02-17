from database import db, ITEMS_PER_PAGE


#dateRep,day,month,year,cases,deaths,countriesAndTerritories,geoId,countryterritoryCode,popData2019,continentExp,Cumulative_number_for_14_days_of_COVID-19_cases_per_100000
class EcdcImport(db.Model):
    __tablename__ = 'ecdc_import'

    id = db.Column(db.Integer, primary_key=True)
    date_rep = db.Column(db.String(255), nullable=False)
    day = db.Column(db.String(255), nullable=False)
    month = db.Column(db.String(255), nullable=False)
    year = db.Column(db.String(255), nullable=False)
    cases = db.Column(db.String(255), nullable=False)
    deaths = db.Column(db.String(255), nullable=False)
    pop_data_2019 = db.Column(db.String(255), nullable=False)
    countries_and_territories = db.Column(db.String(255), nullable=False)
    geo_id = db.Column(db.String(255), nullable=False)
    country_territory_code = db.Column(db.String(255), nullable=False)
    continent_exp = db.Column(db.String(255), nullable=False)
    cumulative_number_for_14_days_of_covid19_cases_per_100000 = db.Column(db.String(255), nullable=False)

    @classmethod
    def remove_all(cls):
        for one in cls.get_all():
            db.session.delete(one)
        db.session.commit()
        return None

    @classmethod
    def get_all_as_page(cls, page: int):
        return db.session.query(cls).order_by(
            #cls.year_week,
            cls.countries_and_territories
        ).paginate(page, per_page=ITEMS_PER_PAGE)

    @classmethod
    def get_all(cls):
        return db.session.query(cls).order_by(
            #cls.year_week,
            cls.countries_and_territories
        ).all()

    @classmethod
    def get_by_id(cls, other_id: int):
        return db.session.query(cls).filter(cls.id == other_id).one()

    @classmethod
    def get_date_rep(cls):
        # sql = "select distinct date_rep, year_week from edcd_import order by year_week desc"
        #return db.session.execute(sql).fetchall()
        return db.session.query(cls.date_rep) \
            .group_by(cls.date_rep)\
            .distinct() \
            .order_by(cls.date_rep.desc())\
            .all()

    @classmethod
    def get_continent(cls):
        # sql = "select distinct continent_exp from edcd_import order by continent_exp asc"
        #return db.session.execute(sql).fetchall()
        return db.session.query(cls.continent_exp) \
            .group_by(cls.continent_exp)\
            .distinct() \
            .order_by(cls.continent_exp.asc()) \
            .all()

    @classmethod
    def get_countries_of_continent(cls, my_continent):
        my_continent_exp = my_continent.region
        my_params = {}
        my_params['my_continent_param'] = my_continent_exp
        return db.session.query(
            cls.countries_and_territories,
            cls.pop_data_2019,
            cls.geo_id,
            cls.country_territory_code,
            cls.continent_exp,
        ).filter(
            cls.continent_exp == my_continent_exp
        ).distinct().group_by(
            cls.countries_and_territories,
            cls.pop_data_2019,
            cls.geo_id,
            cls.country_territory_code,
            cls.continent_exp
        ).order_by(cls.countries_and_territories.asc()).all()
        #sql = """
        #select distinct
        #    countries_and_territories,
        #    geo_id,
        #    pop_data_2019,
        #    continent_exp,
        #    country_territory_code
        #from
        #    ecdc_import
        #group by
        #    countries_and_territories,
        #    geo_id,
        #    country_territory_code,
        #    pop_data_2019,
        #    continent_exp,
        #    country_territory_code
        #having
        #    continent_exp = :my_continent_param
        #order by
        #    countries_and_territories
        #"""
        #return db.session.execute(sql, my_params).fetchall()

    @classmethod
    def find_by_date_reported(cls, p_edcd_date_reported_str: str = ''):
        return db.session.query(cls)\
            .filter(cls.date_rep == p_edcd_date_reported_str) \
            .all()
