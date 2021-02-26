from flask import flash

from database import app
from covid19.blueprints.application.application_service_config import ApplicationServiceConfig
from covid19.blueprints.application.application_service_download import ApplicationServiceDownload
from covid19.blueprints.who.who_service_import import WhoServiceImport
from covid19.blueprints.who.who_service_update import WhoServiceUpdate


class WhoService:
    def __init__(self, database):
        app.logger.debug("------------------------------------------------------------")
        app.logger.debug(" WHO Service [init]")
        app.logger.debug("------------------------------------------------------------")
        self.__database = database
        self.cfg = ApplicationServiceConfig.create_config_for_who()
        self.service_download = ApplicationServiceDownload(database, self.cfg)
        self.service_import = WhoServiceImport(database, self.cfg)
        self.service_update = WhoServiceUpdate(database, self.cfg)
        app.logger.debug("------------------------------------------------------------")
        app.logger.info(" WHO Service [ready]")

    def pretask_database_drop_create(self):
        flash("WhoService.pretask_database_drop_create started")
        self.service_download.download_file()
        return self

    def task_database_drop_create(self):
        self.service_import.import_file()
        self.service_update.update_dimension_tables_only()
        self.service_update.update_fact_table_incremental_only()
        return self

    #def run_download_only(self):
    #def run_import_only(self):
    #def run_update_dimension_tables_only(self):
    #def run_update_fact_table_incremental_only(self):
    #def run_update_fact_table_initial_only(self):
    #def run_update_star_schema_incremental(self):
    #def run_update_star_schema_initial(self):

    def run_download_only(self):
        self.service_download.download_file()
        return self

    def run_import_only(self):
        self.service_import.import_file()
        return self

    def run_update_dimension_tables_only(self):
        self.service_update.update_dimension_tables_only()
        return self

    def run_update_fact_table_incremental_only(self):
        self.service_update.update_fact_table_incremental_only()
        return self

    def run_update_fact_table_initial_only(self):
        self.service_update.update_fact_table_initial_only()
        return self

    def run_update_star_schema_incremental(self):
        self.service_import.import_file()
        self.service_update.update_star_schema_incremental()
        return self

    def run_update_star_schema_initial(self):
        self.service_import.import_file()
        self.service_update.update_star_schema_initial()
        return self

    def download_all_files(self):
        self.service_download.download_file()
        return self

    def task_import_all_files(self):
        self.service_import.import_file()
        return self

    def update_dimension_tables_only(self):
        self.service_update.update_dimension_tables_only()
        return self

    def update_fact_table_initial_only(self):
        self.service_update.update_fact_table_initial_only()
        return self

    def update_fact_table_incremental_only(self):
        self.service_update.update_fact_table_incremental_only()
        return self
