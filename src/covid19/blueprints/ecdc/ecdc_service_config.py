import os

from covid19.blueprints.ecdc.ecdc_model_import import EcdcImport


class EcdcServiceConfig:
    def __init__(self):
        self.limit_nr = 20
        self.category = 'ECDC'
        self.sub_category = 'European Centre for Disease Prevention and Control'
        self.data_path = ".."+os.sep+".."+os.sep+"data"
        self.tablename = EcdcImport.__tablename__
        self.cvsfile_name = "ecdc_europa_data.csv"
        self.url_src = "https://opendata.ecdc.europa.eu/covid19/casedistribution/csv/"
        self.cvsfile_path = self.data_path + os.sep + self.cvsfile_name
