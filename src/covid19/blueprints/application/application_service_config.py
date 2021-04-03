import os
from datetime import date
from covid19.blueprints.ecdc.ecdc_model_import import EcdcImport
from covid19.blueprints.who.who_model_import import WhoImport
from covid19.blueprints.rki_vaccination.rki_vaccination_model_import import RkiVaccinationImport
from covid19.blueprints.owid.owid_model_import import OwidImport
from covid19.blueprints.rki_bundeslaender.rki_bundeslaender_model_import import RkiBundeslaenderImport
from covid19.blueprints.rki_landkreise.rki_landkreise_model_import import RkiLandkreiseImport


class ApplicationServiceConfig:
    def __init__(self, slug: str, category: str, sub_category: str, tablename: str, cvsfile_name: str, url_src: str):
        self.limit_nr = 20
        self.data_path = ".." + os.sep + "data"
        self.slug = slug,
        self.category = category
        self.sub_category = sub_category
        self.tablename = tablename
        self.cvsfile_name = cvsfile_name
        self.url_src = url_src
        self.cvsfile_path = self.data_path + os.sep + self.cvsfile_name
        self.msg_job = "download FILE: "+self.cvsfile_name+" from "+self.url_src
        self.msg_ok = "downloaded FILE: " + self.cvsfile_path + " from " + self.url_src
        self.msg_error = "Error while downloading: " + self.cvsfile_path + " from " + self.url_src

    @classmethod
    def create_config_for_who(cls):
        return ApplicationServiceConfig(
            slug='who',
            category='WHO',
            sub_category='Cases and Deaths',
            tablename=WhoImport.__tablename__,
            cvsfile_name="WHO-COVID-19-global-data.csv",
            url_src="https://covid19.who.int/WHO-COVID-19-global-data.csv",
        )

    @classmethod
    def create_config_for_rki_vaccination(cls):
        return ApplicationServiceConfig(
            slug='rki_vaccination',
            category='RKI',
            sub_category='Vaccination',
            tablename=RkiVaccinationImport.__tablename__,
            cvsfile_name="germany_vaccinations_timeseries_v2.tsv",
            url_src="https://impfdashboard.de/static/data/germany_vaccinations_timeseries_v2.tsv",
        )

    @classmethod
    def create_config_for_owid(cls):
        return ApplicationServiceConfig(
            slug='owid',
            category='OWID',
            sub_category='Our World in Data',
            tablename=OwidImport.__tablename__,
            cvsfile_name="owid-covid-data.csv",
            url_src='"https://covid.ourworldindata.org/data/owid-covid-data.csv"',
        )

    @classmethod
    def create_config_for_ecdc(cls):
        return ApplicationServiceConfig(
            slug='ecdc',
            category='ECDC',
            sub_category='European Centre for Disease Prevention and Control',
            tablename=EcdcImport.__tablename__,
            cvsfile_name="ecdc_europa_data.csv",
            url_src="https://opendata.ecdc.europa.eu/covid19/casedistribution/csv/",
        )

    @classmethod
    def create_config_for_rki_bundeslaender(cls):
        return ApplicationServiceConfig(
            slug='rki_bundeslaender',
            category='RKI',
            sub_category='Bundeslaender',
            tablename=RkiBundeslaenderImport.__tablename__,
            cvsfile_name="RKI_COVID19__" + date.today().isoformat() + "__bundeslaender.csv",
            url_src="https://opendata.arcgis.com/datasets/ef4b445a53c1406892257fe63129a8ea_0.csv",
        )

    @classmethod
    def create_config_for_rki_landkreise(cls):
        return ApplicationServiceConfig(
            slug='rki_landkreise',
            category='RKI',
            sub_category='Landkreise',
            tablename=RkiLandkreiseImport.__tablename__,
            cvsfile_name="RKI_COVID19__" + date.today().isoformat() + "__landkreise.csv",
            url_src="https://opendata.arcgis.com/datasets/917fc37a709542548cc3be077a786c17_0.csv",
        )
