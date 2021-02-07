from flask import flash

from database import app
from covid19.blueprints.vaccination.vaccination_service_download import VaccinationServiceDownload
from covid19.blueprints.vaccination.vaccination_service_import import VaccinationServiceImport
from covid19.blueprints.vaccination.vaccination_service_config import VaccinationServiceDownloadConfig


class VaccinationService:
    def __init__(self, database):
        app.logger.debug("------------------------------------------------------------")
        app.logger.debug(" Vaccination Service [init]")
        app.logger.debug("------------------------------------------------------------")
        self.__database = database
        self.cfg = VaccinationServiceDownloadConfig()
        self.vaccination_service_download = VaccinationServiceDownload(database)
        self.vaccination_service_import = VaccinationServiceImport(database)
        app.logger.debug("------------------------------------------------------------")
        app.logger.info(" Vaccination Service [ready]")

    def pretask_database_drop_create(self):
        flash("vaccination_service.run_download started")
        success = self.vaccination_service_download.download_file()
        return self

    def task_database_drop_create(self):
        self.vaccination_service_import.import_file()
        return self

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
