from database import db, app
from covid19.blueprints.application.application_service_config import ApplicationServiceConfig
from covid19.blueprints.owid.owid_model import OwidDateReported, OwidData, OwidContinent, OwidCountry
from covid19.blueprints.owid.owid_model_import import OwidImport


class OwidServiceUpdate:
    def __init__(self, database, config: ApplicationServiceConfig):
        app.logger.debug("------------------------------------------------------------")
        app.logger.debug(" OWID Service Update [init]")
        app.logger.debug("------------------------------------------------------------")
        self.__database = database
        self.cfg = config
        app.logger.debug("------------------------------------------------------------")
        app.logger.debug(" OWID Service Update [ready]")

    def __update_date_reported(self):
        app.logger.info(" __update_date_reported [begin]")
        app.logger.info("------------------------------------------------------------")
        i = 0
        for i_date_reported, in OwidImport.get_dates():
            i += 1
            output = " [ " + str(i) + " ] " + i_date_reported
            c = OwidDateReported.find_by_date_reported(i_date_reported)
            if c is None:
                o = OwidDateReported.create_new_object_factory(my_date_rep=i_date_reported)
                db.session.add(o)
                db.session.commit()
                output += " added"
            else:
                output += " NOT added "+str(c.id)
            app.logger.info(output)
        app.logger.info("")
        app.logger.info(" __update_date_reported [done]")
        app.logger.info("------------------------------------------------------------")
        return self

    def __update_fact_table_incremental(self):
        app.logger.info(" __update_fact_tables_incremental [begin]")
        app.logger.info("------------------------------------------------------------")
        new_dates_reported_from_import = OwidImport.get_new_dates_reported_as_array()
        i = 0
        for my_date_reported in new_dates_reported_from_import:
            my_OwidDateReported = OwidDateReported.find_by_date_reported(my_date_reported)
            if my_OwidDateReported is None:
                myday = OwidDateReported.create_new_object_factory(my_date_reported)
                db.session.add(myday)
                db.session.commit()
            my_OwidDateReported = OwidDateReported.get_by_date_reported(my_date_reported)
            k = 0
            for oi in OwidImport.get_for_one_day(my_date_reported):
                my_OwidContinent = OwidContinent.find_by_region(i_region=oi.continent)
                if my_OwidContinent is None:
                    my_OwidContinent = OwidContinent(region=oi.continent)
                    db.session.add(my_OwidContinent)
                    db.session.commit()
                my_OwidContinent = OwidContinent.find_by_region(i_region=oi.continent)
                my_OwidCountry = OwidCountry.find_by_iso_code_and_location(iso_code=oi.iso_code, location=oi.location)
                if my_OwidCountry is None:
                    my_OwidCountry = OwidCountry(
                        continent=my_OwidContinent,
                        population=oi.population,
                        population_density=oi.population_density,
                        median_age=oi.median_age,
                        aged_65_older=oi.aged_65_older,
                        aged_70_older=oi.aged_70_older,
                        gdp_per_capita=oi.gdp_per_capita,
                        extreme_poverty=oi.extreme_poverty,
                        cardiovasc_death_rate=oi.cardiovasc_death_rate,
                        diabetes_prevalence=oi.diabetes_prevalence,
                        female_smokers=oi.female_smokers,
                        male_smokers=oi.male_smokers,
                        handwashing_facilities=oi.handwashing_facilities,
                        hospital_beds_per_thousand=oi.hospital_beds_per_thousand,
                        life_expectancy=oi.life_expectancy,
                        human_development_index=oi.human_development_index,
                    )
                    db.session.add(my_OwidCountry)
                    db.session.commit()
                my_OwidCountry = OwidCountry.find_by_iso_code_and_location(iso_code=oi.iso_code, location=oi.location)
                o = OwidData(
                    date_reported=my_OwidDateReported,
                    country=my_OwidCountry,
                    total_cases=oi.total_cases,
                    new_cases=oi.new_cases,
                    new_cases_smoothed=oi.new_cases_smoothed,
                    total_deaths=oi.total_deaths,
                    new_deaths=oi.new_deaths,
                    new_deaths_smoothed=oi.new_deaths_smoothed,
                    total_cases_per_million=oi.total_cases_per_million,
                    new_cases_per_million=oi.new_cases_per_million,
                    new_cases_smoothed_per_million=oi.new_cases_smoothed_per_million,
                    total_deaths_per_million=oi.total_deaths_per_million,
                    new_deaths_per_million=oi.new_deaths_per_million,
                    new_deaths_smoothed_per_million=oi.new_deaths_smoothed_per_million,
                    reproduction_rate=oi.reproduction_rate,
                    icu_patients=oi.icu_patients,
                    icu_patients_per_million=oi.icu_patients_per_million,
                    hosp_patients=oi.hosp_patients,
                    hosp_patients_per_million=oi.hosp_patients_per_million,
                    weekly_icu_admissions=oi.weekly_icu_admissions,
                    weekly_icu_admissions_per_million=oi.weekly_icu_admissions_per_million,
                    weekly_hosp_admissions=oi.weekly_hosp_admissions,
                    weekly_hosp_admissions_per_million=oi.weekly_hosp_admissions_per_million,
                    new_tests=oi.new_tests,
                    total_tests=oi.total_tests,
                    total_tests_per_thousand=oi.total_tests_per_thousand,
                    new_tests_per_thousand=oi.new_tests_per_thousand,
                    new_tests_smoothed=oi.new_tests_smoothed,
                    new_tests_smoothed_per_thousand=oi.new_tests_smoothed_per_thousand,
                    positive_rate=oi.positive_rate,
                    tests_per_case=oi.tests_per_case,
                    tests_units=oi.tests_units,
                    total_vaccinations=oi.total_vaccinations,
                    people_vaccinated=oi.people_vaccinated,
                    people_fully_vaccinated=oi.people_fully_vaccinated,
                    new_vaccinations=oi.new_vaccinations,
                    new_vaccinations_smoothed=oi.new_vaccinations_smoothed,
                    total_vaccinations_per_hundred=oi.total_vaccinations_per_hundred,
                    people_vaccinated_per_hundred=oi.people_vaccinated_per_hundred,
                    people_fully_vaccinated_per_hundred=oi.people_fully_vaccinated_per_hundred,
                    new_vaccinations_smoothed_per_million=oi.new_vaccinations_smoothed_per_million,
                    stringency_index=oi.stringency_index,
                )
                db.session.add(o)
                i += 1
                k += 1
                if i % 1000 == 0:
                    app.logger.info(" update OWID incremental ... "+str(i)+" rows")
            db.session.commit()
            app.logger.info(" update OWID incremental ... " + str(i) + " rows [" + str(my_OwidDateReported) + "] (" + str(k) + ")")
        app.logger.info(" update OWID incremental :  "+str(i)+" rows total")
        app.logger.info(" __update_fact_tables_incremental [done]")
        app.logger.info("------------------------------------------------------------")
        return self

    def __update_fact_table_initial(self):
        app.logger.info(" __update_fact_table_initial [begin]")
        app.logger.info("------------------------------------------------------------")
        OwidData.remove_all()
        new_dates_reported_from_import = OwidImport.get_dates_reported_as_array()
        i = 0
        for my_date_reported in new_dates_reported_from_import:
            my_OwidDateReported = OwidDateReported.find_by_date_reported(my_date_reported)
            if my_OwidDateReported is None:
                myday = OwidDateReported.create_new_object_factory(my_date_reported)
                db.session.add(myday)
                db.session.commit()
            my_OwidDateReported = OwidDateReported.get_by_date_reported(my_date_reported)
            for oi in OwidImport.get_for_one_day(my_date_reported):
                my_OwidContinent = OwidContinent.find_by_region(i_region=oi.continent)
                if my_OwidContinent is None:
                    my_OwidContinent = OwidContinent(region=oi.continent)
                    db.session.add(my_OwidContinent)
                    db.session.commit()
                my_OwidContinent = OwidContinent.find_by_region(i_region=oi.continent)
                my_OwidCountry = OwidCountry.find_by_iso_code_and_location(
                    iso_code=oi.iso_code,
                    location=oi.location
                )
                if my_OwidCountry is None:
                    my_OwidCountry = OwidCountry(
                        continent=my_OwidContinent,
                        iso_code=oi.iso_code,
                        location=oi.location,
                        population=oi.population,
                        population_density=oi.population_density,
                        median_age=oi.median_age,
                        aged_65_older=oi.aged_65_older,
                        aged_70_older=oi.aged_70_older,
                        gdp_per_capita=oi.gdp_per_capita,
                        extreme_poverty=oi.extreme_poverty,
                        cardiovasc_death_rate=oi.cardiovasc_death_rate,
                        diabetes_prevalence=oi.diabetes_prevalence,
                        female_smokers=oi.female_smokers,
                        male_smokers=oi.male_smokers,
                        handwashing_facilities=oi.handwashing_facilities,
                        hospital_beds_per_thousand=oi.hospital_beds_per_thousand,
                        life_expectancy=oi.life_expectancy,
                        human_development_index=oi.human_development_index,
                    )
                    db.session.add(my_OwidCountry)
                    db.session.commit()
                my_OwidCountry = OwidCountry.find_by_iso_code_and_location(
                    iso_code=oi.iso_code,
                    location=oi.location
                )
                o = OwidData(
                    date_reported=my_OwidDateReported,
                    country=my_OwidCountry,
                    total_cases=oi.total_cases,
                    new_cases=oi.new_cases,
                    new_cases_smoothed=oi.new_cases_smoothed,
                    total_deaths=oi.total_deaths,
                    new_deaths=oi.new_deaths,
                    new_deaths_smoothed=oi.new_deaths_smoothed,
                    total_cases_per_million=oi.total_cases_per_million,
                    new_cases_per_million=oi.new_cases_per_million,
                    new_cases_smoothed_per_million=oi.new_cases_smoothed_per_million,
                    total_deaths_per_million=oi.total_deaths_per_million,
                    new_deaths_per_million=oi.new_deaths_per_million,
                    new_deaths_smoothed_per_million=oi.new_deaths_smoothed_per_million,
                    reproduction_rate=oi.reproduction_rate,
                    icu_patients=oi.icu_patients,
                    icu_patients_per_million=oi.icu_patients_per_million,
                    hosp_patients=oi.hosp_patients,
                    hosp_patients_per_million=oi.hosp_patients_per_million,
                    weekly_icu_admissions=oi.weekly_icu_admissions,
                    weekly_icu_admissions_per_million=oi.weekly_icu_admissions_per_million,
                    weekly_hosp_admissions=oi.weekly_hosp_admissions,
                    weekly_hosp_admissions_per_million=oi.weekly_hosp_admissions_per_million,
                    new_tests=oi.new_tests,
                    total_tests=oi.total_tests,
                    total_tests_per_thousand=oi.total_tests_per_thousand,
                    new_tests_per_thousand=oi.new_tests_per_thousand,
                    new_tests_smoothed=oi.new_tests_smoothed,
                    new_tests_smoothed_per_thousand=oi.new_tests_smoothed_per_thousand,
                    positive_rate=oi.positive_rate,
                    tests_per_case=oi.tests_per_case,
                    tests_units=oi.tests_units,
                    total_vaccinations=oi.total_vaccinations,
                    people_vaccinated=oi.people_vaccinated,
                    people_fully_vaccinated=oi.people_fully_vaccinated,
                    new_vaccinations=oi.new_vaccinations,
                    new_vaccinations_smoothed=oi.new_vaccinations_smoothed,
                    total_vaccinations_per_hundred=oi.total_vaccinations_per_hundred,
                    people_vaccinated_per_hundred=oi.people_vaccinated_per_hundred,
                    people_fully_vaccinated_per_hundred=oi.people_fully_vaccinated_per_hundred,
                    new_vaccinations_smoothed_per_million=oi.new_vaccinations_smoothed_per_million,
                    stringency_index=oi.stringency_index,
                )
                db.session.add(o)
                i += 1
                if i % 1000 == 0:
                    app.logger.info(" update OWID initial ... "+str(i)+" rows")
                    db.session.commit()
            db.session.commit()
        app.logger.info(" update OWID initial :  "+str(i)+" total rows")
        app.logger.info(" __update_fact_table_initial [done]")
        app.logger.info("------------------------------------------------------------")
        return self

    def __update_dimension_tables(self):
        self.__update_date_reported()
        return self

    def update_dimension_tables_only(self):
        app.logger.info(" update_dimension_tables_only [begin]")
        app.logger.info("------------------------------------------------------------")
        # TODO
        self.__update_dimension_tables()
        app.logger.info(" update_dimension_tables_only [done]")
        app.logger.info("------------------------------------------------------------")
        return self

    def update_fact_table_incremental_only(self):
        app.logger.info(" update_fact_tables_incremental_only [begin]")
        app.logger.info("------------------------------------------------------------")
        # TODO
        self.__update_fact_table_incremental()
        app.logger.info(" update_fact_tables_incremental_only [done]")
        app.logger.info("------------------------------------------------------------")
        return self

    def update_fact_table_initial_only(self):
        app.logger.info(" update_fact_tables_initial_only [begin]")
        app.logger.info("------------------------------------------------------------")
        # TODO
        self.__update_fact_table_initial()
        app.logger.info(" update_fact_tables_initial_only [done]")
        app.logger.info("------------------------------------------------------------")
        return self

    def update_star_schema_incremental(self):
        app.logger.info(" update_star_schema_incremental [begin]")
        app.logger.info("------------------------------------------------------------")
        # TODO
        self.__update_dimension_tables()
        self.__update_fact_table_incremental()
        app.logger.info(" update_star_schema_incremental [done]")
        app.logger.info("------------------------------------------------------------")
        return self

    def update_star_schema_initial(self):
        app.logger.info(" update_star_schema_initial [begin]")
        app.logger.info("------------------------------------------------------------")
        # TODO
        self.__update_dimension_tables()
        self.__update_fact_table_initial()
        app.logger.info(" update_star_schema_initial [done]")
        app.logger.info("------------------------------------------------------------")
        return self

    #def update_dimension_tables_only(self):
    #def update_fact_table_incremental_only(self):
    #def update_fact_table_initial_only(self):
    #def update_star_schema_incremental(self):
    #def update_star_schema_initial(self):
