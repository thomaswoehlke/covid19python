from datetime import date
import os


class RkiLandkreiseServiceConfig:
    def __init__(self):
        self.limit_nr = 20
        datum_heute = date.today().isoformat()
        self.cvsfile_name = "RKI_COVID19__" + datum_heute + "__landkreise.csv"
        self.url_src = "https://opendata.arcgis.com/datasets/917fc37a709542548cc3be077a786c17_0.csv"
        self.data_path = ".." + os.sep + ".." + os.sep + "data" + os.sep
        self.src_cvsfile_path = self.data_path + self.cvsfile_name
