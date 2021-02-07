from flask import flash

from database import app
from covid19.blueprints.rki.rki_service_download import RkiServiceDownload
from covid19.blueprints.rki.rki_service_import import RkiServiceImport
from covid19.blueprints.rki.rki_service_update import RkiServiceUpdate


# TODO: #132 refactor RkiService to new method scheme introduced 07.02.2021
class RkiService:
    def __init__(self, database):
        app.logger.debug("------------------------------------------------------------")
        app.logger.debug(" RKI Service [init]")
        app.logger.debug("------------------------------------------------------------")
        self.__database = database
        self.limit_nr = 20
        self.service_download = RkiServiceDownload(database)
        self.service_import = RkiServiceImport(database)
        self.service_update = RkiServiceUpdate(database)
        app.logger.debug("------------------------------------------------------------")
        app.logger.info(" RKI Service [ready]")

    def pretask_database_drop_create(self):
        flash("rki_service.run_download started")
        self.service_download.download_file()
        return self

    def task_database_drop_create(self):
        # TODO: #132 refactor RkiService to new method scheme introduced 07.02.2021
        # TODO: #133 implement RkiService.task_database_drop_create
        return self

    def run_download_only(self):
        self.service_download.download_file()
        return self

    def run_import_only(self):
        self.service_import.import_file()
        return self

    def run_update_dimension_tables_only(self):
        # TODO: #132 refactor RkiService to new method scheme introduced 07.02.2021
        # TODO: #134 implement RkiService.run_update_dimension_tables_only
        return self

    def run_update_fact_table_incremental_only(self):
        # TODO: #132 refactor RkiService to new method scheme introduced 07.02.2021
        # TODO: #135 implement RkiService.run_update_fact_table_incremental_only
        return self

    def run_update_fact_table_initial_only(self):
        # TODO: #132 refactor RkiService to new method scheme introduced 07.02.2021
        # TODO: #136 implement RkiService.run_update_fact_table_initial_only
        return self

    def run_update_star_schema_incremental(self):
        # TODO: #132 refactor RkiService to new method scheme introduced 07.02.2021
        # TODO: #137 implement RkiService.run_update_star_schema_incremental
        return self

    def run_update_star_schema_initial(self):
        # TODO: #132 refactor RkiService to new method scheme introduced 07.02.2021
        # TODO: #138 implement RkiService.run_update_star_schema_initial
        return self

    # TODO: #132 refactor RkiService to new method scheme introduced 07.02.2021
    def run_download(self):
        app.logger.info(" run update [begin]")
        app.logger.info("------------------------------------------------------------")
        success = self.service_download.download_file()
        app.logger.info("")
        app.logger.info(" run update [done]")
        app.logger.info("------------------------------------------------------------")
        return success

    # TODO: #132 refactor RkiService to new method scheme introduced 07.02.2021
    def run_update(self, import_file=True):
        app.logger.info(" run update [begin]")
        app.logger.info("------------------------------------------------------------")
        if import_file:
            self.service_import.import_file()
        self.service_update.update_db()
        app.logger.info("")
        app.logger.info(" run update [done]")
        app.logger.info("------------------------------------------------------------")
        return self

    # TODO: #132 refactor RkiService to new method scheme introduced 07.02.2021
    def run_update_short(self, import_file=True):
        app.logger.info(" run update short [begin]")
        app.logger.info("------------------------------------------------------------")
        if import_file:
            self.service_import.import_file()
        self.service_update.update_db_short()
        app.logger.info("")
        app.logger.info(" run update short [done]")
        app.logger.info("------------------------------------------------------------")
        return self

    # TODO: #132 refactor RkiService to new method scheme introduced 07.02.2021
    def run_update_initial(self, import_file=True):
        app.logger.info(" run update initial [begin]")
        app.logger.info("------------------------------------------------------------")
        if import_file:
            self.service_import.import_file()
        self.service_update.update_db_initial()
        app.logger.info("")
        app.logger.info(" run update initial [done]")
        app.logger.info("------------------------------------------------------------")
        return self
