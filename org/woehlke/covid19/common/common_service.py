from database import app


class CommonService:
    def __init__(self, database):
        app.logger.info("------------------------------------------------------------")
        app.logger.info(" Common Service [init]")
        app.logger.info("------------------------------------------------------------")
        self.__database = database
        self.limit_nr = 20
        app.logger.info("------------------------------------------------------------")
        app.logger.info(" Common Service [ready]")
