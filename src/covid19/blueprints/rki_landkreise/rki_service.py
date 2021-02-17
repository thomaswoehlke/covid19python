from flask import flash

from database import app
from covid19.blueprints.rki_landkreise.rki_service_config import RkiLandkreiseServiceConfig
from covid19.blueprints.rki_landkreise.rki_service_download import RkiLandkreiseServiceDownload
from covid19.blueprints.rki_landkreise.rki_service_import import RkiLandkreiseServiceImport
from covid19.blueprints.rki_landkreise.rki_service_update import RkiLandkreiseServiceUpdate


class RkiLandkreiseService:
    def __init__(self, database):
        app.logger.debug("------------------------------------------------------------")
        app.logger.debug(" RkiLandkreiseService [init]")
        app.logger.debug("------------------------------------------------------------")
        self.__database = database
        self.cfg = RkiLandkreiseServiceConfig()
        self.service_download = RkiLandkreiseServiceDownload(database, self.cfg)
        self.service_import = RkiLandkreiseServiceImport(database, self.cfg)
        self.service_update = RkiLandkreiseServiceUpdate(database, self.cfg)
        app.logger.debug("------------------------------------------------------------")
        app.logger.info(" RkiLandkreiseService [ready]")

    def pretask_database_drop_create(self):
        flash("RkiLandkreiseService.pretask_database_drop_create started")
        self.service_download.download_file()
        return self

    def task_database_drop_create(self):
        self.service_import.import_file()
        self.service_update.update_dimension_tables_only()
        self.service_update.update_fact_table_incremental_only()
        # TODO: #133 implement RkiBundeslaenderService.task_database_drop_create
        return self

    def run_download_only(self):
        self.service_download.download_file()
        return self

    def run_import_only(self):
        self.service_import.import_file()
        return self

    def run_update_dimension_tables_only(self):
        self.service_update.update_dimension_tables_only()
        # TODO: #134 implement RkiBundeslaenderService.run_update_dimension_tables_only
        return self

    def run_update_fact_table_incremental_only(self):
        self.service_update.update_fact_table_incremental_only()
        # TODO: #135 implement RkiBundeslaenderService.run_update_fact_table_incremental_only
        return self

    def run_update_fact_table_initial_only(self):
        self.service_update.update_fact_table_initial_only()
        # TODO: #136 implement RkiBundeslaenderService.run_update_fact_table_initial_only
        return self

    def run_update_star_schema_incremental(self):
        self.service_import.import_file()
        self.service_update.update_star_schema_incremental()
        # TODO: #137 implement RkiBundeslaenderService.run_update_star_schema_incremental
        return self

    def run_update_star_schema_initial(self):
        self.service_import.import_file()
        self.service_update.update_star_schema_initial()
        # TODO: #138 implement RkiBundeslaenderService.run_update_star_schema_initial
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
