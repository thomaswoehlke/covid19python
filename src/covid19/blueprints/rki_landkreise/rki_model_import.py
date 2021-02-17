from database import db, ITEMS_PER_PAGE

# OBJECTID,ADE,GF,BSG,RS,AGS,SDV_RS,GEN,BEZ,IBZ,BEM,NBD,SN_L,SN_R,SN_K,SN_V1,SN_V2,SN_G,FK_S3,NUTS,RS_0,AGS_0,WSK,EWZ,KFL,DEBKG_ID,death_rate,cases,deaths,cases_per_100k,cases_per_population,BL,BL_ID,county,last_update,cases7_per_100k,recovered,EWZ_BL,cases7_bl_per_100k,cases7_bl,death7_bl,cases7_lk,death7_lk,cases7_per_100k_txt,AdmUnitId,SHAPE_Length,SHAPE_Area


# TODO: #128 add fields from csv to RkiLandkreiseImport
class RkiLandkreiseImport(db.Model):
    __tablename__ = 'rki_landkreise_import'

    id = db.Column(db.Integer, primary_key=True)

    objectid = db.Column(db.String(255), nullable=False)
    ade = db.Column(db.String(255), nullable=False)
    gf = db.Column(db.String(255), nullable=False)
    bsg = db.Column(db.String(255), nullable=False)
    rs = db.Column(db.String(255), nullable=False)
    ags = db.Column(db.String(255), nullable=False)
    sdv_rs = db.Column(db.String(255), nullable=False)
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
    def get_new_dates_as_array(cls):
        # TODO: #129 change to ORM ClassHierarchy in: RkiLandkreiseImport.get_new_dates_as_array
        sql_query = """
            select
                distinct
                    rki_landkreise_import.date_reported
                from
                    rki_landkreise_import
                where
                    date_reported
                not in (
                    select
                        distinct
                            rki_date_reported.date_reported
                        from
                            rki_landkreise
                        left join
                            rki_date_reported
                        on
                            rki_landkreise.date_reported_id=rki_date_reported.id
                        group by 
                            rki_date_reported.datum
                        order by
                            rki_date_reported.datum desc 
                    )
                group by
                    rki_landkreise_import.date_reported
                order by 
                    rki_landkreise_import.date_reported desc
            """
        new_dates = []
        for item in db.session.execute(sql_query):
            new_dates.append(item['date_reported'])
        return new_dates
