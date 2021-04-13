from flask import flash

from database import app


class UserService:
    def __init__(self, database):
        app.logger.debug("------------------------------------------------------------")
        app.logger.debug(" User Service [init]")
        app.logger.debug("------------------------------------------------------------")
        self.__database = database
        app.logger.debug("------------------------------------------------------------")
        app.logger.info(" User Service [ready]")

