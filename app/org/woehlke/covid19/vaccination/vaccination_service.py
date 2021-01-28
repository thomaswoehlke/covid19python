import os

from database import app
from app.org.woehlke.covid19.vaccination.vaccination_service_download import VaccinationServiceDownload
from app.org.woehlke.covid19.vaccination.vaccination_service_import import VaccinationServiceImport


class VaccinationService:
    def __init__(self, database):
        app.logger.info("------------------------------------------------------------")
        app.logger.info(" Vaccination Service [init]")
        app.logger.info("------------------------------------------------------------")
        self.__database = database
        self.limit_nr = 20
        self.__cvsfile_name = "germany_vaccinations_timeseries_v2.tsv"
        self.__src_cvsfile_name = "data"+os.sep+self.__cvsfile_name
        self.__src_cvsfile_tmp_name = "data"+os.sep+"tmp_"+self.__cvsfile_name
        self.__url_src_data = "https://impfdashboard.de/static/data/germany_vaccinations_timeseries_v2.tsv"
        self.vaccination_service_download = VaccinationServiceDownload(database)
        self.vaccination_service_import = VaccinationServiceImport(database)
        app.logger.info("------------------------------------------------------------")
        app.logger.info(" Vaccination Service [ready]")

    def run_download(self):
        app.logger.info(" run update [begin]")
        app.logger.info("------------------------------------------------------------")
        success = self.vaccination_service_download.download_file()
        app.logger.info("")
        app.logger.info(" run update [done]")
        app.logger.info("------------------------------------------------------------")
        return success

    def run_update_initial(self):
        app.logger.info(" run update initial [begin]")
        app.logger.info("------------------------------------------------------------")
        self.vaccination_service_import.import_file()
        app.logger.info("")
        app.logger.info(" run update initial [done]")
        app.logger.info("------------------------------------------------------------")
        return self
