from datetime import date
import os


class RkiLandkreiseServiceConfig:
    def __init__(self):
        self.limit_nr = 20
        self.data_path = ".."+os.sep+".."+os.sep+"data"
        self.url_src = "https://opendata.arcgis.com/datasets/917fc37a709542548cc3be077a786c17_0.csv"
        self.cvsfile_name = "RKI_COVID19__" + date.today().isoformat() + "__landkreise.csv"
        self.cvsfile_path = self.data_path + os.sep + self.cvsfile_name
