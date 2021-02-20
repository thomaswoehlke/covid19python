import os
import wget
import subprocess
from flask import flash
from database import app
from covid19.blueprints.application.application_service_config import ApplicationServiceConfig


class ApplicationServiceDownload:
    def __init__(self, database, config: ApplicationServiceConfig):
        app.logger.debug("------------------------------------------------------------")
        app.logger.debug(" "+self.cfg.slug+" Download Service [init]")
        app.logger.debug("------------------------------------------------------------")
        self.__database = database
        self.cfg = config
        app.logger.debug("------------------------------------------------------------")
        app.logger.debug(" "+self.cfg.slug+" Download Service [ready]")

    def __log_error(self, error_msg: str):
        flash_msg = self.cfg.msg_error + error_msg
        flash(message=flash_msg, category='error')
        app.logger.error(self.cfg.slug+"############################################################")
        app.logger.error(self.cfg.slug+flash_msg)
        app.logger.error(self.cfg.slug+"############################################################")
        return self

    def __log_success(self, data_file):
        app.logger.info(self.cfg.slug+" download success: " + data_file + " ")
        app.logger.info(self.cfg.slug+self.cfg.msg_ok)
        flash(self.cfg.msg_ok)
        return self

    def __prepare_download(self):
        os.makedirs(self.cfg.data_path, exist_ok=True)
        if os.path.isfile(self.cfg.cvsfile_path):
            os.remove(self.cfg.cvsfile_path)
        return self

    def __download_with_wget(self):
        data_file = wget.download(self.cfg.url_src, self.cfg.cvsfile_path)
        self.__log_success(data_file)
        return self

    def __download_with_subprocess_and_os_native_wget(self):
        orig_workdir = os.getcwd()
        os.chdir(self.cfg.data_path)
        my_cmd = ['wget ' + self.cfg.url_src]
        subprocess.Popen(my_cmd, shell=True)
        os.chdir(orig_workdir)
        self.__log_success(my_cmd[0])
        return self

    def download_file(self):
        app.logger.info(" download_file - "+self.cfg.slug+" [begin] ")
        app.logger.info("------------------------------------------------------------")
        app.logger.info(self.cfg.msg_job)
        app.logger.info("------------------------------------------------------------")
        try:
            self.__prepare_download()
            if self.cfg.slug == 'owid':
                self.__download_with_subprocess_and_os_native_wget()
            else:
                self.__download_with_wget()
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
            app.logger.info(" download_file - "+self.cfg.slug+" [done] ")
        return self
