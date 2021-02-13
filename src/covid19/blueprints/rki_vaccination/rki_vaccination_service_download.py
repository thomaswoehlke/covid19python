import os
import wget
from flask import flash
from database import app
from covid19.blueprints.rki_vaccination.vaccination_service_config import VaccinationServiceConfig


class VaccinationServiceDownload:
    def __init__(self, database):
        app.logger.debug("------------------------------------------------------------")
        app.logger.debug(" Vaccination Service Download [init]")
        app.logger.debug("------------------------------------------------------------")
        self.__database = database
        self.cfg = VaccinationServiceConfig()
        app.logger.debug("------------------------------------------------------------")
        app.logger.debug(" Vaccination Service Download [ready]")

    def download_file(self):
        app.logger.info(" download - Vaccination [begin] ")
        app.logger.info("------------------------------------------------------------")
        app.logger.info(" FILE: "+self.cfg.cvsfile_name+" <- "+self.cfg.url_src_data)
        app.logger.info("------------------------------------------------------------")
        try:
            os.makedirs(self.cfg.data_path, exist_ok=True)
            if os.path.isfile(self.cfg.cvsfile_path):
                os.remove(self.cfg.cvsfile_path)
            data_file = wget.download(self.cfg.url_src_data, self.cfg.cvsfile_path)
            app.logger.info(" " + data_file + " ")
        except RuntimeError as error:
            app.logger.error("############################################################")
            app.logger.error(" " + error + " ")
            app.logger.error("############################################################")
            flash(message="error while downloading: " + self.cfg.cvsfile_path, category='error')
        except AttributeError as attribute_error:
            app.logger.error("############################################################")
            app.logger.error(attribute_error)
            app.logger.error("############################################################")
            flash(message="error after downloading: " + self.cfg.cvsfile_path, category='error')
        except Exception as error:
            app.logger.error("############################################################")
            app.logger.error(error)
            app.logger.error("############################################################")
            flash(message="error after downloading: " + self.cfg.cvsfile_path, category='error')
        finally:
            app.logger.info("------------------------------------------------------------")
            app.logger.info(" download - Vaccination [done] ")
            msg = "downloaded: " + self.cfg.cvsfile_path + " "
            flash(msg)
        return self
