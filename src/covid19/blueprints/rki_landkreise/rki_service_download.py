import os
import wget
from flask import flash

from database import app
from covid19.blueprints.rki_landkreise.rki_service_config import RkiLandkreiseServiceConfig


class RkiLandkreiseServiceDownload:
    def __init__(self, database):
        app.logger.debug("------------------------------------------------------------")
        app.logger.debug(" RKI Landkreise Service Download [init]")
        app.logger.debug("------------------------------------------------------------")
        self.__database = database
        self.cfg = RkiLandkreiseServiceConfig()
        app.logger.debug("------------------------------------------------------------")
        app.logger.debug(" RKI Landkreise Service Download [ready]")

    def download_file(self):
        app.logger.info(" RKI Landkreise Service Download - download_file begin] ")
        app.logger.info("------------------------------------------------------------")
        app.logger.info(" FILE: "+self.cfg.cvsfile_name+" <- "+self.cfg.url_src)
        app.logger.info("------------------------------------------------------------")
        try:
            os.makedirs(self.cfg.data_path, exist_ok=True)
            if os.path.isfile(self.cfg.src_cvsfile_path):
                os.remove(self.cfg.src_cvsfile_path)
            data_file = wget.download(self.cfg.url_src, self.cfg.src_cvsfile_path)
            app.logger.info(" " + data_file + " ")
        except RuntimeError as error:
            app.logger.error("############################################################")
            app.logger.error(" " + error + " ")
            app.logger.error("############################################################")
            flash(message="error while downloading: " + self.cfg.url_src, category='error')
        except Exception as error:
            app.logger.error("############################################################")
            app.logger.error(error)
            app.logger.error("############################################################")
            flash(message="error after downloading: " + self.cfg.url_src, category='error')
        except AttributeError as aerror:
            app.logger.error("############################################################")
            app.logger.error(aerror)
            app.logger.error("############################################################")
        finally:
            app.logger.info("------------------------------------------------------------")
            app.logger.info(" RKI Landkreise Service Download - download_file [done] ")
            msg = "downloaded: " + self.cfg.cvsfile_name + " "
            flash(msg)
        return self

