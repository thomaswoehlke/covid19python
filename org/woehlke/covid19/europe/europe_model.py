from database import db, ITEMS_PER_PAGE


class EuropeDataImportTable(db.Model):
    __tablename__ = 'europe_data_import'

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
        db.session.execute("delete from " + cls.__tablename__)
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


class EuropeDateReported(db.Model):
    __tablename__ = 'europe_date_reported'

    id = db.Column(db.Integer, primary_key=True)
    date_rep = db.Column(db.String(255), nullable=False)
    day = db.Column(db.String(255), nullable=False)
    month = db.Column(db.String(255), nullable=False)
    year = db.Column(db.String(255), nullable=False)

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
        return db.session.query(cls).limit(500)

    @classmethod
    def get_by_id(cls, other_id):
        return db.session.query(cls).filter(cls.id == other_id).one()


class EuropeContinent(db.Model):
    __tablename__ = 'europe_continent'

    id = db.Column(db.Integer, primary_key=True)
    continent_exp = db.Column(db.String(255), nullable=False)

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
        return db.session.query(cls).limit(500)

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

    europe_continent_id = db.Column(db.Integer, db.ForeignKey('europe_continent.id'), nullable=False)
    europe_continent = db.relationship('EuropeContinent', lazy='joined')

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
        return db.session.query(cls).limit(500)

    @classmethod
    def get_by_id(cls, other_id):
        return db.session.query(cls).filter(cls.id == other_id).one()


class EuropeData(db.Model):
    __tablename__ = 'europe_data'

    id = db.Column(db.Integer, primary_key=True)
    deaths = db.Column(db.String(255), nullable=False)
    cases = db.Column(db.String(255), nullable=False)
    cases_cumulative_14days_per_100000 = db.Column(db.String(255), nullable=False)

    europe_country_id = db.Column(db.Integer, db.ForeignKey('europe_country.id'), nullable=False)
    europe_country = db.relationship('EuropeCountry', lazy='joined')

    europe_date_reported_id = db.Column(db.Integer, db.ForeignKey('europe_date_reported.id'), nullable=False)
    europe_date_reported = db.relationship('EuropeDateReported', lazy='joined')

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
        return db.session.query(cls).limit(500)

    @classmethod
    def get_by_id(cls, other_id):
        return db.session.query(cls).filter(cls.id == other_id).one()

