import os
import wget
from datetime import date
from flask import flash

from database import app


class RkiServiceDownload:
    def __init__(self, database):
        app.logger.debug("------------------------------------------------------------")
        app.logger.debug(" RKI Service Download [init]")
        app.logger.debug("------------------------------------------------------------")
        self.__database = database
        self.limit_nr = 20
        datum_heute = date.today().isoformat()
        #
        self.__bundeslaender_cvsfile_name = "RKI_COVID19__"+datum_heute+"__bundeslaender.csv"
        self.__bundeslaender_url_src = "https://opendata.arcgis.com/datasets/ef4b445a53c1406892257fe63129a8ea_0.csv"
        #
        self.__landkreise_cvsfile_name = "RKI_COVID19__"+datum_heute+"__landkreise.csv"
        self.__landkreise_url_src ="https://opendata.arcgis.com/datasets/917fc37a709542548cc3be077a786c17_0.csv"
        #
        app.logger.debug("------------------------------------------------------------")
        app.logger.debug(" RKI Service Download [ready]")

    def __download_file(self, datascope, cvsfile_name, url_src):
        src_cvsfile_path = ".." + os.sep + "data" + os.sep + cvsfile_name
        app.logger.info(" download - RKI "+datascope+" [begin] ")
        app.logger.info("------------------------------------------------------------")
        app.logger.info(" FILE: "+cvsfile_name+" ")
        app.logger.info(" FROM: "+url_src+" ")
        app.logger.info("------------------------------------------------------------")
        #os.makedirs('data', exist_ok=True)
        try:
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

    def download_file(self):
        app.logger.info(" download - RKI [begin] ")
        app.logger.info("------------------------------------------------------------")
        self.__download_file("bundeslaender", self.__bundeslaender_cvsfile_name, self.__bundeslaender_url_src)
        self.__download_file("landkreise", self.__landkreise_cvsfile_name, self.__landkreise_url_src)
        app.logger.info(" download - RKI [done] ")
        app.logger.info("------------------------------------------------------------")
        return self
