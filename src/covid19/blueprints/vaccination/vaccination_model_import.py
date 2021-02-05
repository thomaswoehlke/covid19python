from database import db, ITEMS_PER_PAGE


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

    @classmethod
    def remove_all(cls):
        for one in cls.get_all():
            db.session.delete(one)
        db.session.commit()
        return None

    @classmethod
    def get_all_as_page(cls, page):
        return db.session.query(cls)\
            .order_by(cls.datum.desc())\
            .paginate(page, per_page=ITEMS_PER_PAGE)

    @classmethod
    def get_all(cls):
        return db.session.query(cls)\
            .order_by(cls.datum.desc())\
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
            .filter(cls.datum == other_datum) \
            .one_or_none()

