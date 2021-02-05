from database import app


class CommonService:
    def __init__(self, database):
        app.logger.debug("------------------------------------------------------------")
        app.logger.debug(" Common Service [init]")
        app.logger.debug("------------------------------------------------------------")
        self.__database = database
        self.limit_nr = 20
        app.logger.debug("------------------------------------------------------------")
        app.logger.info(" Common Service [ready]")
