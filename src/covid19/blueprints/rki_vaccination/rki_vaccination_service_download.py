import os
import wget
import subprocess
from flask import flash
from database import app
from covid19.blueprints.rki_vaccination.rki_vaccination_service_config import RkiVaccinationServiceConfig


class RkiVaccinationServiceDownload:
    def __init__(self, database, config: RkiVaccinationServiceConfig):
        app.logger.debug("------------------------------------------------------------")
        app.logger.debug(" "+self.cfg+" Download Service [init]")
        app.logger.debug("------------------------------------------------------------")
        self.__database = database
        self.cfg = config
        app.logger.debug("------------------------------------------------------------")
        app.logger.debug(" "+self.cfg+" Download Service [ready]")

    def __log_error(self, error_msg: str):
        flash_msg = self.cfg.msg_error + error_msg
        flash(message=flash_msg, category='error')
        app.logger.error("############################################################")
        app.logger.error(flash_msg)
        app.logger.error("############################################################")
        return self

    def __log_success(self, data_file):
        app.logger.info(" download success: " + data_file + " ")
        app.logger.info(self.cfg.msg_ok)
        flash(self.cfg.msg_ok)
        return self

    def __prepare_download(self):
        os.makedirs(self.cfg.data_path, exist_ok=True)
        if os.path.isfile(self.cfg.cvsfile_path):
            os.remove(self.cfg.cvsfile_path)
        return self

    def __download_with_wget(self, src_url: str, target_file_path: str):
        data_file = wget.download(src_url, target_file_path)
        self.__log_success(data_file)
        return self

    def __download_with_subprocess_and_os_native_wget(self):
        orig_workdir = os.getcwd()
        os.chdir(self.cfg.data_path)
        my_cmd = ['wget ' + self.cfg.url_src]
        subprocess.Popen(my_cmd, shell=True)
        os.chdir(orig_workdir)
        return self

    def download_file(self):
        app.logger.info(" download_file - "+self.cfg+" [begin] ")
        app.logger.info("------------------------------------------------------------")
        app.logger.info(self.cfg.msg_job)
        app.logger.info("------------------------------------------------------------")
        try:
            self.__prepare_download()
            self.__download_with_wget(self.cfg.url_src, self.cfg.cvsfile_path)
        except RuntimeError as runtimeError:
            self.__log_error(" RuntimeError: " + runtimeError + " ")
        except OSError as osError:
            self.__log_error(" OSError: " + osError + " ")
        except AttributeError as attributeError:
            self.__log_error(" AttributeError: " + attributeError + " ")
        except Exception as exception:
            self.__log_error(" Exception: " + exception)
        finally:
            app.logger.info("------------------------------------------------------------")
            app.logger.info(" download_file - "+self.cfg+" [done] ")
        return self
