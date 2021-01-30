from database import app
from covid19.oodm.europe.europe_service_download import EuropeServiceDownload
from covid19.oodm.europe.europe_service_import import EuropeServiceImport
from covid19.oodm.europe.europe_service_update import EuropeServiceUpdate


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

    def download(self):
        app.logger.info(" download [begin]")
        app.logger.info("------------------------------------------------------------")
        self.europe_service_download.download()
        app.logger.info(" download [done]")
        app.logger.info("------------------------------------------------------------")
        return self

    def run_update_initial(self):
        app.logger.info(" run update [begin]")
        app.logger.info("------------------------------------------------------------")
        self.europe_service_import.import_datafile_to_db()
        self.europe_service_update.update_db_initial()
        app.logger.info(" run update [done]")
        app.logger.info("------------------------------------------------------------")
        return self

    def run_update_short(self):
        app.logger.info(" run update short [begin]")
        app.logger.info("------------------------------------------------------------")
        self.europe_service_import.import_datafile_to_db()
        self.europe_service_update.update_db_short()
        app.logger.info(" run update short [done]")
        app.logger.info("------------------------------------------------------------")
        return self
