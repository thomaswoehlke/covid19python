from datetime import date

from database import db, ITEMS_PER_PAGE
from covid19.blueprints.common.common_model import CommonDateReported


class VaccinationDateReported(CommonDateReported):
    __mapper_args__ = {'polymorphic_identity': 'vaccination_date_reported'}

    @classmethod
    def create_new_object_factory(cls, my_date_rep):
        my_datum = date.fromisoformat(my_date_rep)
        (my_iso_year, week_number, weekday) = my_datum.isocalendar()
        my_year_week = "" + str(my_iso_year)
        if week_number < 10:
            my_year_week += "-0"
        else:
            my_year_week += "-"
        my_year_week += str(week_number)
        return VaccinationDateReported(
            date_reported=my_date_rep,
            datum=my_datum,
            year=my_datum.year,
            month=my_datum.month,
            day_of_month=my_datum.day,
            day_of_week=weekday,
            week_of_year=week_number,
            year_week=my_year_week
        )


# TODO: #86 rename VaccinationData to VaccinationData
# TODO: #162 rename table vaccination_germany_timeline into vaccination_data
class VaccinationData(db.Model):
    __tablename__ = 'vaccination_data'

    id = db.Column(db.Integer, primary_key=True)
    date_reported_id = db.Column(db.Integer, db.ForeignKey('common_date_reported.id'), nullable=False)
    date_reported = db.relationship(
        'VaccinationDateReported',
        lazy='joined',
        cascade='all, delete',
        order_by='desc(VaccinationDateReported.date_reported)')
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

    @classmethod
    def remove_all(cls):
        for one in cls.get_all():
            db.session.delete(one)
        db.session.commit()
        return None

    @classmethod
    def get_all_as_page(cls, page):
        return db.session.query(cls)\
            .order_by(cls.date_reported)\
            .paginate(page, per_page=ITEMS_PER_PAGE)

    @classmethod
    def get_all(cls):
        return db.session.query(cls)\
            .order_by(cls.date_reported)\
            .all()

    @classmethod
    def get_by_id(cls, other_id):
        return db.session.query(cls)\
            .filter(cls.id == other_id)\
            .one()

    @classmethod
    def find_by_id(cls, other_id):
        return db.session.query(cls) \
            .filter(cls.id == other_id) \
            .one_or_none()

    @classmethod
    def find_by_datum(cls, other_datum):
        return db.session.query(cls) \
            .filter(cls.date_reported == other_datum) \
            .one_or_none()
