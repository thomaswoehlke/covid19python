import sys
import csv
import psycopg2

from database import db, app

from covid19.blueprints.rki_landkreise.rki_model_import import RkiLandkreiseImport
from covid19.blueprints.rki_landkreise.rki_service_config import RkiLandkreiseServiceConfig


class RkiLandkreiseServiceImport:
    def __init__(self, database):
        app.logger.debug("------------------------------------------------------------")
        app.logger.debug(" RKI Landkreise Service Import [init]")
        app.logger.debug("------------------------------------------------------------")
        self.__database = database
        self.cfg = RkiLandkreiseServiceConfig()
        app.logger.debug("------------------------------------------------------------")
        app.logger.debug(" RKI Landkreise Service Import [ready]")

    def import_file(self):
        app.logger.info(" RKI Landkreise Service Import - import_file [begin]")
        app.logger.info("------------------------------------------------------------")
        app.logger.info(" FILE:  "+self.cfg.cvsfile_name)
        app.logger.info(" TABLE: who_global_data_import")
        app.logger.info("------------------------------------------------------------")
        row = None
        if sys.platform == 'linux':
            keyDate_reported ='\ufeffDate_reported'
        else:
            keyDate_reported = 'ï»¿Date_reported'
        try:
            RkiLandkreiseImport.remove_all()
            with open(self.cfg.cvsfile_name, newline='\n') as csv_file:
                file_reader = csv.DictReader(csv_file, delimiter=',', quotechar='"')
                k = 0
                for row in file_reader:
                    # TODO: #140 move WhoImport to RKI in: rk_service_import.py
                    o = RkiLandkreiseImport(
                        date_reported=row[keyDate_reported],
                        country_code=row['Country_code'],
                        country=row['Country'],
                        who_region=row['WHO_region'],
                        new_cases=row['New_cases'],
                        cumulative_cases=row['Cumulative_cases'],
                        new_deaths=row['New_deaths'],
                        cumulative_deaths=row['Cumulative_deaths']
                    )
                    db.session.add(o)
                    if (k % 2000) == 0:
                        db.session.commit()
                        app.logger.info(" import import_file  ... " + str(k) + " rows")
                    k = k + 1
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
            app.logger.info(" RKI Landkreise Service Import - import_file [done]")
        return self
