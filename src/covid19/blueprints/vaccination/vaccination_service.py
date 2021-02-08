from flask import flash

from database import app
from covid19.blueprints.vaccination.vaccination_service_download import VaccinationServiceDownload
from covid19.blueprints.vaccination.vaccination_service_import import VaccinationServiceImport
from covid19.blueprints.vaccination.vaccination_service_config import VaccinationServiceConfig
from covid19.blueprints.vaccination.vaccination_service_update import VaccinationServiceUpdate


# TODO: #90 refactor VaccinationService to new method scheme introduced 07.02.2021
class VaccinationService:
    def __init__(self, database):
        app.logger.debug("------------------------------------------------------------")
        app.logger.debug(" Vaccination Service [init]")
        app.logger.debug("------------------------------------------------------------")
        self.__database = database
        self.cfg = VaccinationServiceConfig()
        self.vaccination_service_download = VaccinationServiceDownload(database)
        self.vaccination_service_import = VaccinationServiceImport(database)
        self.vaccination_service_udpate = VaccinationServiceUpdate(database)
        app.logger.debug("------------------------------------------------------------")
        app.logger.info(" Vaccination Service [ready]")

    def pretask_database_drop_create(self):
        flash("vaccination_service.run_download started")
        self.vaccination_service_download.download_file()
        return self

    def task_database_drop_create(self):
        self.vaccination_service_import.import_file()
        return self

    def run_download_only(self):
        # TODO: #90 refactor VaccinationService to new method scheme introduced 07.02.2021
        # TODO: #91 implement VaccinationService.run_download_only
        self.vaccination_service_download.download_file()
        return self

    def run_import_only(self):
        # TODO: #90 refactor VaccinationService to new method scheme introduced 07.02.2021
        # TODO: #92 implement VaccinationService.run_import_only
        self.vaccination_service_import.import_file()
        return self

    def run_update_dimension_tables_only(self):
        # TODO: #90 refactor VaccinationService to new method scheme introduced 07.02.2021
        # TODO: #93 implement VaccinationService.run_update_dimension_tables_only
        self.vaccination_service_udpate.update_dimension_tables_only()
        return self

    def run_update_fact_table_incremental_only(self):
        # TODO: #90 refactor VaccinationService to new method scheme introduced 07.02.2021
        # TODO: #94 implement VaccinationService.run_update_fact_table_incremental_only
        self.vaccination_service_udpate.update_fact_table_incremental_only()
        return self

    def run_update_fact_table_initial_only(self):
        # TODO: #90 refactor VaccinationService to new method scheme introduced 07.02.2021
        # TODO: #95 implement VaccinationService.run_update_fact_table_initial_only
        self.vaccination_service_udpate.update_fact_table_initial_only()
        return self

    def run_update_star_schema_incremental(self):
        # TODO: #90 refactor VaccinationService to new method scheme introduced 07.02.2021
        # TODO: #96 implement VaccinationService.run_update_star_schema_incremental
        self.vaccination_service_udpate.update_star_schema_incremental()
        return self

    def run_update_star_schema_initial(self):
        # TODO: #90 refactor VaccinationService to new method scheme introduced 07.02.2021
        # TODO: #97 implement VaccinationService.run_update_star_schema_initial
        self.run_import_only()
        self.vaccination_service_udpate.update_star_schema_initial()
        return self

    # TODO: #90 refactor VaccinationService to new method scheme introduced 07.02.2021
    def run_download(self):
        app.logger.info(" run update [begin]")
        app.logger.info("------------------------------------------------------------")
        success = self.vaccination_service_download.download_file()
        app.logger.info("")
        app.logger.info(" run update [done]")
        app.logger.info("------------------------------------------------------------")
        return success

    # TODO: #90 refactor VaccinationService to new method scheme introduced 07.02.2021
    def run_update_initial(self):
        app.logger.info(" run update initial [begin]")
        app.logger.info("------------------------------------------------------------")
        self.vaccination_service_import.import_file()
        app.logger.info("")
        app.logger.info(" run update initial [done]")
        app.logger.info("------------------------------------------------------------")
        return self
