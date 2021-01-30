import os


class VaccinationServiceDownloadConfig:
    def __init__(self):
        self.limit_nr = 20
        self.data_path = ".." + os.sep + "data"
        self.cvsfile_name = "germany_vaccinations_timeseries_v2.tsv"
        self.cvsfile_path = self.data_path + os.sep + self.cvsfile_name
        self.url_src_data = "https://impfdashboard.de/static/data/germany_vaccinations_timeseries_v2.tsv"
        os.makedirs(self.data_path, exist_ok=True)
