from flask_sqlalchemy import Pagination
from sqlalchemy import and_, func
from database import db, ITEMS_PER_PAGE
from sqlalchemy.orm import joinedload, raiseload


class VaccinationDateReported(db.Model):
    __tablename__ = 'vaccination_date_reported'

    id = db.Column(db.Integer, primary_key=True)
    date_reported = db.Column(db.String(255), nullable=False, unique=True)

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


class VaccinationRegion(db.Model):
    __tablename__ = 'vaccination_region'

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


class VaccinationCountry(db.Model):
    __tablename__ = 'vaccination_country'

    id = db.Column(db.Integer, primary_key=True)
    country_code = db.Column(db.String(255), unique=True, nullable=False)
    country = db.Column(db.String(255), unique=True, nullable=False)
    region_id = db.Column(db.Integer, db.ForeignKey('vaccination_region.id'), nullable=False)
    region = db.relationship(
        'VaccinationRegion',
        lazy='subquery',
        order_by='VaccinationRegion.region')

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


class VaccinationData(db.Model):
    __tablename__ = 'vaccination_global_data'

    id = db.Column(db.Integer, primary_key=True)
    cases_new = db.Column(db.Integer, nullable=False)
    cases_cumulative = db.Column(db.Integer, nullable=False)
    deaths_new = db.Column(db.Integer, nullable=False)
    deaths_cumulative = db.Column(db.Integer, nullable=False)
    date_reported_id = db.Column(db.Integer,
        db.ForeignKey('vaccination_date_reported.id'), nullable=False)
    date_reported = db.relationship(
        'VaccinationDateReported', lazy='joined', order_by='desc(VaccinationDateReported.date_reported)')
    country_id = db.Column(db.Integer,
        db.ForeignKey('vaccination_country.id'), nullable=False)
    country = db.relationship(
        'VaccinationCountry', lazy='joined', order_by='asc(VaccinationCountry.country)')

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
            joinedload(cls.country).subqueryload(VaccinationCountry.region),
            joinedload(cls.date_reported)
        ).paginate(page, per_page=ITEMS_PER_PAGE)

    @classmethod
    def get_data_for_day(cls, date_reported, page):
        return db.session.query(cls).filter(
                cls.date_reported_id == date_reported.id
            ).populate_existing().options(
                joinedload(cls.country).subqueryload(VaccinationCountry.region),
                joinedload(cls.date_reported)
            ).order_by(
                cls.deaths_new.desc(),
                cls.cases_new.desc(),
                cls.deaths_cumulative.desc(),
                cls.cases_cumulative.desc()
            ).paginate(page, per_page=ITEMS_PER_PAGE)


class VaccinationDataImportTable(db.Model):
    __tablename__ = 'vaccination_data_import'

    id = db.Column(db.Integer, primary_key=True)
    datum = db.Column(db.String(255), nullable=False)
    dosen_kumulativ = db.Column(db.Integer, nullable=False)
    dosen_differenz_zum_vortag = db.Column(db.Integer, nullable=False)
    dosen_biontech_kumulativ = db.Column(db.Integer, nullable=False)
    dosen_moderna_kumulativ = db.Column(db.Integer, nullable=False)
    personen_erst_kumulativ = db.Column(db.Integer, nullable=False)
    personen_voll_kumulativ = db.Column(db.Integer, nullable=False)
    impf_quote_erst = db.Column(db.Float, nullable=False)
    impf_quote_voll = db.Column(db.Float, nullable=False)
    indikation_alter_dosen = db.Column(db.Integer, nullable=False)
    indikation_beruf_dosen = db.Column(db.Integer, nullable=False)
    indikation_medizinisch_dosen = db.Column(db.Integer, nullable=False)
    indikation_pflegeheim_dosen = db.Column(db.Integer, nullable=False)
    indikation_alter_erst = db.Column(db.Integer, nullable=False)
    indikation_beruf_erst = db.Column(db.Integer, nullable=False)
    indikation_medizinisch_erst = db.Column(db.Integer, nullable=False)
    indikation_pflegeheim_erst = db.Column(db.Integer, nullable=False)
    indikation_alter_voll = db.Column(db.Integer, nullable=False)
    indikation_beruf_voll = db.Column(db.Integer, nullable=False)
    indikation_medizinisch_voll = db.Column(db.Integer, nullable=False)
    indikation_pflegeheim_voll = db.Column(db.Integer, nullable=False)
    row_imported = db.Column(db.Boolean, nullable=False, default=False)

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
    def get_new_dates_as_array(cls):
        sql_query = """
            select
                date_reported
            from
                vaccination_data_import
            where
                date_reported
            not in (
            select
                distinct
                    vaccination_date_reported.date_reported
                from
                    vaccination_global_data
                left join
                    vaccination_date_reported
                on
                    vaccination_global_data.date_reported_id=vaccination_date_reported.id
            )
            group by
                vaccination_data_import.date_reported
            order by date_reported desc
            """
        new_dates = []
        for item in db.session.execute(sql_query):
            new_dates.append(item['date_reported'])
        return new_dates
