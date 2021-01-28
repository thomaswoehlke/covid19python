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
        #
        self.__bundeslaender_cvsfile_name = "RKI-COVID-19-bundeslaender-data.csv"
        self.__bundeslaender_url_src = "https://opendata.arcgis.com/datasets/ef4b445a53c1406892257fe63129a8ea_0.csv"
        #
        self.__landkreise_cvsfile_name = "RKI-COVID-19-landkreise-data.csv"
        self.__landkreise_url_src ="https://opendata.arcgis.com/datasets/917fc37a709542548cc3be077a786c17_0.csv"
        #
        app.logger.info("------------------------------------------------------------")
        app.logger.info(" RKI Service Download [ready]")

    def __download_file(self, datascope, cvsfile_name, url_src):
        src_cvsfile_path = "data" + os.sep + cvsfile_name
        app.logger.info(" download - RKI "+datascope+" [begin] ")
        app.logger.info("------------------------------------------------------------")
        app.logger.info(" FILE: "+cvsfile_name+" ")
        app.logger.info(" FROM: "+url_src+" ")
        app.logger.info("------------------------------------------------------------")
        os.makedirs('data', exist_ok=True)
        try:
            os.remove(src_cvsfile_path)
            data_file = wget.download(url_src, src_cvsfile_path)
            app.logger.info(" " + data_file + " ")
        except RuntimeError as error:
            app.logger.info("############################################################")
            app.logger.info(" " + error + " ")
            app.logger.info("############################################################")
            flash(message="error while downloading: " + url_src, category='error')
        except Exception as error:
            app.logger.info("############################################################")
            app.logger.info(error)
            app.logger.info("############################################################")
            flash(message="error after downloading: " + url_src, category='error')
        except AttributeError as aerror:
            app.logger.info("############################################################")
            app.logger.info(aerror)
            app.logger.info("############################################################")
        finally:
            app.logger.info("------------------------------------------------------------")
            app.logger.info(" download - RKI "+datascope+" [done] ")
            msg = "downloaded: " + cvsfile_name + " "
            flash(msg)
        return self

    def download_file(self):
        app.logger.info(" download - RKI [begin] ")
        app.logger.info("------------------------------------------------------------")
        self.__download_file("bundeslaender", self.__bundeslaender_cvsfile_name, self.__bundeslaender_url_src)
        self.__download_file("landkreise", self.__landkreise_cvsfile_name, self.__landkreise_url_src)
        app.logger.info(" download - RKI [done] ")
        app.logger.info("------------------------------------------------------------")
        return self

