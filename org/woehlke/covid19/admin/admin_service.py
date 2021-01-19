import os
from database import app

admin_service = None


class AdminService:
    def __init__(self, database):
        app.logger.info("------------------------------------------------------------")
        app.logger.info(" Admin Service [init]")
        app.logger.info("------------------------------------------------------------")
        self.__database = database
        self.limit_nr = 20
        app.logger.info("------------------------------------------------------------")
        app.logger.info(" Admin Service [ready]")

    def run_admin_database_dump(self):
        app.logger.info(" run update countries [begin]")
        app.logger.info("------------------------------------------------------------")
        app.logger.info("... TBD")
        app.logger.info(" run update countries [done]")
        app.logger.info("------------------------------------------------------------")
        return self

    def run_admin_database_import(self):
        app.logger.info(" run update countries [begin]")
        app.logger.info("------------------------------------------------------------")
        app.logger.info("... TBD")
        app.logger.info(" run update countries [done]")
        app.logger.info("------------------------------------------------------------")
        return self

    def run_admin_database_drop(self):
        app.logger.info(" run update countries [begin]")
        app.logger.info("------------------------------------------------------------")
        self.__database.drop_all()
        self.__database.create_all()
        app.logger.info("")
        app.logger.info(" run update countries [done]")
        app.logger.info("------------------------------------------------------------")
        return self
