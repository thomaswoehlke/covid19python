import os

from covid19.blueprints.owid.owid_model_import import OwidImport


class OwidServiceConfig:
    def __init__(self):
        self.limit_nr = 20
        self.data_path = ".." + os.sep + ".." + os.sep + "data"
        self.category = 'OWID'
        self.sub_category = 'Our World in Data'
        self.tablename = OwidImport.__tablename__
        self.cvsfile_name = "owid-covid-data.csv"
        self.url_src = "https://covid.ourworldindata.org/data/owid-covid-data.csv"
        self.cvsfile_path = self.data_path + os.sep + self.cvsfile_name
        self.msg_ok = "downloaded: " + self.cfg.cvsfile_path + " from " + self.cfg.url_src
        self.msg_error = "while downloading: " + self.cfg.cvsfile_path + " from " + self.cfg.url_src
