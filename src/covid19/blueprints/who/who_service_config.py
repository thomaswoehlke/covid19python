import os

from covid19.blueprints.who.who_model_import import WhoImport


class WhoServiceConfig:
    def __init__(self):
        self.limit_nr = 20
        self.data_path = ".." + os.sep + ".." + os.sep + "data"
        self.category = 'WHO'
        self.sub_category = 'Cases and Deaths'
        self.tablename = WhoImport.__tablename__
        self.cvsfile_name = "WHO-COVID-19-global-data.csv"
        self.url_src = "https://covid19.who.int/" + self.cvsfile_name
        self.cvsfile_path = self.data_path + os.sep + self.cvsfile_name
