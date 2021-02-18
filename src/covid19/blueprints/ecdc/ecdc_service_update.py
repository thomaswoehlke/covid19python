from database import db, app
from covid19.blueprints.ecdc.ecdc_service_config import EcdcServiceConfig
from covid19.blueprints.ecdc.ecdc_model_import import EcdcImport
from covid19.blueprints.ecdc.ecdc_model import EcdcDateReported, EcdcContinent, EcdcCountry, EcdcData


class EcdcServiceUpdate:
    def __init__(self, database, config: EcdcServiceConfig):
        app.logger.debug("------------------------------------------------------------")
        app.logger.debug(" ECDC Service Update [init]")
        app.logger.debug("------------------------------------------------------------")
        self.__database = database
        self.cfg = config
        app.logger.debug("------------------------------------------------------------")
        app.logger.debug(" ECDC Service Update [ready] ")

    def __update_date_reported(self):
        app.logger.info(" __update_date_reported [begin]")
        app.logger.info("------------------------------------------------------------")
        EcdcData.remove_all()
        EcdcDateReported.remove_all()
        result_date_rep = EcdcImport.get_date_rep()
        k = 0
        for result_item in result_date_rep:
            k += 1
            my_date_rep = result_item[0]
            oo = EcdcDateReported.find_by_date_reported(my_date_rep)
            if oo is None:
                o = EcdcDateReported.create_new_object_factory(
                    my_date_rep=my_date_rep
                )
                db.session.add(o)
                db.session.commit()
            app.logger.info("| " + my_date_rep + " | " + str(k) + " rows ")
        app.logger.info(" __update_date_reported [done]")
        app.logger.info("------------------------------------------------------------")
        return self

    def __update_continent(self):
        app.logger.info(" __update_continent [begin]")
        app.logger.info("------------------------------------------------------------")
        EcdcData.remove_all()
        EcdcCountry.remove_all()
        EcdcContinent.remove_all()
        result_continent = EcdcImport.get_continent()
        for result_item in result_continent:
            my_continent_exp = result_item[0]
            o = EcdcContinent(
                region=my_continent_exp
            )
            app.logger.info("| " + str(o) + " |")
            db.session.add(o)
        db.session.commit()
        app.logger.info(" __update_continent [done]")
        app.logger.info("------------------------------------------------------------")
        return self

    def __update_country(self):
        app.logger.info(" __update_country [begin]")
        app.logger.info("------------------------------------------------------------")
        EcdcData.remove_all()
        EcdcCountry.remove_all()
        all_continents = EcdcContinent.get_all()
        for my_continent in all_continents:
            result_countries_of_continent = EcdcImport.get_countries_of_continent(my_continent)
            for c in result_countries_of_continent:
                o = EcdcCountry(
                    countries_and_territories=c[0],
                    pop_data_2019=c[1],
                    geo_id=c[2],
                    country_territory_code=c[3],
                    continent=my_continent)
                app.logger.info("| " + str(o) + " |")
                db.session.add(o)
            db.session.commit()
        app.logger.info(" __update_country [done]")
        app.logger.info("------------------------------------------------------------")
        return self

    def __get_continent_from_import(self, ecdc_import: EcdcImport):
        my_a = ecdc_import.continent_exp
        ecdc_continent = EcdcContinent.find_by_region(my_a)
        if ecdc_continent in None:
            ecdc_continent = EcdcContinent(region=my_a)
            db.session.add(ecdc_continent)
            db.session.commit()
        ecdc_continent = EcdcContinent.find_by_region(my_a)
        return ecdc_continent

    def __get_country_from_import(self, ecdc_import: EcdcImport):
        my_countries_and_territories = ecdc_import.countries_and_territories
        my_geo_id = ecdc_import.geo_id
        my_country_territory_code = ecdc_import.country_territory_code
        my_pop_data_2019 = ecdc_import.pop_data_2019
        ecdc_country = EcdcCountry.find_by(
            countries_and_territories=my_countries_and_territories,
            geo_id=my_geo_id,
            country_territory_code=my_country_territory_code
        )
        if ecdc_country is None:
            my_continent = self.__get_continent_from_import(ecdc_import)
            app.logger.info(my_continent.id + " "+my_continent.region)
            o = EcdcCountry(
                countries_and_territories=my_countries_and_territories,
                pop_data_2019=my_pop_data_2019,
                geo_id=my_geo_id,
                country_territory_code=my_country_territory_code,
                continent=my_continent
            )
            db.session.add(o)
            db.session.commit()
            ecdc_country = EcdcCountry.get_by(
                countries_and_territories=my_countries_and_territories,
                geo_id=my_geo_id,
                country_territory_code=my_country_territory_code
            )
        return ecdc_country

    def __get_date_reported_from_import(self):
        dict_date_reported_from_import = {}
        result_date_str_from_ecdc_import = EcdcImport.get_date_rep()
        for item_date_str_from_ecdc_import in result_date_str_from_ecdc_import:
            item_date_str_from_ecdc_import_str = str(item_date_str_from_ecdc_import[0])
            app.logger.info(item_date_str_from_ecdc_import_str)
            my_date_reported_search_str = EcdcDateReported.get_date_format_from_ecdc_import_format(
                date_reported_ecdc_import_fomat=item_date_str_from_ecdc_import_str
            )
            app.logger.info(my_date_reported_search_str)
            my_ecdc_date_reported_obj = EcdcDateReported.find_by_date_reported(
                p_date_reported=my_date_reported_search_str
            )
            if my_ecdc_date_reported_obj is None:
                my_ecdc_date_reported_obj = EcdcDateReported.create_new_object_factory(
                    my_date_rep=item_date_str_from_ecdc_import_str
                )
                db.session.add(my_ecdc_date_reported_obj)
                db.session.commit()
            my_ecdc_date_reported_obj = EcdcDateReported.get_by_date_reported(
                p_date_reported=my_date_reported_search_str
            )
            dict_date_reported_from_import[item_date_str_from_ecdc_import_str] = my_ecdc_date_reported_obj
        return dict_date_reported_from_import

    def __update_data_initial(self):
        app.logger.info(" __update_data_initial [begin]")
        app.logger.info("------------------------------------------------------------")
        EcdcData.remove_all()
        i = 0
        dict_date_reported_from_import = self.__get_date_reported_from_import()
        for my_date_reported in dict_date_reported_from_import.keys():
            my_ecdc_date_reported = dict_date_reported_from_import[my_date_reported]
            for item_ecdc_data_import in EcdcImport.find_by_date_reported(my_date_reported):
                my_ecdc_country = self.__get_country_from_import(item_ecdc_data_import)
                my_deaths = int(item_ecdc_data_import.deaths)
                my_cases = int(item_ecdc_data_import.cases)
                if item_ecdc_data_import.cumulative_number_for_14_days_of_covid19_cases_per_100000 == '':
                    my_cumulative_number = 0.0
                else:
                    my_cumulative_number = \
                        float(item_ecdc_data_import.cumulative_number_for_14_days_of_covid19_cases_per_100000)
                o = EcdcData(
                    ecdc_country=my_ecdc_country,
                    ecdc_date_reported=my_ecdc_date_reported,
                    deaths=my_deaths,
                    cases=my_cases,
                    cumulative_number_for_14_days_of_covid19_cases_per_100000=my_cumulative_number
                )
                db.session.add(o)
                i += 1
                if i % 500 == 0:
                    app.logger.info(" update EDCD initial ... " + str(i) + " rows")
                    db.session.commit()
        db.session.commit()
        app.logger.info(" update ECDC initial ... " + str(i) + " rows total")
        app.logger.info(" __update_data_initial [done]")
        app.logger.info("------------------------------------------------------------")
        return self

    def update_dimension_tables_only(self):
        EcdcData.remove_all()
        EcdcCountry.remove_all()
        EcdcContinent.remove_all()
        self.__update_date_reported()
        self.__update_continent()
        self.__update_country()
        return self

    def update_fact_table_incremental_only(self):
        self.__update_data_initial()
        return self

    def update_fact_table_initial_only(self):
        self.__update_data_initial()
        return self

    def update_star_schema_incremental(self):
        EcdcData.remove_all()
        EcdcCountry.remove_all()
        EcdcContinent.remove_all()
        EcdcDateReported.remove_all()
        self.__update_date_reported()
        self.__update_continent()
        self.__update_country()
        self.__update_data_initial()
        return self

    def update_star_schema_initial(self):
        EcdcData.remove_all()
        EcdcCountry.remove_all()
        EcdcContinent.remove_all()
        EcdcDateReported.remove_all()
        self.__update_date_reported()
        self.__update_continent()
        self.__update_country()
        self.__update_data_initial()
        return self
