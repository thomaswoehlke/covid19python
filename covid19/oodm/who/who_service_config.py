import os


class WhoServiceDownloadConfig:
    def __init__(self):
        self.limit_nr = 20
        self.data_path = ".."+os.sep+"data"
        self.cvsfile_name = "WHO-COVID-19-global-data.csv"
        self.url_src_data = "https://covid19.who.int/" + self.cvsfile_name
