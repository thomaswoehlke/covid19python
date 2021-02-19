from sqlalchemy import and_
from datetime import date
from sqlalchemy.orm import joinedload

from database import db, ITEMS_PER_PAGE


class RkiLandkreise(db.Model):
    __tablename__ = 'rki_landkreise'

    id = db.Column(db.Integer, primary_key=True)
    objectid = db.Column(db.String(255), nullable=False)
    ade = db.Column(db.String(255), nullable=False)
    gf = db.Column(db.String(255), nullable=False)
    bsg = db.Column(db.String(255), nullable=False)
    rs = db.Column(db.String(255), nullable=False)
    ags = db.Column(db.String(255), nullable=False)
    sdv_rs = db.Column(db.String(255), nullable=False)
    gen = db.Column(db.String(255), nullable=False)
    bez = db.Column(db.String(255), nullable=False)
    ibz = db.Column(db.String(255), nullable=False)
    bem = db.Column(db.String(255), nullable=False)
    nbd = db.Column(db.String(255), nullable=False)
    sn_l = db.Column(db.String(255), nullable=False)
    sn_r = db.Column(db.String(255), nullable=False)
    sn_k = db.Column(db.String(255), nullable=False)
    sn_v1 = db.Column(db.String(255), nullable=False)
    sn_v2 = db.Column(db.String(255), nullable=False)
    sn_g = db.Column(db.String(255), nullable=False)
    fk_s3 = db.Column(db.String(255), nullable=False)
    nuts = db.Column(db.String(255), nullable=False)
    rs_0 = db.Column(db.String(255), nullable=False)
    ags_0 = db.Column(db.String(255), nullable=False)
    wsk = db.Column(db.String(255), nullable=False)
    ewz = db.Column(db.String(255), nullable=False)
    kfl = db.Column(db.String(255), nullable=False)
    debkg_id = db.Column(db.String(255), nullable=False)
    death_rate = db.Column(db.String(255), nullable=False)
    cases = db.Column(db.String(255), nullable=False)
    deaths = db.Column(db.String(255), nullable=False)
    cases_per_100k = db.Column(db.String(255), nullable=False)
    cases_per_population = db.Column(db.String(255), nullable=False)
    bl = db.Column(db.String(255), nullable=False)
    bl_id = db.Column(db.String(255), nullable=False)
    county = db.Column(db.String(255), nullable=False)
    last_update = db.Column(db.String(255), nullable=False)
    cases7_per_100k = db.Column(db.String(255), nullable=False)
    recovered = db.Column(db.String(255), nullable=False)
    ewz_bl = db.Column(db.String(255), nullable=False)
    cases7_bl_per_100k = db.Column(db.String(255), nullable=False)
    cases7_bl = db.Column(db.String(255), nullable=False)
    death7_bl = db.Column(db.String(255), nullable=False)
    cases7_lk = db.Column(db.String(255), nullable=False)
    death7_lk = db.Column(db.String(255), nullable=False)
    cases7_per_100k_txt = db.Column(db.String(255), nullable=False)
    adm_unit_id = db.Column(db.String(255), nullable=False)
    shape_length = db.Column(db.String(255), nullable=False)
    shape_area = db.Column(db.String(255), nullable=False)

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
