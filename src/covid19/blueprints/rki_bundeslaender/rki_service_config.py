from datetime import date
import os


class RkiBundeslaenderServiceConfig:
    def __init__(self):
        self.limit_nr = 20
        datum_heute = date.today().isoformat()
        self.cvsfile_name = "RKI_COVID19__" + datum_heute + "__bundeslaender.csv"
        self.url_src = "https://opendata.arcgis.com/datasets/ef4b445a53c1406892257fe63129a8ea_0.csv"
        self.data_path = ".." + os.sep + ".." + os.sep + "data" + os.sep
        self.src_cvsfile_path = self.data_path + self.cvsfile_name
