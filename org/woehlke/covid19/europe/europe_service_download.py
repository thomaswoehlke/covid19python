import os
import wget
from flask import flash
from database import app

europe_service_download = None


class EuropeServiceDownload:
    def __init__(self, database):
        app.logger.info("------------------------------------------------------------")
        app.logger.info(" Europe Service Download [init]")
        app.logger.info("------------------------------------------------------------")
        self.__database = database
        self.limit_nr = 20
        self.__cvsfile_name = "ecdc_europa_data.csv"
        self.__src_cvsfile_name = "data"+os.sep+self.__cvsfile_name
        self.__src_cvsfile_tmp_name = "data"+os.sep+"tmp_"+self.__cvsfile_name
        self.__url_src_data = "https://opendata.ecdc.europa.eu/covid19/casedistribution/csv/"
        app.logger.info("------------------------------------------------------------")
        app.logger.info(" Europe Service Download [ready] ")

    def download(self):
        app.logger.info("------------------------------------------------------------")
        app.logger.info(" download Europa [begin]")
        app.logger.info("------------------------------------------------------------")
        app.logger.info(" FILE: "+self.__cvsfile_name+" <- "+self.__url_src_data)
        app.logger.info("------------------------------------------------------------")
        os.makedirs('data', exist_ok=True)
        app.logger.info("------------------------------------------------------------")
        try:
            if os.path.isfile(self.__src_cvsfile_name):
                os.remove(self.__src_cvsfile_name)
            wget.download(self.__url_src_data, self.__src_cvsfile_name)
            app.logger.info("------------------------------------------------------------")
        except RuntimeError as error:
            app.logger.info("############################################################")
            app.logger.info(" " + error + " ")
            app.logger.info("############################################################")
            flash(message="error while downloading: " + self.__url_src_data, category='error')
        except Exception as error:
            app.logger.info("############################################################")
            app.logger.info(error)
            app.logger.info("############################################################")
            flash(message="error after downloading: " + self.__cvsfile_name, category='error')
        except AttributeError as aerror:
            app.logger.info("############################################################")
            app.logger.info(aerror)
            app.logger.info("############################################################")
            flash(message="error after downloading: " + self.__cvsfile_name, category='error')
        finally:
            app.logger.info(" download Europa [done]")
            msg = "downloaded: " + self.__cvsfile_name + " "
            flash(msg)
        return self
