from sqlalchemy import and_
from datetime import date
from sqlalchemy.orm import joinedload

from database import db, ITEMS_PER_PAGE


# TODO: #123 split RkiBundeslaenderService into two Services, one for bundeslaender and one for landkreise
# TODO: #125 implement RkiLandkreise
class RkiLandkreise(db.Model):
    __tablename__ = 'rki_landkreise'

    id = db.Column(db.Integer, primary_key=True)

    OBJECTID_1 = db.Column(db.String(255), nullable=False)
    LAN_ew_AGS = db.Column(db.String(255), nullable=False)
    LAN_ew_GEN = db.Column(db.String(255), nullable=False)
    LAN_ew_BEZ = db.Column(db.String(255), nullable=False)
    LAN_ew_EWZ = db.Column(db.String(255), nullable=False)
    OBJECTID = db.Column(db.String(255), nullable=False)
    Fallzahl = db.Column(db.String(255), nullable=False)
    Aktualisierung = db.Column(db.String(255), nullable=False)
    AGS_TXT = db.Column(db.String(255), nullable=False)
    GlobalID = db.Column(db.String(255), nullable=False)
    faelle_100000_EW = db.Column(db.String(255), nullable=False)
    Death = db.Column(db.String(255), nullable=False)
    cases7_bl_per_100k = db.Column(db.String(255), nullable=False)
    cases7_bl = db.Column(db.String(255), nullable=False)
    death7_bl = db.Column(db.String(255), nullable=False)
    cases7_bl_per_100k_txt = db.Column(db.String(255), nullable=False)
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
