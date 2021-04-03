import os
import wget
import subprocess
# from flask import flash
from database import app
from covid19.blueprints.application.application_service_config import ApplicationServiceConfig


class ApplicationServiceDownload:
    def __init__(self, database, config: ApplicationServiceConfig):
        app.logger.debug("------------------------------------------------------------")
        app.logger.debug(" ApplicationServiceDownload [init]")
        app.logger.debug("------------------------------------------------------------")
        self.__database = database
        self.cfg = config
        app.logger.debug("------------------------------------------------------------")
        app.logger.debug(" ApplicationServiceDownload [ready]")

    #def __log_error(self, error_msg: str, error_obj):
    #    log_msg = self.cfg.slug[0] + " " + self.cfg.msg_error() + " " + error_msg + " "
    #    app.logger.error(log_msg)
    #    flash(message=log_msg, category='error')
    #    return self
    #
    #def __log_success(self, data_file):
    #    slug = self.cfg.slug[0]
    #    log_msg1 = " " + slug + " | download success: " + data_file + " "
    #    log_msg2 = " " + slug + " | " + self.cfg.msg_ok
    #    app.logger.info(log_msg1)
    #    app.logger.info(log_msg2)
    #    flash(log_msg1)
    #    return self

    def __prepare_download(self):
        os.makedirs(self.cfg.data_path, exist_ok=True)
        if os.path.isfile(self.cfg.cvsfile_path):
            os.remove(self.cfg.cvsfile_path)
        return self

    def __download_with_wget(self):
        data_file = wget.download(self.cfg.url_src, self.cfg.cvsfile_path)
        app.logger.info(data_file)
        return self

    def __download_with_subprocess_and_os_native_wget(self):
        orig_workdir = os.getcwd()
        os.chdir(self.cfg.data_path)
        my_cmds = [
            'wget ' + self.cfg.url_src,
            'mv ' + self.cfg.cvsfile_name + ' ' + self.cfg.cvsfile_path,
        ]
        # subprocess.Popen(my_cmd, shell=True)
        for my_cmd in my_cmds:
            retcode = subprocess.call(my_cmd, shell=True)
            app.logger.info(retcode)
            app.logger.info(my_cmd[0])
        os.chdir(orig_workdir)
        return self

    def download_file(self):
        app.logger.info(" download_file - [begin] ")
        app.logger.info("------------------------------------------------------------")
        app.logger.info(self.cfg.msg_job)
        app.logger.info("------------------------------------------------------------")
        try:
            self.__prepare_download()
            if self.cfg.slug[0] == 'owid':
                self.__download_with_subprocess_and_os_native_wget()
            else:
                self.__download_with_wget()
        except RuntimeError as runtimeError:
            app.logger.error(" RuntimeError: ")
            app.logger.error(runtimeError)
        except OSError as osError:
            app.logger.error(" OSError: ")
            app.logger.error(osError)
        except AttributeError as attributeError:
            app.logger.error(" AttributeError: ")
            app.logger.error(attributeError)
        except Exception as exception:
            app.logger.error(" Exception: ")
            app.logger.error(exception)
        finally:
            app.logger.info("------------------------------------------------------------")
            app.logger.info(" download_file - [done] ")
        return self
