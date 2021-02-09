from flask import flash

from database import app
from covid19.blueprints.vaccination.vaccination_service_download import VaccinationServiceDownload
from covid19.blueprints.vaccination.vaccination_service_import import VaccinationServiceImport
from covid19.blueprints.vaccination.vaccination_service_config import VaccinationServiceConfig
from covid19.blueprints.vaccination.vaccination_service_update import VaccinationServiceUpdate


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
        self.vaccination_service_udpate.update_star_schema_initial()
        return self

    def run_download_only(self):
        self.vaccination_service_download.download_file()
        return self

    def run_import_only(self):
        self.vaccination_service_import.import_file()
        return self

    def run_update_dimension_tables_only(self):
        self.vaccination_service_udpate.update_dimension_tables_only()
        return self

    def run_update_fact_table_incremental_only(self):
        self.vaccination_service_udpate.update_fact_table_incremental_only()
        return self

    def run_update_fact_table_initial_only(self):
        self.vaccination_service_udpate.update_fact_table_initial_only()
        return self

    def run_update_star_schema_incremental(self):
        self.vaccination_service_udpate.update_star_schema_incremental()
        return self

    def run_update_star_schema_initial(self):
        self.run_import_only()
        self.vaccination_service_udpate.update_star_schema_initial()
        return self

    # TODO remove DEPRECATED
    #def run_download_DEPRECATED(self):
    #    app.logger.info(" run update [begin]")
    #    app.logger.info("------------------------------------------------------------")
    #    success = self.vaccination_service_download.download_file()
    #    app.logger.info("")
    #    app.logger.info(" run update [done]")
    #    app.logger.info("------------------------------------------------------------")
    #    return success

    # TODO remove DEPRECATED
    #def run_update_initial_DEPRECATED(self):
    #    app.logger.info(" run update initial [begin]")
    #    app.logger.info("------------------------------------------------------------")
    #    self.vaccination_service_import.import_file()
    #    app.logger.info("")
    #    app.logger.info(" run update initial [done]")
    #    app.logger.info("------------------------------------------------------------")
    #    return self
