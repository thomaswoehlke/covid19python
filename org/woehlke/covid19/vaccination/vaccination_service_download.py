import os
import wget
from flask import flash
from database import app

vaccination_service_download = None


class VaccinationServiceDownload:
    def __init__(self, database):
        app.logger.info("------------------------------------------------------------")
        app.logger.info(" Vaccination Service Download [init]")
        app.logger.info("------------------------------------------------------------")
        self.__database = database
        self.limit_nr = 20
        self.__cvsfile_name = "germany_vaccinations_timeseries_v2.tsv"
        self.__src_cvsfile_name = "data"+os.sep+self.__cvsfile_name
        self.__src_cvsfile_tmp_name = "data"+os.sep+"tmp_"+self.__cvsfile_name
        self.__url_src_data = "https://impfdashboard.de/static/data/germany_vaccinations_timeseries_v2.tsv"
        app.logger.info("------------------------------------------------------------")
        app.logger.info(" Vaccination Service Download [ready]")

    def download_file(self):
        app.logger.info(" download - Vaccination [begin] ")
        app.logger.info("------------------------------------------------------------")
        app.logger.info(" FILE: "+self.__src_cvsfile_name+" ")
        app.logger.info(" FROM: "+self.__url_src_data+" ")
        app.logger.info("------------------------------------------------------------")
        os.makedirs('data', exist_ok=True)
        try:
            os.remove(self.__src_cvsfile_name)
            data_file = wget.download(self.__url_src_data, self.__src_cvsfile_name)
            app.logger.info(" " + data_file + " ")
        except RuntimeError as error:
            app.logger.info("############################################################")
            app.logger.info(" " + error + " ")
            app.logger.info("############################################################")
            flash(message="error while downloading: " + self.__url_src_data, category='error')
        except Exception as error:
            app.logger.info("############################################################")
            app.logger.info(error)
            app.logger.info("############################################################")
            flash(message="error after downloading: " + self.__cvsfile_name, category='error')
        except AttributeError as aerror:
            app.logger.info("############################################################")
            app.logger.info(aerror)
            app.logger.info("############################################################")
        finally:
            app.logger.info("------------------------------------------------------------")
            app.logger.info(" download - Vaccination [done] ")
            msg = "downloaded: " + self.__cvsfile_name + " "
            flash(msg)
        return self

