from sqlalchemy import and_
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
    row_imported = db.Column(db.Boolean, nullable=False, default=False)

    @classmethod
    def remove_all(cls):
        # TODO: SQLalchemy instead of SQL
        db.session.execute("delete from " + cls.__tablename__ + " cascade")
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


class EuropeDateReported(db.Model):
    __tablename__ = 'europe_date_reported'

    id = db.Column(db.Integer, primary_key=True)
    date_rep = db.Column(db.String(255), nullable=False)
    year_week = db.Column(db.String(255), nullable=False, unique=True)

    @classmethod
    def remove_all(cls):
        # TODO: SQLalchemy instead of SQL
        db.session.execute("delete from " + cls.__tablename__ + " cascade")
        db.session.commit()
        return None

    @classmethod
    def get_all_as_page(cls, page):
        return db.session.query(cls).paginate(page, per_page=ITEMS_PER_PAGE)

    @classmethod
    def get_all(cls):
        return db.session.query(cls).limit(500)

    @classmethod
    def get_by_id(cls, other_id):
        return db.session.query(cls).filter(cls.id == other_id).one()

    @classmethod
    def find_by(cls, year_week):
        return db.session.query(cls).filter(cls.year_week == year_week).one()


class EuropeContinent(db.Model):
    __tablename__ = 'europe_continent'

    id = db.Column(db.Integer, primary_key=True)
    continent_exp = db.Column(db.String(255), nullable=False)

    @classmethod
    def remove_all(cls):
        # TODO: SQLalchemy instead of SQL
        db.session.execute("delete from " + cls.__tablename__ + " cascade")
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


class EuropeCountry(db.Model):
    __tablename__ = 'europe_country'

    id = db.Column(db.Integer, primary_key=True)
    countries_and_territories = db.Column(db.String(255), nullable=False)
    pop_data_2019 = db.Column(db.String(255), nullable=False)
    geo_id = db.Column(db.String(255), nullable=False)
    country_territory_code = db.Column(db.String(255), nullable=False)

    continent_id = db.Column(db.Integer, db.ForeignKey('europe_continent.id'), nullable=False)
    continent = db.relationship('EuropeContinent', lazy='subquery', order_by='EuropeContinent.continent_exp')

    @classmethod
    def remove_all(cls):
        # TODO: SQLalchemy instead of SQL
        db.session.execute("delete from " + cls.__tablename__ + " cascade")
        db.session.commit()
        return None

    @classmethod
    def get_all_as_page(cls, page):
        return db.session.query(cls).paginate(page, per_page=ITEMS_PER_PAGE)

    @classmethod
    def get_all(cls):
        return db.session.query(cls).limit(500)

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


class EuropeData(db.Model):
    __tablename__ = 'europe_data'

    id = db.Column(db.Integer, primary_key=True)
    deaths_weekly = db.Column(db.Integer, nullable=False)
    cases_weekly = db.Column(db.Integer, nullable=False)
    notification_rate_per_100000_population_14days = db.Column(db.Float, nullable=False)

    europe_country_id = db.Column(db.Integer, db.ForeignKey('europe_country.id'), nullable=False)
    europe_country = db.relationship('EuropeCountry', lazy='joined')

    europe_date_reported_id = db.Column(db.Integer, db.ForeignKey('europe_date_reported.id'), nullable=False)
    europe_date_reported = db.relationship('EuropeDateReported', lazy='joined')

    @classmethod
    def remove_all(cls):
        # TODO: SQLalchemy instead of SQL
        db.session.execute("delete from " + cls.__tablename__ + " cascade")
        db.session.commit()
        return None

    @classmethod
    def get_all_as_page(cls, page):
        return db.session.query(cls).paginate(page, per_page=ITEMS_PER_PAGE)

    @classmethod
    def get_all(cls):
        return db.session.query(cls).limit(500)

    @classmethod
    def get_by_id(cls, other_id):
        return db.session.query(cls).filter(cls.id == other_id).one()

    @classmethod
    def find_by_date_reported(cls, europe_date_reported, page):
        return db.session.query(cls).filter(
            cls.europe_date_reported_id == europe_date_reported.id).paginate(page, per_page=ITEMS_PER_PAGE)

    @classmethod
    def find_by_country(cls, europe_country, page):
        return db.session.query(cls).filter(
            cls.europe_country_id == europe_country.id).paginate(page, per_page=ITEMS_PER_PAGE)

