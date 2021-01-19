import os
import psycopg2
from database import db, app
from org.woehlke.covid19.europe.europe_model import EuropeDataImportTable


class EuropeServiceUpdate:
    def __init__(self, database):
        app.logger.info("------------------------------------------------------------")
        app.logger.info(" Europe Service Update [init]")
        app.logger.info("------------------------------------------------------------")
        self.__database = database
        self.limit_nr = 20
        self.__europa_cvsfile_name = "ecdc_europa_data.csv"
        self.__src_europa_cvsfile_name = "data"+os.sep+self.__europa_cvsfile_name
        self.__src_europa_cvsfile_tmp_name = "data"+os.sep+"tmp_"+self.__europa_cvsfile_name
        self.__url_src_data = "https://opendata.ecdc.europa.eu/covid19/casedistribution/csv/"
        app.logger.info("------------------------------------------------------------")
        app.logger.info(" Europe Service Update [ready] ")

    def __update_date_reported(self):
        EuropeDataImportTable.remove_all()
        result = EuropeDataImportTable.get_date_rep()
        for result_item in result.items:
            my_date_rep = result_item['date_rep']
            year_week = result_item['year_week']
            app.logger.info("| "+my_date_rep+" | "+year_week+" |")
        return self

    def update_db(self):
        app.logger.info(" update_db [begin]")
        app.logger.info("------------------------------------------------------------")
        app.logger.info(" ... ")
        app.logger.info(" ... TBD ... ")
        self.__update_date_reported()
        app.logger.info(" ... ")
        app.logger.info(" update_db [done]")
        app.logger.info("------------------------------------------------------------")
        return self

