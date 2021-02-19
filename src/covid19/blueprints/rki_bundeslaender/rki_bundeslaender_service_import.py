import csv
import psycopg2

from database import db, app
from covid19.blueprints.rki_bundeslaender.rki_bundeslaender_model_import import RkiBundeslaenderImport
from covid19.blueprints.rki_bundeslaender.rki_bundeslaender_service_config import RkiBundeslaenderServiceConfig


class RkiBundeslaenderServiceImport:
    def __init__(self, database, config: RkiBundeslaenderServiceConfig):
        app.logger.debug("------------------------------------------------------------")
        app.logger.debug(" RKI Service Import [init]")
        app.logger.debug("------------------------------------------------------------")
        self.__database = database
        self.cfg = config
        app.logger.debug("------------------------------------------------------------")
        app.logger.debug(" RKI Service Import [ready]")

    def import_file(self):
        app.logger.info(" import RKI [begin]")
        app.logger.info("------------------------------------------------------------")
        app.logger.info(" import into TABLE: "+self.cfg.tablename+" from "+self.cfg.cvsfile_path)
        app.logger.info("------------------------------------------------------------")
        row = None
        try:
            RkiBundeslaenderImport.remove_all()
            with open(self.cfg.cvsfile_path, newline='\n') as csv_file:
                file_reader = csv.DictReader(csv_file, delimiter=',', quotechar='"')
                k = 0
                for row in file_reader:
                    k = k + 1
                    o = RkiBundeslaenderImport(
                        OBJECTID_1=row['OBJECTID_1'],
                        LAN_ew_AGS=row['LAN_ew_AGS'],
                        LAN_ew_GEN=row['LAN_ew_GEN'],
                        LAN_ew_BEZ=row['LAN_ew_BEZ'],
                        LAN_ew_EWZ=row['LAN_ew_EWZ'],
                        OBJECTID=row['OBJECTID'],
                        Fallzahl=row['Fallzahl'],
                        Aktualisierung=row['Aktualisierung'],
                        AGS_TXT=row['AGS_TXT'],
                        GlobalID=row['GlobalID'],
                        faelle_100000_EW=row['faelle_100000_EW'],
                        Death=row['Death'],
                        cases7_bl_per_100k=row['cases7_bl_per_100k'],
                        cases7_bl=row['cases7_bl'],
                        death7_bl=row['death7_bl'],
                        cases7_bl_per_100k_txt=row['cases7_bl_per_100k_txt'],
                        AdmUnitId=row['AdmUnitId'],
                        SHAPE_Length=row['SHAPE_Length'],
                        SHAPE_Area=row['SHAPE_Area'],
                    )
                    db.session.add(o)
                    if (k % 2000) == 0:
                        db.session.commit()
                        app.logger.info(" import RKI Bundeslaender  ... " + str(k) + " rows")
                db.session.commit()
                app.logger.info(" import RKI Bundeslaender ... " + str(k) + " rows total")
        except KeyError as error:
            app.logger.warning("WARN: import RKI [begin]")
            app.logger.warning(":::"+str(error)+":::")
            for item_key, item_value in row.items():
                app.logger.warning(item_key+" : "+item_value)
            app.logger.warning("WARN: import RKI Bundeslaender [end]")
        except (Exception, psycopg2.DatabaseError) as error:
            app.logger.warning("WARN: import RKI Bundeslaender [begin]")
            app.logger.warning(error)
            app.logger.warning("WARN: import RKI Bundeslaender [end]")
        finally:
            app.logger.info("")
            app.logger.info("------------------------------------------------------------")
            app.logger.info(" imported into TABLE: "+self.cfg.tablename+" from "+self.cfg.cvsfile_path)
            app.logger.info("------------------------------------------------------------")
            app.logger.info(" import RKI Bundeslaender  [done]")
        return self
