from database import db, ITEMS_PER_PAGE


class EuropeDataImportTable(db.Model):
    __tablename__ = 'europe_data_import'

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
        # TODO: SQLalchemy instead of SQL
        db.session.execute("delete from " + cls.__tablename__ + " cascade")
        db.session.commit()
        return None

    @classmethod
    def get_all_as_page(cls, page):
        #TODO: #51 order_by: year_week, country
        return db.session.query(cls).paginate(page, per_page=ITEMS_PER_PAGE)

    @classmethod
    def get_all(cls):
        return db.session.query(cls).all()

    @classmethod
    def get_by_id(cls, other_id):
        return db.session.query(cls).filter(cls.id == other_id).one()

    @classmethod
    def get_date_rep(cls):
        #TODO: SQLalchemy instead of SQL
        sql = "select distinct date_rep, year_week from europe_data_import order by year_week desc"
        return db.session.execute(sql).fetchall()

    @classmethod
    def get_continent(cls):
        # TODO: SQLalchemy instead of SQL
        sql = "select distinct continent_exp from europe_data_import order by continent_exp asc"
        return db.session.execute(sql).fetchall()

    @classmethod
    def get_countries_of_continent(cls, my_continent):
        my_continent_exp = my_continent.continent_exp
        my_params = {}
        my_params['my_continent_param'] = my_continent_exp
        # TODO: SQLalchemy instead of SQL
        sql = """
        select distinct
            countries_and_territories,
            geo_id,
            country_territory_code,
            pop_data_2019,
            continent_exp
        from
            europe_data_import
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
