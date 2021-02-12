from sqlalchemy import and_
from datetime import date
from sqlalchemy.orm import joinedload

from database import db, ITEMS_PER_PAGE


# TODO: #123 split RkiBundeslaenderService into two Services, one for bundeslaender and one for landkreise
# TODO: #125 implement RkiLandkreise
class RkiLandkreise(db.Model):
    __tablename__ = 'rki_landkreise'

    id = db.Column(db.Integer, primary_key=True)

    OBJECTID = db.Column(db.String(255), nullable=False)
    ADE = db.Column(db.String(255), nullable=False)
    GF = db.Column(db.String(255), nullable=False)
    BSG = db.Column(db.String(255), nullable=False)
    RS = db.Column(db.String(255), nullable=False)
    AGS = db.Column(db.String(255), nullable=False)
    SDV_RS = db.Column(db.String(255), nullable=False)
    GEN = db.Column(db.String(255), nullable=False)
    BEZ = db.Column(db.String(255), nullable=False)
    IBZ = db.Column(db.String(255), nullable=False)
    BEM = db.Column(db.String(255), nullable=False)
    NBD = db.Column(db.String(255), nullable=False)
    SN_L = db.Column(db.String(255), nullable=False)
    SN_R = db.Column(db.String(255), nullable=False)
    SN_K = db.Column(db.String(255), nullable=False)
    SN_V1 = db.Column(db.String(255), nullable=False)
    SN_V2 = db.Column(db.String(255), nullable=False)
    SN_G = db.Column(db.String(255), nullable=False)
    FK_S3 = db.Column(db.String(255), nullable=False)
    NUTS = db.Column(db.String(255), nullable=False)
    RS_0 = db.Column(db.String(255), nullable=False)
    AGS_0 = db.Column(db.String(255), nullable=False)
    WSK = db.Column(db.String(255), nullable=False)
    EWZ = db.Column(db.String(255), nullable=False)
    KFL = db.Column(db.String(255), nullable=False)
    DEBKG_ID = db.Column(db.String(255), nullable=False)
    death_rate = db.Column(db.String(255), nullable=False)
    cases = db.Column(db.String(255), nullable=False)
    deaths = db.Column(db.String(255), nullable=False)
    cases_per_100k = db.Column(db.String(255), nullable=False)
    cases_per_population = db.Column(db.String(255), nullable=False)
    BL = db.Column(db.String(255), nullable=False)
    BL_ID = db.Column(db.String(255), nullable=False)
    county = db.Column(db.String(255), nullable=False)
    last_update = db.Column(db.String(255), nullable=False)
    cases7_per_100k = db.Column(db.String(255), nullable=False)
    recovered = db.Column(db.String(255), nullable=False)
    EWZ_BL = db.Column(db.String(255), nullable=False)
    cases7_bl_per_100k = db.Column(db.String(255), nullable=False)
    cases7_bl = db.Column(db.String(255), nullable=False)
    death7_bl = db.Column(db.String(255), nullable=False)
    cases7_lk = db.Column(db.String(255), nullable=False)
    death7_lk = db.Column(db.String(255), nullable=False)
    cases7_per_100k_txt = db.Column(db.String(255), nullable=False)
    AdmUnitId = db.Column(db.String(255), nullable=False)
    SHAPE_Length = db.Column(db.String(255), nullable=False)
    SHAPE_Area = db.Column(db.String(255), nullable=False)

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
