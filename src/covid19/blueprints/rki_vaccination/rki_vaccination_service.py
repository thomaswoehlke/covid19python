from flask import flash

from database import app
from covid19.blueprints.rki_vaccination.rki_vaccination_service_download import RkiVaccinationServiceDownload
from covid19.blueprints.rki_vaccination.rki_vaccination_service_import import RkiVaccinationServiceImport
from covid19.blueprints.rki_vaccination.rki_vaccination_service_config import RkiVaccinationServiceConfig
from covid19.blueprints.rki_vaccination.rki_vaccination_service_update import RkiVaccinationServiceUpdate


class RkiVaccinationService:
    def __init__(self, database):
        app.logger.debug("------------------------------------------------------------")
        app.logger.debug(" Vaccination Service [init]")
        app.logger.debug("------------------------------------------------------------")
        self.__database = database
        self.cfg = RkiVaccinationServiceConfig()
        self.service_download = RkiVaccinationServiceDownload(database)
        self.service_import = RkiVaccinationServiceImport(database)
        self.service_udpate = RkiVaccinationServiceUpdate(database)
        app.logger.debug("------------------------------------------------------------")
        app.logger.info(" Vaccination Service [ready]")

    def pretask_database_drop_create(self):
        flash("vaccination_service.run_download started")
        self.service_download.download_file()
        return self

    def task_database_drop_create(self):
        self.service_import.import_file()
        self.service_udpate.update_star_schema_initial()
        return self

    def run_download_only(self):
        self.service_download.download_file()
        return self

    def run_import_only(self):
        self.service_import.import_file()
        return self

    def run_update_dimension_tables_only(self):
        self.service_udpate.update_dimension_tables_only()
        return self

    def run_update_fact_table_incremental_only(self):
        self.service_udpate.update_fact_table_incremental_only()
        return self

    def run_update_fact_table_initial_only(self):
        self.service_udpate.update_fact_table_initial_only()
        return self

    def run_update_star_schema_incremental(self):
        self.service_udpate.update_star_schema_incremental()
        return self

    def run_update_star_schema_initial(self):
        self.run_import_only()
        self.service_udpate.update_star_schema_initial()
        return self

    def download_all_files(self):
        self.service_download.download_file()
        return self