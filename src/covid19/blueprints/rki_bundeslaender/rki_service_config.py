from datetime import date
import os


class RkiBundeslaenderServiceConfig:
    def __init__(self):
        self.limit_nr = 20
        self.data_path = ".."+os.sep+".."+os.sep+"data"
        self.url_src = "https://opendata.arcgis.com/datasets/ef4b445a53c1406892257fe63129a8ea_0.csv"
        self.cvsfile_name = "RKI_COVID19__" + date.today().isoformat() + "__bundeslaender.csv"
        self.cvsfile_path = self.data_path + os.sep + self.cvsfile_name
