import os


class EcdcServiceConfig:
    def __init__(self):
        self.limit_nr = 20
        self.data_path = ".."+os.sep+".."+os.sep+"data"
        self.cvsfile_name = "ecdc_europa_data.csv"
        self.url_src = "https://opendata.ecdc.europa.eu/covid19/casedistribution/csv/"
        self.cvsfile_path = self.data_path + os.sep + self.cvsfile_name
