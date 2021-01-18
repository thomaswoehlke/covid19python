import os
import csv
import psycopg2
from database import db, app
from org.woehlke.covid19.europe.europe_model import EuropeDataImportTable

europe_service_import = None


class EuropeServiceImport:
    def __init__(self, database):
        app.logger.info("------------------------------------------------------------")
        app.logger.info(" Europe Service Import [init]")
        app.logger.info("------------------------------------------------------------")
        self.__database = database
        self.limit_nr = 20
        self.__europa_cvsfile_name = "ecdc_europa_data.csv"
        self.__src_europa_cvsfile_name = "data"+os.sep+self.__europa_cvsfile_name
        self.__src_europa_cvsfile_tmp_name = "data"+os.sep+"tmp_"+self.__europa_cvsfile_name
        self.__url_src_data = "https://opendata.ecdc.europa.eu/covid19/casedistribution/csv/"
        app.logger.info("------------------------------------------------------------")
        app.logger.info(" Europe Service Import [ready] ")

    def import_datafile_to_db(self):
        app.logger.info(" import Europa [begin]")
        app.logger.info("------------------------------------------------------------")
        app.logger.info(" FILE:  " + self.__src_europa_cvsfile_name)
        app.logger.info(" TABLE: europe_data_import")
        app.logger.info("------------------------------------------------------------")
        try:
            EuropeDataImportTable.remove_all()
            with open(self.__src_europa_cvsfile_name, newline='') as csv_file:
                file_reader = csv.DictReader(csv_file, delimiter=',', quotechar='"')
                k = 0
                for row in file_reader:
                    o = EuropeDataImportTable(
                        date_rep=row['dateRep'],
                        year_week=row['year_week'],
                        cases_weekly=row['cases_weekly'],
                        deaths_weekly=row['deaths_weekly'],
                        countries_and_territories=row['countriesAndTerritories'],
                        geo_id=row['geoId'],
                        country_territory_code=row['countryterritoryCode'],
                        pop_data_2019=row['popData2019'],
                        continent_exp=row['continentExp'],
                        notification_rate_per_100000_population_14days
                        =row['notification_rate_per_100000_population_14-days']
                    )
                    db.session.add(o)
                    if (k % 1000) == 0:
                        db.session.commit()
                        app.logger.info("  import Europa  ...  " + str(k) + " rows")
                    k = k + 1
                db.session.commit()
                app.logger.info("  import Europa  ...  " + str(k) + " rows total")
        except KeyError as error:
            app.logger.warning("KeyError: import Europa [begin]")
            app.logger.warning(":::" + str(error) + ":::")
            for item_key, item_value in row.items():
                app.logger.warning(item_key + " : " + item_value)
            app.logger.warning("KeyError: import Europa [end]")
        except (Exception, psycopg2.DatabaseError) as error:
            app.logger.warning("WARN: import Europa [begin]")
            app.logger.warning(error)
            app.logger.warning("WARN: import Europa [end]")
        finally:
            app.logger.info("------------------------------------------------------------")
            app.logger.info(" import Europa [done]")
        return self
