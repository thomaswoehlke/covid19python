import os
import wget
from flask import flash
from database import app


class VaccinationServiceDownloadConfig:
    def __init__(self):
        self.limit_nr = 20
        self.data_path = ".."+os.sep+"data"
        self.cvsfile_name = "germany_vaccinations_timeseries_v2.tsv"
        self.url_src_data = "https://impfdashboard.de/static/data/germany_vaccinations_timeseries_v2.tsv"


class VaccinationServiceDownload:
    def __init__(self, database):
        app.logger.info("------------------------------------------------------------")
        app.logger.info(" Vaccination Service Download [init]")
        app.logger.info("------------------------------------------------------------")
        self.__database = database
        self.cfg = VaccinationServiceDownloadConfig()
        app.logger.info("------------------------------------------------------------")
        app.logger.info(" Vaccination Service Download [ready]")

    def download_file(self):
        src_cvsfile_name = self.cfg.data_path+os.sep+self.cfg.cvsfile_name
        app.logger.info(" download - Vaccination [begin] ")
        app.logger.info("------------------------------------------------------------")
        app.logger.info(" FILE: "+self.cfg.cvsfile_name+" ")
        app.logger.info(" FROM: "+self.cfg.url_src_data+" ")
        app.logger.info("------------------------------------------------------------")
        os.makedirs('data', exist_ok=True)
        try:
            if os.path.isfile(src_cvsfile_name):
                os.remove(src_cvsfile_name)
            data_file = wget.download(self.cfg.url_src_data, src_cvsfile_name)
            app.logger.info(" " + data_file + " ")
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
            app.logger.info("------------------------------------------------------------")
            app.logger.info(" download - Vaccination [done] ")
            msg = "downloaded: " + src_cvsfile_name + " "
            flash(msg)
        return self

