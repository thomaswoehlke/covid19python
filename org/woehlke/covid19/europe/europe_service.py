import os
import csv
import psycopg2
import wget
from database import db, app
from org.woehlke.covid19.europe.europe_model import EuropeDataImportTable
from org.woehlke.covid19.europe.europe_service_download import EuropeServiceDownload
from org.woehlke.covid19.europe.europe_service_import import EuropeServiceImport
from org.woehlke.covid19.europe.europe_service_update import EuropeServiceUpdate

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
        self.europe_service_download = EuropeServiceDownload(database)
        self.europe_service_import = EuropeServiceImport(database)
        self.europe_service_update = EuropeServiceUpdate(database)
        app.logger.info("------------------------------------------------------------")
        app.logger.info(" Europe Service [ready] ")

    def download(self):
        app.logger.info(" download [begin]")
        app.logger.info("------------------------------------------------------------")
        self.europe_service_download.download()
        app.logger.info(" download [done]")
        app.logger.info("------------------------------------------------------------")
        return self

    def run_update(self):
        app.logger.info(" run update [begin]")
        app.logger.info("------------------------------------------------------------")
        self.europe_service_import.import_datafile_to_db()
        self.europe_service_update.update_db()
        app.logger.info(" run update [done]")
        app.logger.info("------------------------------------------------------------")
        return self
