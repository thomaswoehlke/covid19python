import csv
import psycopg2
from database import db, app
from covid19.blueprints.owid.owid_model_import import OwidImport
from covid19.blueprints.owid.owid_service_config import OwidServiceConfig


class OwidServiceImport:
    def __init__(self, database, config: OwidServiceConfig):
        app.logger.debug("------------------------------------------------------------")
        app.logger.debug(" OWID Service Import [init]")
        app.logger.debug("------------------------------------------------------------")
        self.__database = database
        self.cfg = config
        app.logger.debug("------------------------------------------------------------")
        app.logger.debug(" OWID Service Import [ready]")

    def import_file(self):
        app.logger.info(" import OWID [begin]")
        app.logger.info("------------------------------------------------------------")
        app.logger.info(" import into TABLE: "+self.cfg.tablename+" from "+self.cfg.cvsfile_path)
        app.logger.info("------------------------------------------------------------")
        row = None
        try:
            OwidImport.remove_all()
            with open(self.cfg.cvsfile_path, newline='\n') as csv_file:
                file_reader = csv.DictReader(csv_file, delimiter=',', quotechar='"')
                k = 0
                for row in file_reader:
                    o = OwidImport(
                        iso_code=row['iso_code'],
                        continent=row['continent'],
                        location=row['location'],
                        date=row['date'],
                        total_cases=row['total_cases'],
                        new_cases=row['new_cases'],
                        new_cases_smoothed=row['new_cases_smoothed'],
                        total_deaths=row['total_deaths'],
                        new_deaths=row['new_deaths'],
                        new_deaths_smoothed=row['new_deaths_smoothed'],
                        total_cases_per_million=row['total_cases_per_million'],
                        new_cases_per_million=row['new_cases_per_million'],
                        new_cases_smoothed_per_million=row['new_cases_smoothed_per_million'],
                        total_deaths_per_million=row['total_deaths_per_million'],
                        new_deaths_per_million=row['new_deaths_per_million'],
                        new_deaths_smoothed_per_million=row['new_deaths_smoothed_per_million'],
                        reproduction_rate=row['reproduction_rate'],
                        icu_patients=row['icu_patients'],
                        icu_patients_per_million=row['icu_patients_per_million'],
                        hosp_patients=row['hosp_patients'],
                        hosp_patients_per_million=row['hosp_patients_per_million'],
                        weekly_icu_admissions=row['weekly_icu_admissions'],
                        weekly_icu_admissions_per_million=row['weekly_icu_admissions_per_million'],
                        weekly_hosp_admissions=row['weekly_hosp_admissions'],
                        weekly_hosp_admissions_per_million=row['weekly_hosp_admissions_per_million'],
                        new_tests=row['new_tests'],
                        total_tests=row['total_tests'],
                        total_tests_per_thousand=row['total_tests_per_thousand'],
                        new_tests_per_thousand=row['new_tests_per_thousand'],
                        new_tests_smoothed=row['new_tests_smoothed'],
                        new_tests_smoothed_per_thousand=row['new_tests_smoothed_per_thousand'],
                        positive_rate=row['positive_rate'],
                        tests_per_case=row['tests_per_case'],
                        tests_units=row['tests_units'],
                        total_vaccinations=row['total_vaccinations'],
                        people_vaccinated=row['people_vaccinated'],
                        people_fully_vaccinated=row['people_fully_vaccinated'],
                        new_vaccinations=row['new_vaccinations'],
                        new_vaccinations_smoothed=row['new_vaccinations_smoothed'],
                        total_vaccinations_per_hundred=row['total_vaccinations_per_hundred'],
                        people_vaccinated_per_hundred=row['people_vaccinated_per_hundred'],
                        people_fully_vaccinated_per_hundred=row['people_fully_vaccinated_per_hundred'],
                        new_vaccinations_smoothed_per_million=row['new_vaccinations_smoothed_per_million'],
                        stringency_index=row['stringency_index'],
                        population=row['population'],
                        population_density=row['population_density'],
                        median_age=row['median_age'],
                        aged_65_older=row['aged_65_older'],
                        aged_70_older=row['aged_70_older'],
                        gdp_per_capita=row['gdp_per_capita'],
                        extreme_poverty=row['extreme_poverty'],
                        cardiovasc_death_rate=row['cardiovasc_death_rate'],
                        diabetes_prevalence=row['diabetes_prevalence'],
                        female_smokers=row['female_smokers'],
                        male_smokers=row['male_smokers'],
                        handwashing_facilities=row['handwashing_facilities'],
                        hospital_beds_per_thousand=row['hospital_beds_per_thousand'],
                        life_expectancy=row['life_expectancy'],
                        human_development_index=row['human_development_index'],
                    )
                    db.session.add(o)
                    k += 1
                    if (k % 2000) == 0:
                        db.session.commit()
                        app.logger.info(" import OWID  ... " + str(k) + " rows")
            db.session.commit()
            app.logger.info(" import OWID  ... " + str(k) + " rows total")
        except KeyError as error:
            app.logger.warning("WARN: import OWID [begin]")
            app.logger.warning(":::"+str(error)+":::")
            for item_key, item_value in row.items():
                app.logger.warning(item_key+" : "+item_value)
            app.logger.warning("WARN: import OWID [end]")
        except (Exception, psycopg2.DatabaseError) as error:
            app.logger.warning("WARN: import OWID [begin]")
            app.logger.warning(error)
            app.logger.warning("WARN: import OWID [end]")
        finally:
            app.logger.info("")
            app.logger.info("------------------------------------------------------------")
            app.logger.info(" imported into TABLE: "+self.cfg.tablename+" from "+self.cfg.cvsfile_path)
            app.logger.info("------------------------------------------------------------")
            app.logger.info(" import OWID [done]")
        return self
