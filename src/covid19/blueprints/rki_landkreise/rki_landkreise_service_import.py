import sys
import csv
import psycopg2

from database import db, app

from covid19.blueprints.application.application_service_config import ApplicationServiceConfig
from covid19.blueprints.rki_landkreise.rki_landkreise_model_import import RkiLandkreiseImport


class RkiLandkreiseServiceImport:
    def __init__(self, database, config: ApplicationServiceConfig):
        app.logger.debug("------------------------------------------------------------")
        app.logger.debug(" RKI Landkreise Service Import [init]")
        app.logger.debug("------------------------------------------------------------")
        self.__database = database
        self.cfg = config
        app.logger.debug("------------------------------------------------------------")
        app.logger.debug(" RKI Landkreise Service Import [ready]")

    # TODO: BUG: RkiLandkreiseServiceImport.import_file #178
    def import_file(self):
        app.logger.info(" RKI Landkreise Service Import - import_file [begin]")
        app.logger.info("------------------------------------------------------------")
        app.logger.info(" import into TABLE: "+self.cfg.tablename+" from "+self.cfg.cvsfile_path)
        app.logger.info("------------------------------------------------------------")
        row = None
        try:
            RkiLandkreiseImport.remove_all()
            with open(self.cfg.cvsfile_path, newline='\n') as csv_file:
                file_reader = csv.DictReader(csv_file, delimiter=',', quotechar='"')
                k = 0
                for row in file_reader:
                    k += 1
                    o = RkiLandkreiseImport(
                        OBJECTID=row['OBJECTID'],
                        ADE=row['ADE'],
                        GF=row['GF'],
                        BSG=row['BSG'],
                        RS=row['RS'],
                        AGS=row['AGS'],
                        SDV_RS=row['SDV_RS'],
                        GEN=row['GEN'],
                        BEZ=row['BEZ'],
                        IBZ=row['IBZ'],
                        BEM=row['BEM'],
                        NBD=row['NBD'],
                        SN_L=row['SN_L'],
                        SN_R=row['SN_R'],
                        SN_K=row['SN_K'],
                        SN_V1=row['SN_V1'],
                        SN_V2=row['SN_V2'],
                        SN_G=row['SN_G'],
                        FK_S3=row['FK_S3'],
                        NUTS=row['NUTS'],
                        RS_0=row['RS_0'],
                        AGS_0=row['AGS_0'],
                        WSK=row['WSK'],
                        EWZ=row['EWZ'],
                        KFL=row['KFL'],
                        DEBKG_ID=row['DEBKG_ID'],
                        death_rate=row['death_rate'],
                        cases=row['cases'],
                        deaths=row['deaths'],
                        cases_per_100k=row['cases_per_100k'],
                        cases_per_population=row['cases_per_population'],
                        BL=row['BL'],
                        BL_ID=row['BL_ID'],
                        county=row['county'],
                        last_update=row['last_update'],
                        cases7_per_100k=row['cases7_per_100k'],
                        recovered=row['recovered'],
                        EWZ_BL=row['EWZ_BL'],
                        cases7_bl_per_100k=row['cases7_bl_per_100k'],
                        cases7_bl=row['cases7_bl'],
                        death7_bl=row['death7_bl'],
                        cases7_lk=row['cases7_lk'],
                        death7_lk=row['death7_lk'],
                        cases7_per_100k_txt=row['cases7_per_100k_txt'],
                        AdmUnitId=row['AdmUnitId'],
                        SHAPE_Length=row['SHAPE_Length'],
                        SHAPE_Area=row['SHAPE_Area'],
                    )
                    db.session.add(o)
                    if (k % 2000) == 0:
                        db.session.commit()
                        app.logger.info(" import import_file  ... " + str(k) + " rows")
                db.session.commit()
                app.logger.info(" import import_file  ... " + str(k) + " rows total")
        except KeyError as error:
            app.logger.warning("WARN: RKI Landkreise Service Import - import_file [begin]")
            app.logger.warning(":::"+str(error)+":::")
            for item_key, item_value in row.items():
                app.logger.warning(item_key+" : "+item_value)
            app.logger.warning("WARN: RKI Landkreise Service Import - import_file [end]")
        except (Exception, psycopg2.DatabaseError) as error:
            app.logger.warning("WARN: RKI Landkreise Service Import - import_file [begin]")
            app.logger.warning(error)
            app.logger.warning("WARN: RKI Landkreise Service Import - import_file [end]")
        finally:
            app.logger.info("")
            app.logger.info("------------------------------------------------------------")
            app.logger.info(" imported into TABLE: "+self.cfg.tablename+" from "+self.cfg.cvsfile_path)
            app.logger.info("------------------------------------------------------------")
            app.logger.info(" RKI Landkreise Service Import - import_file [done]")
        return self
