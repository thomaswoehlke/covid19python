import os
import subprocess

from database import app


class AdminService:
    def __init__(self, database):
        app.logger.debug("------------------------------------------------------------")
        app.logger.debug(" Admin Service [init]")
        app.logger.debug("------------------------------------------------------------")
        self.__database = database
        self.limit_nr = 20
        self.file_path = '..'+os.sep+'data'+os.sep+'db'+os.sep+'covid19data.sql'
        app.logger.debug("------------------------------------------------------------")
        app.logger.info(" Admin Service [ready]")

    def task_database_drop_create(self):
        self.run_admin_database_dump()
        return self

    def run_admin_database_dump(self):
        app.logger.info(" run database dump [begin]")
        app.logger.info("------------------------------------------------------------")
        user = app.config['SQLALCHEMY_POSTGRES_USER']
        url = app.config['SQLALCHEMY_POSTGRES_URL']
        db = app.config['SQLALCHEMY_POSTGRES_DB']
        cmd = 'pg_dump -U '+user+' -h '+url+' '+db\
              +' --clean --if-exists --no-tablespaces '\
              +' --on-conflict-do-nothing --rows-per-insert=1000 --column-inserts '\
              +' --quote-all-identifiers --no-privileges > '\
              + self.file_path
        app.logger.info(" start: "+str(cmd))
        returncode = self.__run_ome_shell_command(cmd)
        app.logger.info(" result: " + str(returncode))
        app.logger.info(" run database dump [done]")
        app.logger.info("------------------------------------------------------------")
        return self

    @classmethod
    def __run_ome_shell_command(cls, cmd):
        args = [cmd]
        app.logger.info(" start: " + str(cmd))
        returncode = 0
        try:
            result = subprocess.run(args, shell=True, check=True, capture_output=True, encoding='UTF-8')
            returncode = result.returncode
        except subprocess.CalledProcessError as error:
            app.logger.warning("WARN: AdminService.__run_ome_shell_command")
            app.logger.warning("cmd    :::" + cmd + ":::")
            app.logger.warning("error  :::" + str(error) + ":::")
            app.logger.warning("WARN: AdminService.__run_ome_shell_command")
        return returncode

    def run_admin_database_dump_reimport(self):
        app.logger.info(" run database dump reimport [begin]")
        app.logger.info("------------------------------------------------------------")
        user = app.config['SQLALCHEMY_POSTGRES_USER']
        url = app.config['SQLALCHEMY_POSTGRES_URL']
        db = app.config['SQLALCHEMY_POSTGRES_DB']
        cmd_list = [
            'psql -U ' + user + ' -h ' + url + ' ' + db + ' < ' + self.file_path
        ]
        for cmd in cmd_list:
            returncode = self.__run_ome_shell_command(cmd)
            msg = '[ returncode: ' + str(returncode) + '] ' + cmd
            app.logger.info(msg)
        app.logger.info(" run database dump reimport [done]")
        app.logger.info("------------------------------------------------------------")
        return self

    def run_admin_database_drop(self):
        app.logger.info(" run database drop and create [begin]")
        app.logger.info("------------------------------------------------------------")
        self.__database.drop_all()
        self.__database.create_all()
        app.logger.info("")
        app.logger.info(" run database drop and create [done]")
        app.logger.info("------------------------------------------------------------")
        return self
