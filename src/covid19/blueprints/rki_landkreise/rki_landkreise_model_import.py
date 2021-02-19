from database import db, ITEMS_PER_PAGE

# OBJECTID,ADE,GF,BSG,RS,AGS,SDV_RS,GEN,BEZ,IBZ,BEM,NBD,SN_L,SN_R,SN_K,SN_V1,SN_V2,SN_G,FK_S3,NUTS,RS_0,AGS_0,WSK,EWZ,KFL,DEBKG_ID,death_rate,cases,deaths,cases_per_100k,cases_per_population,BL,BL_ID,county,last_update,cases7_per_100k,recovered,EWZ_BL,cases7_bl_per_100k,cases7_bl,death7_bl,cases7_lk,death7_lk,cases7_per_100k_txt,AdmUnitId,SHAPE_Length,SHAPE_Area


class RkiLandkreiseImport(db.Model):
    __tablename__ = 'rki_landkreise_import'

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

    @classmethod
    def find_by_id(cls, other_id):
        return db.session.query(cls).filter(cls.id == other_id).one_or_none()

    @classmethod
    def find_by_last_update(cls, last_update_from_import: str):
        return []

    @classmethod
    def get_last_updates(cls):
        return []

    @classmethod
    def get_new_last_update_as_array(cls):
        return []
