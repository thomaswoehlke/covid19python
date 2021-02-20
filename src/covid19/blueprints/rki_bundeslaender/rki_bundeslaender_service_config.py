from datetime import date
import os
from covid19.blueprints.rki_bundeslaender.rki_bundeslaender_model_import import RkiBundeslaenderImport


class RkiBundeslaenderServiceConfig:
    def __init__(self):
        self.limit_nr = 20
        self.data_path = ".." + os.sep + ".." + os.sep + "data"
        self.category = 'RKI'
        self.sub_category = 'Bundeslaender'
        self.tablename = RkiBundeslaenderImport.__tablename__
        self.url_src = "https://opendata.arcgis.com/datasets/ef4b445a53c1406892257fe63129a8ea_0.csv"
        self.cvsfile_name = "RKI_COVID19__" + date.today().isoformat() + "__bundeslaender.csv"
        self.cvsfile_path = self.data_path + os.sep + self.cvsfile_name
        self.msg_ok = "downloaded: " + self.cfg.cvsfile_path + " from " + self.cfg.url_src
        self.msg_error = "while downloading: " + self.cfg.cvsfile_path + " from " + self.cfg.url_src
