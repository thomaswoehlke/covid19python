import os
import wget
from flask import flash
from database import app
from covid19.blueprints.who.who_service_config import WhoServiceConfig


class WhoServiceDownload:
    def __init__(self, database, config: WhoServiceConfig):
        app.logger.debug("------------------------------------------------------------")
        app.logger.debug(" WHO Service Download [init]")
        app.logger.debug("------------------------------------------------------------")
        self.__database = database
        self.cfg = config
        app.logger.debug("------------------------------------------------------------")
        app.logger.debug(" WHO Service Download [ready]")

    def download_file(self):
        app.logger.info(" download - [begin] ")
        app.logger.info("------------------------------------------------------------")
        app.logger.info(" download FILE: "+self.cfg.cvsfile_name+" from "+self.cfg.url_src)
        app.logger.info("------------------------------------------------------------")
        try:
            if os.path.isfile(self.cfg.cvsfile_path):
                os.remove(self.cfg.cvsfile_path)
            data_file = wget.download(self.cfg.url_src, self.cfg.cvsfile_path)
            app.logger.info(" download success: " + data_file + " ")
            flash(self.cfg.msg_ok)
        except RuntimeError as runtimeError:
            app.logger.error("############################################################")
            app.logger.error(" " + runtimeError + " ")
            app.logger.error("############################################################")
            flash(message="error while downloading: " + self.cfg.cvsfile_path, category='error')
        except AttributeError as attributeError:
            app.logger.error("############################################################")
            app.logger.error(attributeError)
            app.logger.error("############################################################")
            flash(message="error after downloading: " + self.cfg.cvsfile_path, category='error')
        except Exception as exception:
            app.logger.error("############################################################")
            app.logger.error(exception)
            app.logger.error("############################################################")
            flash(message="error while downloading: " + self.cfg.cvsfile_path, category='error')
        finally:
            app.logger.info("------------------------------------------------------------")
            app.logger.info(" download - [done] ")
        return self

