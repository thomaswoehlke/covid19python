import os
import wget
from flask import flash
from database import app


class EuropeServiceDownloadConfig:
    def __init__(self):
        self.limit_nr = 20
        self.data_path = "data"
        self.cvsfile_name = "ecdc_europa_data.csv"
        self.url_src_data = "https://opendata.ecdc.europa.eu/covid19/casedistribution/csv/"


class EuropeServiceDownload:
    def __init__(self, database):
        app.logger.info("------------------------------------------------------------")
        app.logger.info(" Europe Service Download [init]")
        app.logger.info("------------------------------------------------------------")
        self.__database = database
        self.cfg = EuropeServiceDownloadConfig()
        app.logger.info("------------------------------------------------------------")
        app.logger.info(" Europe Service Download [ready] ")

    def download(self):
        src_cvsfile_name = self.cfg.data_path+os.sep+self.cfg.cvsfile_name
        app.logger.info("------------------------------------------------------------")
        app.logger.info(" download Europa [begin]")
        app.logger.info("------------------------------------------------------------")
        app.logger.info(" FILE: "+self.cfg.cvsfile_name+" <- "+self.cfg.url_src_data)
        app.logger.info("------------------------------------------------------------")
        os.makedirs('data', exist_ok=True)
        app.logger.info("------------------------------------------------------------")
        try:
            if os.path.isfile(src_cvsfile_name):
                os.remove(src_cvsfile_name)
            wget.download(self.cfg.url_src_data, src_cvsfile_name)
            app.logger.info("------------------------------------------------------------")
        except RuntimeError as error:
            app.logger.info("############################################################")
            app.logger.info(" " + error + " ")
            app.logger.info("############################################################")
            flash(message="error while downloading: " + src_cvsfile_name, category='error')
        except Exception as error:
            app.logger.info("############################################################")
            app.logger.info(error)
            app.logger.info("############################################################")
            flash(message="error after downloading: " + src_cvsfile_name, category='error')
        except AttributeError as aerror:
            app.logger.info("############################################################")
            app.logger.info(aerror)
            app.logger.info("############################################################")
            flash(message="error after downloading: " + src_cvsfile_name, category='error')
        finally:
            app.logger.info(" download Europa [done]")
            msg = "downloaded: " + src_cvsfile_name + " "
            flash(msg)
        return self
