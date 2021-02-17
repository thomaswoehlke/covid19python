import os

from covid19.blueprints.rki_vaccination.rki_vaccination_model_import import RkiVaccinationImport


class RkiVaccinationServiceConfig:
    def __init__(self):
        self.limit_nr = 20
        self.category = 'RKI'
        self.sub_category = 'Vaccination'
        self.tablename = RkiVaccinationImport.__tablename__
        self.url_src = "https://impfdashboard.de/static/data/germany_vaccinations_timeseries_v2.tsv"
        self.cvsfile_name = "germany_vaccinations_timeseries_v2.tsv"
        self.data_path = ".."+os.sep+".."+os.sep+"data"
        self.cvsfile_path = self.data_path + os.sep + self.cvsfile_name
