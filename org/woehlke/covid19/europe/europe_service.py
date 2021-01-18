import os
import csv
import psycopg2
import wget
from database import db, app
from org.woehlke.covid19.europe.europe_model import EuropeDataImportTable

europe_service = None


class EuropeService:
    def __init__(self, database):
        app.logger.info("------------------------------------------------------------")
        app.logger.info(" Europe Service [init]")
        app.logger.info("------------------------------------------------------------")
        self.__database = database
        self.limit_nr = 20
        self.__europa_cvsfile_name = "ecdc_europa_data.csv"
        self.__src_europa_cvsfile_name = "data"+os.sep+self.__europa_cvsfile_name
        self.__src_europa_cvsfile_tmp_name = "data"+os.sep+"tmp_"+self.__europa_cvsfile_name
        self.__url_src_data = "https://opendata.ecdc.europa.eu/covid19/casedistribution/csv/"
        app.logger.info("------------------------------------------------------------")
        app.logger.info(" Europe Service [ready] ")

    def __download(self):
        app.logger.info("------------------------------------------------------------")
        app.logger.info(" download Europa [begin]")
        app.logger.info("------------------------------------------------------------")
        app.logger.info(" FILE: "+self.__src_europa_cvsfile_name+" <- "+self.__url_src_data)
        app.logger.info("------------------------------------------------------------")
        os.makedirs('data', exist_ok=True)
        app.logger.info("------------------------------------------------------------")
        try:
            data_file = wget.download(self.__url_src_data,self.__src_europa_cvsfile_name)
            #os.remove(self.__src_europa_cvsfile_name)
            #os.renames(data_file, self.__src_europa_cvsfile_name)
            app.logger.info("------------------------------------------------------------")
        except Exception as error:
            app.logger.warning(error)
            app.logger.warning("------------------------------------------------------------")
        finally:
            app.logger.info(" download Europa [done]")
        return self

    def __import(self):
        app.logger.info(" import Europa [begin]")
        app.logger.info("------------------------------------------------------------")
        app.logger.info(" FILE:  "+self.__src_europa_cvsfile_name)
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
                    if (k % 1000) == 0:
                        db.session.commit()
                        app.logger.info("  import Europa  ...  " + str(k) + " rows")
                    k = k + 1
                db.session.commit()
        except KeyError as error:
            app.logger.warning("KeyError: import Europa [begin]")
            app.logger.warning(":::"+str(error)+":::")
            for item_key, item_value in row.items():
                app.logger.warning(item_key+" : "+item_value)
            app.logger.warning("KeyError: import Europa [end]")
        except (Exception, psycopg2.DatabaseError) as error:
            app.logger.warning("WARN: import Europa [begin]")
            app.logger.warning(error)
            app.logger.warning("WARN: import Europa [end]")
        finally:
            app.logger.info("------------------------------------------------------------")
            app.logger.info(" import Europa [done]")
        return self

    def __update_db(self):
        return self

    def download(self):
        app.logger.info(" download [begin]")
        app.logger.info("------------------------------------------------------------")
        self.__download()
        app.logger.info(" download [done]")
        app.logger.info("------------------------------------------------------------")
        return self

    def run_update(self):
        app.logger.info(" run [begin]")
        app.logger.info("------------------------------------------------------------")
        self.__import()
        self.__update_db()
        app.logger.info(" run [done]")
        app.logger.info("------------------------------------------------------------")
        return self
