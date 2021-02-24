from whoosh.analysis import StemmingAnalyzer

from database import db, ITEMS_PER_PAGE


class RkiBundeslaender(db.Model):
    __tablename__ = 'rki_bundeslaender'
    __searchable__ = ['county']  # indexed fields
    __analyzer__ = StemmingAnalyzer()

    id = db.Column(db.Integer, primary_key=True)
    object_id_1 = db.Column(db.Integer, nullable=False)
    lan_ew_ags = db.Column(db.Integer, nullable=False)
    lan_ew_gen = db.Column(db.String(255), nullable=False)
    lan_ew_bez = db.Column(db.String(255), nullable=False)
    lan_ew_ewz = db.Column(db.Integer, nullable=False)
    object_id = db.Column(db.Integer, nullable=False)
    fallzahl = db.Column(db.Integer, nullable=False)
    aktualisierung = db.Column(db.String(255), nullable=False)
    ags_txt = db.Column(db.Integer, nullable=False)
    global_id = db.Column(db.String(255), nullable=False)
    faelle_100000_ew = db.Column(db.Float, nullable=False)
    death = db.Column(db.Integer, nullable=False)
    cases7_bl_per_100k = db.Column(db.Float, nullable=False)
    cases7_bl = db.Column(db.Integer, nullable=False)
    death7_bl = db.Column(db.Integer, nullable=False)
    cases7_bl_per_100k_txt = db.Column(db.String(255), nullable=False)
    adm_unit_id = db.Column(db.Integer, nullable=False)
    shape_length = db.Column(db.Float, nullable=False)
    shape_area = db.Column(db.Float, nullable=False)

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
    def find_by_id(cls, other_id):
        return db.session.query(cls).filter(cls.id == other_id).one_or_none()
