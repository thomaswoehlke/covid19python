from database import app

#TODO: deprecated
class ApplicationService:
    def __init__(self, database):
        app.logger.debug("------------------------------------------------------------")
        app.logger.debug(" Common Service [init]")
        app.logger.debug("------------------------------------------------------------")
        self.__database = database
        app.logger.debug("------------------------------------------------------------")
        app.logger.info(" Common Service [ready]")
