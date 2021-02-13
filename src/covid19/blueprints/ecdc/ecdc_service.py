from flask import flash

from database import app
from covid19.blueprints.ecdc.europe_service_download import EuropeServiceDownload
from covid19.blueprints.ecdc.europe_service_import import EuropeServiceImport
from covid19.blueprints.ecdc.europe_service_update import EuropeServiceUpdate


# TODO: #111 refactor to new method scheme itroduced 07.02.2021
class EuropeService:
    def __init__(self, database):
        app.logger.debug("------------------------------------------------------------")
        app.logger.debug(" Europe Service [init]")
        app.logger.debug("------------------------------------------------------------")
        self.__database = database
        self.europe_service_download = EuropeServiceDownload(database)
        self.europe_service_import = EuropeServiceImport(database)
        self.europe_service_update = EuropeServiceUpdate(database)
        app.logger.debug("------------------------------------------------------------")
        app.logger.info(" Europe Service [ready] ")

    def pretask_database_drop_create(self):
        flash("europe_service.download started")
        self.europe_service_download.download()
        return self

    def task_database_drop_create(self):
        self.europe_service_import.import_datafile_to_db()
        self.europe_service_update.update_db_short()
        return self

    def run_download_only(self):
        self.europe_service_download.download()
        return self

    def run_import_only(self):
        self.europe_service_import.import_datafile_to_db()
        return self

    # TODO: #112 implement EuropeService.run_update_dimension_tables_only
    # TODO: #111 refactor to new method scheme itroduced 07.02.2021
    def run_update_dimension_tables_only(self):
        return self

    # TODO: #113 implement EuropeService.run_update_fact_table_incremental_only
    # TODO: #111 refactor to new method scheme itroduced 07.02.2021
    def run_update_fact_table_incremental_only(self):
        return self


    # TODO: #114 implement EuropeService.run_update_fact_table_initial_only
    # TODO: #111 refactor to new method scheme itroduced 07.02.2021
    def run_update_fact_table_initial_only(self):
        return self

    # TODO: #115 implement EuropeService.run_update_star_schema_incremental
    # TODO: #111 refactor to new method scheme itroduced 07.02.2021
    def run_update_star_schema_incremental(self):
        return self


    # TODO: #116 implement EuropeService.run_update_star_schema_initial
    # TODO: #111 refactor to new method scheme itroduced 07.02.2021
    def run_update_star_schema_initial(self):
        return self

    # TODO remove DEPRECATED
    # TODO: #111 refactor to new method scheme itroduced 07.02.2021
    def download_DEPRECATED(self):
        app.logger.info(" download [begin]")
        app.logger.info("------------------------------------------------------------")
        self.europe_service_download.download()
        app.logger.info(" download [done]")
        app.logger.info("------------------------------------------------------------")
        return self

    # TODO remove DEPRECATED
    # TODO: #111 refactor to new method scheme itroduced 07.02.2021
    def run_update_initial_DEPRECATED(self):
        app.logger.info(" run update [begin]")
        app.logger.info("------------------------------------------------------------")
        self.europe_service_import.import_datafile_to_db()
        self.europe_service_update.update_db_initial()
        app.logger.info(" run update [done]")
        app.logger.info("------------------------------------------------------------")
        return self

    # TODO remove DEPRECATED
    # TODO: #111 refactor to new method scheme itroduced 07.02.2021
    def run_update_short_DEPRECATED(self):
        app.logger.info(" run update short [begin]")
        app.logger.info("------------------------------------------------------------")
        self.europe_service_import.import_datafile_to_db()
        self.europe_service_update.update_db_short()
        app.logger.info(" run update short [done]")
        app.logger.info("------------------------------------------------------------")
        return self
