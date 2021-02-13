from database import db, ITEMS_PER_PAGE


class EcdcImport(db.Model):
    __tablename__ = 'ecdc_import'

    id = db.Column(db.Integer, primary_key=True)
    date_rep = db.Column(db.String(255), nullable=False)
    year_week = db.Column(db.String(255), nullable=False)
    cases_weekly = db.Column(db.String(255), nullable=False)
    deaths_weekly = db.Column(db.String(255), nullable=False)
    pop_data_2019 = db.Column(db.String(255), nullable=False)
    countries_and_territories = db.Column(db.String(255), nullable=False)
    geo_id = db.Column(db.String(255), nullable=False)
    country_territory_code = db.Column(db.String(255), nullable=False)
    continent_exp = db.Column(db.String(255), nullable=False)
    notification_rate_per_100000_population_14days = db.Column(db.String(255), nullable=False)

    @classmethod
    def remove_all(cls):
        for one in cls.get_all():
            db.session.delete(one)
        db.session.commit()
        return None

    @classmethod
    def get_all_as_page(cls, page: int):
        return db.session.query(cls).order_by(
            cls.year_week,
            cls.countries_and_territories
        ).paginate(page, per_page=ITEMS_PER_PAGE)

    @classmethod
    def get_all(cls):
        return db.session.query(cls).order_by(
            cls.year_week,
            cls.countries_and_territories
        ).all()

    @classmethod
    def get_by_id(cls, other_id: int):
        return db.session.query(cls).filter(cls.id == other_id).one()

    @classmethod
    def get_date_rep(cls):
        # TODO: #109 SQLalchemy instead of SQL in: EcdcImport.get_date_rep
        # sql = "select distinct date_rep, year_week from edcd_import order by year_week desc"
        #return db.session.execute(sql).fetchall()
        return db.session.query(cls.date_rep) \
            .group_by(cls.date_rep) \
            .order_by(cls.date_rep.desc())\
            .distinct().all()

    @classmethod
    def get_continent(cls):
        # TODO: #110 SQLalchemy instead of SQL in: EcdcImport.get_continent
        # sql = "select distinct continent_exp from edcd_import order by continent_exp asc"
        #return db.session.execute(sql).fetchall()
        return db.session.query(cls.continent_exp) \
            .group_by(cls.continent_exp) \
            .order_by(cls.continent_exp.asc()) \
            .distinct().all()

    @classmethod
    def get_countries_of_continent(cls, my_continent: str):
        my_continent_exp = my_continent.region
        my_params = {}
        my_params['my_continent_param'] = my_continent_exp
        #TODO: #107 SQLalchemy instead of SQL in: EcdcImport.get_countries_of_continent
        #TODO: #108 BUG: change to ORM ClassHierarchy in: EcdcImport.get_countries_of_continent
        #return db.session.query(
        #    cls.countries_and_territories,
        #    cls.geo_id,
        #    cls.country_territory_code,
        #    cls.pop_data_2019,
        #    cls.continent_exp
        #).group_by(
        #    cls.countries_and_sterritories,
        #    cls.geo_id,
        #    cls.country_territory_code,
        #    cls.pop_data_2019,
        #    cls.continent_exp
        #).order_by(cls.countries_and_territories.asc()).filter(
        #    cls.continent_exp == my_continent
        #).distinct().all()
        sql = """
        select distinct
            countries_and_territories,
            geo_id,
             pop_data_2019,
            continent_exp
        from
            ecdc_import
        group by
            countries_and_territories,
            geo_id,
            country_territory_code,
            pop_data_2019,
            continent_exp
        having
            continent_exp = :my_continent_param
        order by
            countries_and_territories
        """
        return db.session.execute(sql, my_params).fetchall()

    @classmethod
    def find_by_date_reported(cls, europe_date_reported):
        return db.session.query(cls).filter(cls.year_week == europe_date_reported.year_week).all()
