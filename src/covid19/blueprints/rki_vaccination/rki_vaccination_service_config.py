import os


class RkiVaccinationServiceConfig:
    def __init__(self):
        self.limit_nr = 20
        self.url_src = "https://impfdashboard.de/static/data/germany_vaccinations_timeseries_v2.tsv"
        self.cvsfile_name = "germany_vaccinations_timeseries_v2.tsv"
        self.data_path = ".."+os.sep+".."+os.sep+"data"
        self.cvsfile_path = self.data_path + os.sep + self.cvsfile_name
