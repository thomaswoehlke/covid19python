from datetime import date
import os

from covid19.blueprints.rki_landkreise.rki_landkreise_model_import import RkiLandkreiseImport


class RkiLandkreiseServiceConfig:
    def __init__(self):
        self.limit_nr = 20
        self.data_path = ".." + os.sep + ".." + os.sep + "data"
        self.category = 'RKI'
        self.sub_category = 'Landkreise'
        self.tablename = RkiLandkreiseImport.__tablename__
        self.url_src = "https://opendata.arcgis.com/datasets/917fc37a709542548cc3be077a786c17_0.csv"
        self.cvsfile_name = "RKI_COVID19__" + date.today().isoformat() + "__landkreise.csv"
        self.cvsfile_path = self.data_path + os.sep + self.cvsfile_name
        self.msg_ok = "downloaded: " + self.cfg.cvsfile_path + " from " + self.cfg.url_src
        self.msg_error = "while downloading: " + self.cfg.cvsfile_path + " from " + self.cfg.url_src
