import os
import wget
from datetime import date
from flask import flash

from database import app
from covid19.blueprints.rki_bundeslaender.rki_service_config import RkiBundeslaenderServiceConfig


# RkiBundeslaenderServiceDownload
# TODO: #123 split RkiService into two Services: RkiBundeslaenderService and RkiLandkreiseService
# TODO: #139 refactor RkiBundeslaenderServiceDownload to new method scheme introduced 07.02.2021
class RkiBundeslaenderServiceDownload:
    def __init__(self, database):
        app.logger.debug("------------------------------------------------------------")
        app.logger.debug(" RKI Service Download [init]")
        app.logger.debug("------------------------------------------------------------")
        self.__database = database
        self.cfg = RkiBundeslaenderServiceConfig()
        app.logger.debug("------------------------------------------------------------")
        app.logger.debug(" RKI Service Download [ready]")

    # TODO: #123 split RkiBundeslaenderService into two Services, one for bundeslaender and one for landkreise
    def __download_file(self):
        app.logger.info(" download - RKI "+datascope+" [begin] ")
        app.logger.info("------------------------------------------------------------")
        app.logger.info(" FILE: "+cvsfile_name+" <- "+url_src)
        app.logger.info("------------------------------------------------------------")
        try:
            os.makedirs(data_path, exist_ok=True)
            if os.path.isfile(src_cvsfile_path):
                os.remove(src_cvsfile_path)
            data_file = wget.download(url_src, src_cvsfile_path)
            app.logger.info(" " + data_file + " ")
        except RuntimeError as error:
            app.logger.error("############################################################")
            app.logger.error(" " + error + " ")
            app.logger.error("############################################################")
            flash(message="error while downloading: " + url_src, category='error')
        except Exception as error:
            app.logger.error("############################################################")
            app.logger.error(error)
            app.logger.error("############################################################")
            flash(message="error after downloading: " + url_src, category='error')
        except AttributeError as aerror:
            app.logger.error("############################################################")
            app.logger.error(aerror)
            app.logger.error("############################################################")
        finally:
            app.logger.info("------------------------------------------------------------")
            app.logger.info(" download - RKI "+datascope+" [done] ")
            msg = "downloaded: " + cvsfile_name + " "
            flash(msg)
        return self
