from flask_sqlalchemy import Pagination
from sqlalchemy import and_, func
from database import db, ITEMS_PER_PAGE
from sqlalchemy.orm import joinedload, raiseload


class VaccinationGermanyTimeline(db.Model):
    __tablename__ = 'vaccination_germany_timeline'

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
