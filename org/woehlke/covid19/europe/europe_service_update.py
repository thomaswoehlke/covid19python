import os
import psycopg2
from database import db, app
from org.woehlke.covid19.europe.europe_model import EuropeDataImportTable, EuropeDateReported


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
        app.logger.info(" __update_date_reported [begin]")
        app.logger.info("------------------------------------------------------------")
        EuropeDateReported.remove_all()
        result_date_rep = EuropeDataImportTable.get_date_rep()
        for result_item in result_date_rep:
            my_date_rep = result_item['date_rep']
            my_year_week = result_item['year_week']
            app.logger.info("| "+my_date_rep+" | "+my_year_week+" |")
            o = EuropeDateReported(
                date_rep=my_date_rep,
                year_week=my_year_week
            )
            db.session.add(o)
        db.session.commit()
        app.logger.info(" __update_date_reported [done]")
        app.logger.info("------------------------------------------------------------")
        return self

    def __update_continent(self):
        app.logger.info(" __update_continent [begin]")
        app.logger.info("------------------------------------------------------------")
        app.logger.info(" ... ")
        app.logger.info(" __update_continent [done]")
        app.logger.info("------------------------------------------------------------")
        return self

    def __update_country(self):
        app.logger.info(" __update_country [begin]")
        app.logger.info("------------------------------------------------------------")
        app.logger.info(" ... ")
        app.logger.info(" __update_country [done]")
        app.logger.info("------------------------------------------------------------")
        return self

    def __update_data(self):
        app.logger.info(" __update_data [begin]")
        app.logger.info("------------------------------------------------------------")
        app.logger.info(" ... ")
        app.logger.info(" __update_data [done]")
        app.logger.info("------------------------------------------------------------")
        return self

    def update_db(self):
        app.logger.info(" update_db [begin]")
        app.logger.info("------------------------------------------------------------")
        self.__update_date_reported()
        self.__update_continent()
        app.logger.info(" update_db [done]")
        app.logger.info("------------------------------------------------------------")
        return self

