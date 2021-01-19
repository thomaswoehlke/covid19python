import os
import wget
from flask import flash
from database import app

rki_service_download = None


class RkiServiceDownload:
    def __init__(self, database):
        app.logger.info("------------------------------------------------------------")
        app.logger.info(" RKI Service Download [init]")
        app.logger.info("------------------------------------------------------------")
        self.__database = database
        self.limit_nr = 20
        self.__who_cvsfile_name = "RKI-COVID-19-DE-data.csv"
        self.__src_who_cvsfile_name = "data"+os.sep+self.__who_cvsfile_name
        self.__src_who_cvsfile_tmp_name = "data"+os.sep+"tmp_"+self.__who_cvsfile_name
        self.__url_src_data = "https://opendata.arcgis.com/datasets/ef4b445a53c1406892257fe63129a8ea_0.csv"

        self.__rki_landkreise_url_src ="https://opendata.arcgis.com/datasets/917fc37a709542548cc3be077a786c17_0.csv"
        app.logger.info("------------------------------------------------------------")
        app.logger.info(" RKI Service Download [ready]")

    def download_file(self):
        app.logger.info(" download - RKI [begin] ")
        app.logger.info("------------------------------------------------------------")
        app.logger.info(" FILE: "+self.__src_who_cvsfile_name+" ")
        app.logger.info(" FROM: "+self.__url_src_data+" ")
        app.logger.info("------------------------------------------------------------")
        os.makedirs('data', exist_ok=True)
        try:
            os.remove(self.__src_who_cvsfile_name)
            data_file = wget.download(self.__url_src_data, self.__src_who_cvsfile_name)
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
            flash(message="error after downloading: " + self.__who_cvsfile_name, category='error')
        except AttributeError as aerror:
            app.logger.info("############################################################")
            app.logger.info(aerror)
            app.logger.info("############################################################")
        finally:
            app.logger.info("------------------------------------------------------------")
            app.logger.info(" download - RKI [done] ")
            msg = "downloaded: " + self.__who_cvsfile_name + " "
            flash(msg)
        return self

