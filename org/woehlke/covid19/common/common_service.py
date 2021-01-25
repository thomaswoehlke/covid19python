import os
from database import app
from org.woehlke.covid19.vaccination.vaccination_service_download import VaccinationServiceDownload
from org.woehlke.covid19.vaccination.vaccination_service_import import VaccinationServiceImport
from org.woehlke.covid19.vaccination.vaccination_service_update import VaccinationServiceUpdate

common_service = None


class CommonService:
    def __init__(self, database):
        app.logger.info("------------------------------------------------------------")
        app.logger.info(" Common Service [init]")
        app.logger.info("------------------------------------------------------------")
        self.__database = database
        self.limit_nr = 20
        self.vaccination_service_download = VaccinationServiceDownload(database)
        self.vaccination_service_import = VaccinationServiceImport(database)
        self.vaccination_service_update = VaccinationServiceUpdate(database)
        app.logger.info("------------------------------------------------------------")
        app.logger.info(" Common Service [ready]")

    def add_new_datum(self, date_string):
        return self