from flask import flash

from database import app
from covid19.blueprints.ecdc.ecdc_service_download import EcdcServiceDownload
from covid19.blueprints.ecdc.ecdc_service_import import EcdcServiceImport
from covid19.blueprints.ecdc.ecdc_service_update import EcdcServiceUpdate


# TODO: #111 refactor to new method scheme introduced 07.02.2021
class EcdcService:
    def __init__(self, database):
        app.logger.debug("------------------------------------------------------------")
        app.logger.debug(" ECDC Service [init]")
        app.logger.debug("------------------------------------------------------------")
        self.__database = database
        self.ecdc_service_download = EcdcServiceDownload(database)
        self.ecdc_service_import = EcdcServiceImport(database)
        self.ecdc_service_update = EcdcServiceUpdate(database)
        app.logger.debug("------------------------------------------------------------")
        app.logger.info(" ECDC Service [ready] ")

    def pretask_database_drop_create(self):
        flash("ecdc_service.download started")
        self.ecdc_service_download.download()
        return self

    def task_database_drop_create(self):
        self.ecdc_service_import.import_datafile_to_db()
        self.ecdc_service_update.update_db_short()
        return self

    def run_download_only(self):
        self.ecdc_service_download.download()
        return self

    def run_import_only(self):
        self.ecdc_service_import.import_datafile_to_db()
        return self

    # TODO: #112 implement EcdcService.run_update_dimension_tables_only
    # TODO: #111 refactor to new method scheme itroduced 07.02.2021
    def run_update_dimension_tables_only(self):
        self.ecdc_service_update.update_dimension_tables_only()
        return self

    # TODO: #113 implement EcdcService.run_update_fact_table_incremental_only
    # TODO: #111 refactor to new method scheme itroduced 07.02.2021
    def run_update_fact_table_incremental_only(self):
        self.ecdc_service_update.update_fact_table_incremental_only()
        return self


    # TODO: #114 implement EcdcService.run_update_fact_table_initial_only
    # TODO: #111 refactor to new method scheme itroduced 07.02.2021
    def run_update_fact_table_initial_only(self):
        self.ecdc_service_update.update_fact_table_initial_only()
        return self

    # TODO: #115 implement EcdcService.run_update_star_schema_incremental
    # TODO: #111 refactor to new method scheme itroduced 07.02.2021
    def run_update_star_schema_incremental(self):
        self.ecdc_service_update.update_star_schema_incremental()
        return self


    # TODO: #116 implement EcdcService.run_update_star_schema_initial
    # TODO: #111 refactor to new method scheme itroduced 07.02.2021
    def run_update_star_schema_initial(self):
        self.ecdc_service_update.update_star_schema_initial()
        return self

    # TODO remove DEPRECATED
    # TODO: #111 refactor to new method scheme itroduced 07.02.2021
    def download_DEPRECATED(self):
        app.logger.info(" download [begin]")
        app.logger.info("------------------------------------------------------------")
        self.ecdc_service_download.download()
        app.logger.info(" download [done]")
        app.logger.info("------------------------------------------------------------")
        return self

    # TODO remove DEPRECATED
    # TODO: #111 refactor to new method scheme itroduced 07.02.2021
    def run_update_initial_DEPRECATED(self):
        app.logger.info(" run update [begin]")
        app.logger.info("------------------------------------------------------------")
        self.ecdc_service_import.import_datafile_to_db()
        self.ecdc_service_update.update_db_initial()
        app.logger.info(" run update [done]")
        app.logger.info("------------------------------------------------------------")
        return self

    # TODO remove DEPRECATED
    # TODO: #111 refactor to new method scheme itroduced 07.02.2021
    def run_update_short_DEPRECATED(self):
        app.logger.info(" run update short [begin]")
        app.logger.info("------------------------------------------------------------")
        self.ecdc_service_import.import_datafile_to_db()
        self.ecdc_service_update.update_db_short()
        app.logger.info(" run update short [done]")
        app.logger.info("------------------------------------------------------------")
        return self
