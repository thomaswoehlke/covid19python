import os
import wget
from database import app

europe_service_download = None


class EuropeServiceDownload:
    def __init__(self, database):
        app.logger.info("------------------------------------------------------------")
        app.logger.info(" Europe Service Download [init]")
        app.logger.info("------------------------------------------------------------")
        self.__database = database
        self.limit_nr = 20
        self.__europa_cvsfile_name = "ecdc_europa_data.csv"
        self.__src_europa_cvsfile_name = "data"+os.sep+self.__europa_cvsfile_name
        self.__src_europa_cvsfile_tmp_name = "data"+os.sep+"tmp_"+self.__europa_cvsfile_name
        self.__url_src_data = "https://opendata.ecdc.europa.eu/covid19/casedistribution/csv/"
        app.logger.info("------------------------------------------------------------")
        app.logger.info(" Europe Service Download [ready] ")

    def download(self):
        app.logger.info("------------------------------------------------------------")
        app.logger.info(" download Europa [begin]")
        app.logger.info("------------------------------------------------------------")
        app.logger.info(" FILE: "+self.__src_europa_cvsfile_name+" <- "+self.__url_src_data)
        app.logger.info("------------------------------------------------------------")
        os.makedirs('data', exist_ok=True)
        app.logger.info("------------------------------------------------------------")
        try:
            wget.download(self.__url_src_data, self.__src_europa_cvsfile_name)
            app.logger.info("------------------------------------------------------------")
        except Exception as error:
            app.logger.warning(error)
            app.logger.warning("------------------------------------------------------------")
        finally:
            app.logger.info(" download Europa [done]")
        return self
