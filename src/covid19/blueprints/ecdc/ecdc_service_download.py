import os
import wget
from flask import flash
from database import app
from covid19.blueprints.ecdc.ecdc_service_config import EcdcServiceConfig


class EcdcServiceDownload:
    def __init__(self, database):
        app.logger.debug("------------------------------------------------------------")
        app.logger.debug(" ECDC Service Download [init]")
        app.logger.debug("------------------------------------------------------------")
        self.__database = database
        self.cfg = EcdcServiceConfig()
        app.logger.debug("------------------------------------------------------------")
        app.logger.debug(" ECDC Service Download [ready] ")

    def download(self):
        src_cvsfile_name = self.cfg.data_path+os.sep+self.cfg.cvsfile_name
        app.logger.info("------------------------------------------------------------")
        app.logger.info(" download ECDC [begin]")
        app.logger.info("------------------------------------------------------------")
        app.logger.info(" FILE: "+self.cfg.cvsfile_name+" <- "+self.cfg.url_src_data)
        app.logger.info("------------------------------------------------------------")
        try:
            os.makedirs(self.cfg.data_path, exist_ok=True)
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
            app.logger.info(" download ECDC [done]")
            msg = "downloaded: " + src_cvsfile_name + " "
            flash(msg)
        return self
