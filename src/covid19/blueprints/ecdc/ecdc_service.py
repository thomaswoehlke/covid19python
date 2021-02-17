from flask import flash

from database import app
from covid19.blueprints.ecdc.ecdc_service_download import EcdcServiceDownload
from covid19.blueprints.ecdc.ecdc_service_import import EcdcServiceImport
from covid19.blueprints.ecdc.ecdc_service_update import EcdcServiceUpdate


class EcdcService:
    def __init__(self, database):
        app.logger.debug("------------------------------------------------------------")
        app.logger.debug(" ECDC Service [init]")
        app.logger.debug("------------------------------------------------------------")
        self.__database = database
        self.service_download = EcdcServiceDownload(database)
        self.service_import = EcdcServiceImport(database)
        self.service_update = EcdcServiceUpdate(database)
        app.logger.debug("------------------------------------------------------------")
        app.logger.info(" ECDC Service [ready] ")

    def pretask_database_drop_create(self):
        flash("ecdc_service.download started")
        self.service_download.download()
        return self

    def task_database_drop_create(self):
        self.service_import.import_datafile_to_db()
        self.service_update.update_db_short()
        return self

    def run_download_only(self):
        self.service_download.download()
        return self

    def run_import_only(self):
        self.service_import.import_datafile_to_db()
        return self

    # TODO: #112 implement EcdcService.run_update_dimension_tables_only
    # TODO: #111 refactor to new method scheme itroduced 07.02.2021
    def run_update_dimension_tables_only(self):
        self.service_update.update_dimension_tables_only()
        return self

    # TODO: #113 implement EcdcService.run_update_fact_table_incremental_only
    # TODO: #111 refactor to new method scheme itroduced 07.02.2021
    def run_update_fact_table_incremental_only(self):
        self.service_update.update_fact_table_incremental_only()
        return self

    # TODO: #114 implement EcdcService.run_update_fact_table_initial_only
    # TODO: #111 refactor to new method scheme itroduced 07.02.2021
    def run_update_fact_table_initial_only(self):
        self.service_update.update_fact_table_initial_only()
        return self

    # TODO: #115 implement EcdcService.run_update_star_schema_incremental
    # TODO: #111 refactor to new method scheme itroduced 07.02.2021
    def run_update_star_schema_incremental(self):
        self.service_import.import_datafile_to_db()
        self.service_update.update_star_schema_incremental()
        return self

    # TODO: #116 implement EcdcService.run_update_star_schema_initial
    # TODO: #111 refactor to new method scheme itroduced 07.02.2021
    def run_update_star_schema_initial(self):
        self.service_import.import_datafile_to_db()
        self.service_update.update_star_schema_initial()
        return self

    def download_all_files(self):
        self.service_download.download_file()
        return self