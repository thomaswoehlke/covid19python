from sqlalchemy import and_
from datetime import date
from sqlalchemy.orm import joinedload

from database import db, ITEMS_PER_PAGE
from covid19.blueprints.common.common_model import CommonDateReported, CommonRegion
from covid19.blueprints.common.common_model import RkiDateReported, RkiRegion, RkiCountry


# TODO: #123 split RkiBundeslaenderService into two Services, one for bundeslaender and one for landkreise
# TODO: #124 rename RkiBundeslaender to RkiBundeslaender
class RkiBundeslaender(db.Model):
    __tablename__ = 'rki_bundeslaender'

    id = db.Column(db.Integer, primary_key=True)
    cases_new = db.Column(db.Integer, nullable=False)
    cases_cumulative = db.Column(db.Integer, nullable=False)
    deaths_new = db.Column(db.Integer, nullable=False)
    deaths_cumulative = db.Column(db.Integer, nullable=False)
    date_reported_id = db.Column(db.Integer,
        db.ForeignKey('rki_date_reported.id'), nullable=False)
    date_reported = db.relationship(
        'RkiDateReported',
        lazy='joined',
        cascade='all, delete',
        order_by='desc(RkiDateReported.date_reported)')
    country_id = db.Column(db.Integer,
        db.ForeignKey('rki_country.id'), nullable=False)
    country = db.relationship(
        'RkiCountry', lazy='joined', order_by='asc(RkiCountry.country)')

    @classmethod
    def remove_all(cls):
        for one in cls.get_all():
            db.session.delete(one)
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
