import csv
import psycopg2

from database import db, app
from covid19.blueprints.ecdc.ecdc_model_import import EcdcImport
from covid19.blueprints.ecdc.ecdc_service_config import EcdcServiceConfig


class EcdcServiceImport:
    def __init__(self, database):
        app.logger.debug("------------------------------------------------------------")
        app.logger.debug(" ECDC Service Import [init]")
        app.logger.debug("------------------------------------------------------------")
        self.__database = database
        self.cfg = EcdcServiceConfig()
        app.logger.debug("------------------------------------------------------------")
        app.logger.debug(" ECDC Service Import [ready] ")

    def import_file(self):
        app.logger.info(" import ECDC [begin]")
        app.logger.info("------------------------------------------------------------")
        app.logger.info(" import into TABLE: "+self.cfg.tablename+" from "+self.cfg.cvsfile_path)
        app.logger.info("------------------------------------------------------------")
        k = 0
        try:
            EcdcImport.remove_all()
            with open(self.cfg.cvsfile_path, newline='') as csv_file:
                file_reader = csv.DictReader(csv_file, delimiter=',', quotechar='"')
                for row in file_reader:
                    o = EcdcImport(
                        date_rep=row['dateRep'],
                        day=row['day'],
                        month=row['month'],
                        year=row['year'],
                        cases=row['cases'],
                        deaths=row['deaths'],
                        countries_and_territories=row['countriesAndTerritories'],
                        geo_id=row['geoId'],
                        country_territory_code=row['countryterritoryCode'],
                        pop_data_2019=row['popData2019'],
                        continent_exp=row['continentExp'],
                        cumulative_number_for_14_days_of_covid19_cases_per_100000
                        =row['Cumulative_number_for_14_days_of_COVID-19_cases_per_100000']
                    )
                    db.session.add(o)
                    k = k + 1
                    if (k % 100) == 0:
                        db.session.commit()
                        app.logger.info("  import ECDC  ...  " + str(k) + " rows")
            db.session.commit()
            app.logger.info("  import ECDC  ...  " + str(k) + " rows total")
        except KeyError as error:
            app.logger.warning("KeyError: import ECDC [begin]")
            app.logger.warning(":::" + str(error) + ":::")
            for item_key, item_value in row.items():
                app.logger.warning(item_key + " : " + item_value)
            app.logger.warning("KeyError: import ECDC [end]")
        except (Exception, psycopg2.DatabaseError) as error:
            app.logger.warning("WARN: import ECDC [begin]")
            app.logger.warning(error)
            app.logger.warning("WARN: import ECDC [end]")
        finally:
            app.logger.info("------------------------------------------------------------")
            app.logger.info(" import ECDC [done]")
        return self
