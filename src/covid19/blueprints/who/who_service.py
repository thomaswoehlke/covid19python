from flask import flash

from database import app
from covid19.blueprints.who.who_service_download import WhoServiceDownload
from covid19.blueprints.who.who_service_import import WhoServiceImport
from covid19.blueprints.who.who_service_update import WhoServiceUpdate


class WhoService:
    def __init__(self, database):
        app.logger.debug("------------------------------------------------------------")
        app.logger.debug(" WHO Service [init]")
        app.logger.debug("------------------------------------------------------------")
        self.__database = database
        self.service_download = WhoServiceDownload(database)
        self.service_import = WhoServiceImport(database)
        self.service_update = WhoServiceUpdate(database)
        app.logger.debug("------------------------------------------------------------")
        app.logger.info(" WHO Service [ready]")

    def pretask_database_drop_create(self):
        flash("who_service.run_download started")
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
        app.logger.info(" run_download_only [begin]")
        app.logger.info("------------------------------------------------------------")
        self.service_download.download_file()
        app.logger.info("")
        app.logger.info(" run_download_only [done]")
        app.logger.info("------------------------------------------------------------")
        return self

    def run_import_only(self):
        app.logger.info(" run_import_only [begin]")
        app.logger.info("------------------------------------------------------------")
        self.service_import.import_file()
        app.logger.info("")
        app.logger.info(" run_import_only [done]")
        app.logger.info("------------------------------------------------------------")
        return self

    def run_update_dimension_tables_only(self):
        app.logger.info(" run_update_only [begin]")
        app.logger.info("------------------------------------------------------------")
        self.service_update.update_dimension_tables_only()
        app.logger.info("")
        app.logger.info(" run_update_only [done]")
        app.logger.info("------------------------------------------------------------")
        return self

    def run_update_fact_table_incremental_only(self):
        app.logger.info(" run_update_only [begin]")
        app.logger.info("------------------------------------------------------------")
        self.service_update.update_fact_table_incremental_only()
        app.logger.info("")
        app.logger.info(" run_update_only [done]")
        app.logger.info("------------------------------------------------------------")
        return self

    def run_update_fact_table_initial_only(self):
        app.logger.info(" run_update_initial [begin]")
        app.logger.info("------------------------------------------------------------")
        self.service_update.update_fact_table_initial_only()
        app.logger.info("")
        app.logger.info(" run_update_initial [done]")
        app.logger.info("------------------------------------------------------------")
        return self

    def run_update_star_schema_incremental(self):
        app.logger.info(" run_update_short [begin]")
        app.logger.info("------------------------------------------------------------")
        self.service_import.import_file()
        self.service_update.update_star_schema_incremental()
        app.logger.info("")
        app.logger.info(" run_update_short [done]")
        app.logger.info("------------------------------------------------------------")
        return self

    def run_update_star_schema_initial(self):
        app.logger.info(" run_update_initial_full [begin]")
        app.logger.info("------------------------------------------------------------")
        self.service_import.import_file()
        self.service_update.update_star_schema_initial()
        app.logger.info("")
        app.logger.info(" run_update_initial_full [done]")
        app.logger.info("------------------------------------------------------------")
        return self

    def download_all_files(self):
        self.service_download.download_file()
        return self

