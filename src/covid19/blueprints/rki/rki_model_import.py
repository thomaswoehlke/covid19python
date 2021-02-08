from database import db, ITEMS_PER_PAGE

# OBJECTID_1,LAN_ew_AGS,LAN_ew_GEN,LAN_ew_BEZ,LAN_ew_EWZ,OBJECTID,Fallzahl,Aktualisierung,AGS_TXT,GlobalID,faelle_100000_EW,Death,cases7_bl_per_100k,cases7_bl,death7_bl,cases7_bl_per_100k_txt,AdmUnitId,SHAPE_Length,SHAPE_Area


# TODO: #123 split RkiBundeslaenderService into two Services, one for bundeslaender and one for landkreise
# TODO: #126 implement RkiBundeslaenderImport
class RkiBundeslaenderImport(db.Model):
    __tablename__ = 'rki_bundeslsaender_import'

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

    @classmethod
    def get_dates_reported(self):
        # TODO: #127 implement RkiBundeslaenderImport.get_dates_reported
        return self


# TODO: #123 split RkiBundeslaenderService into two Services, one for bundeslaender and one for landkreise
# TODO: #128 add fields from csv to RkiLandkreiseImport
class RkiLandkreiseImport(db.Model):
    __tablename__ = 'rki_landkreise_import'

    id = db.Column(db.Integer, primary_key=True)
    date_reported = db.Column(db.String(255), nullable=False)
    country_code = db.Column(db.String(255), nullable=False)
    country = db.Column(db.String(255), nullable=False)
    who_region = db.Column(db.String(255), nullable=False)
    new_cases = db.Column(db.String(255), nullable=False)
    cumulative_cases = db.Column(db.String(255), nullable=False)
    new_deaths = db.Column(db.String(255), nullable=False)
    cumulative_deaths = db.Column(db.String(255), nullable=False)

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
    def get_regions(cls):
        return db.session.query(cls.who_region).distinct()

    @classmethod
    def get_dates_reported(cls):
        return db.session.query(cls.date_reported).distinct()

    @classmethod
    def get_for_one_day(cls, day):
        return db.session.query(cls).filter(cls.date_reported == day).all()

    @classmethod
    def get_new_dates_as_array(cls):
        # TODO: #129 change to ORM ClassHierarchy in: RkiLandkreiseImport.get_new_dates_as_array
        sql_query = """
            select
                date_reported
            from
                rki_landkreise_import
            where
                date_reported
            not in (
            select
                distinct
                    common_date_reported.date_reported
                from
                    rki_landkreise
                left join
                    rki_date_reported
                on
                    rki_landkreise.date_reported_id=common_date_reported.id 
                and 
                    common_date_reported.type='rki_date_reported'    
            )
            group by
                rki_landkreise_import.date_reported
            order by date_reported desc
            """
        new_dates = []
        for item in db.session.execute(sql_query):
            new_dates.append(item['date_reported'])
        return new_dates
