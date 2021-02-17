import os


class WhoServiceConfig:
    def __init__(self):
        self.limit_nr = 20
        self.url_src = "https://covid19.who.int/" + self.cvsfile_name
        self.cvsfile_name = "WHO-COVID-19-global-data.csv"
        self.data_path = ".."+os.sep+".."+os.sep+"data"
        self.cvsfile_path = self.data_path + os.sep + self.cvsfile_name
