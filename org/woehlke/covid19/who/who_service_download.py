import os
import wget
from database import app

who_service_download = None


class WhoServiceDownload:
    def __init__(self, database):
        app.logger.info("------------------------------------------------------------")
        app.logger.info(" WHO Service Download [init]")
        app.logger.info("------------------------------------------------------------")
        self.__database = database
        self.limit_nr = 20
        self.__who_cvsfile_name = "WHO-COVID-19-global-data.csv"
        self.__src_who_cvsfile_name = "data"+os.sep+self.__who_cvsfile_name
        self.__src_who_cvsfile_tmp_name = "data"+os.sep+"tmp_"+self.__who_cvsfile_name
        self.__url_src_data = "https://covid19.who.int/"+self.__who_cvsfile_name
        app.logger.info("------------------------------------------------------------")
        app.logger.info(" WHO Service Download [ready]")

    def download_file(self):
        app.logger.info(" download - WHO [begin] ")
        app.logger.info("------------------------------------------------------------")
        app.logger.info(" FILE: "+self.__src_who_cvsfile_name)
        app.logger.info(" FROM: "+self.__url_src_data)
        app.logger.info("------------------------------------------------------------")
        os.makedirs('data', exist_ok=True)
        try:
            #os.remove(self.__src_who_cvsfile_name)
            os.chdir("data")
            data_file = wget.download(self.__url_src_data)
            os.renames(data_file, self.__who_cvsfile_name)
            for my_datafile in os.listdir():
                app.logger.info(my_datafile)
            os.chdir("..")
        except Exception as error:
            app.logger.warning("############################################################")
            app.logger.warning(error)
            app.logger.warning("############################################################")
        finally:
            app.logger.info("------------------------------------------------------------")
            app.logger.info(" download - WHO [done] ")
        return self
