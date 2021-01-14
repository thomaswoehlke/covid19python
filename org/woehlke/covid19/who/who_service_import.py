import os
import sys
import csv
import psycopg2
from database import db, app
from org.woehlke.covid19.who.who_model import WhoGlobalDataImportTable


who_service_import = None


class WhoServiceImport:
    def __init__(self, database):
        app.logger.info("------------------------------------------------------------")
        app.logger.info(" WHO Service Import [init]")
        app.logger.info("------------------------------------------------------------")
        self.__database = database
        self.limit_nr = 20
        self.__who_cvsfile_name = "WHO-COVID-19-global-data.csv"
        self.__src_who_cvsfile_name = "data"+os.sep+self.__who_cvsfile_name
        self.__src_who_cvsfile_tmp_name = "data"+os.sep+"tmp_"+self.__who_cvsfile_name
        self.__url_src_data = "https://covid19.who.int/"+self.__who_cvsfile_name
        app.logger.info("------------------------------------------------------------")
        app.logger.info(" WHO Service Import [ready]")

    def import_file(self):
        app.logger.info(" import WHO [begin]")
        app.logger.info("------------------------------------------------------------")
        app.logger.info(" FILE:  "+self.__src_who_cvsfile_name)
        app.logger.info(" TABLE: who_global_data_import")
        app.logger.info("------------------------------------------------------------")
        row = None
        if sys.platform == 'linux':
            keyDate_reported ='\ufeffDate_reported'
        else:
            keyDate_reported = 'ï»¿Date_reported'
        try:
            WhoGlobalDataImportTable.remove_all()
            with open(self.__src_who_cvsfile_name, newline='\n') as csv_file:
                file_reader = csv.DictReader(csv_file, delimiter=',', quotechar='"')
                k = 0
                for row in file_reader:
                    o = WhoGlobalDataImportTable(
                        date_reported=row[keyDate_reported],
                        country_code=row['Country_code'],
                        country=row['Country'],
                        who_region=row['WHO_region'],
                        new_cases=row['New_cases'],
                        cumulative_cases=row['Cumulative_cases'],
                        new_deaths=row['New_deaths'],
                        cumulative_deaths=row['Cumulative_deaths'],
                        row_imported=False
                    )
                    db.session.add(o)
                    if (k % 2000) == 0:
                        db.session.commit()
                        app.logger.info(" import WHO  ... " + str(k) + " rows")
                    k = k + 1
                db.session.commit()
        except KeyError as error:
            app.logger.warning("WARN: import WHO [begin]")
            app.logger.warning(":::"+str(error)+":::")
            for item_key, item_value in row.items():
                app.logger.warning(item_key+" : "+item_value)
            app.logger.warning("WARN: import WHO [end]")
        except (Exception, psycopg2.DatabaseError) as error:
            app.logger.warning("WARN: import WHO [begin]")
            app.logger.warning(error)
            app.logger.warning("WARN: import WHO [end]")
        finally:
            app.logger.info("")
            app.logger.info("------------------------------------------------------------")
            app.logger.info(" import WHO [done]")
        return self
