import os
from database import app, db
from org.woehlke.covid19.common.common_model import CommonDatum

common_service = None


class CommonService:
    def __init__(self, database):
        app.logger.info("------------------------------------------------------------")
        app.logger.info(" Common Service [init]")
        app.logger.info("------------------------------------------------------------")
        self.__database = database
        self.limit_nr = 20
        app.logger.info("------------------------------------------------------------")
        app.logger.info(" Common Service [ready]")
