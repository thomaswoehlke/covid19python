from database import db, app
from covid19.blueprints.ecdc.ecdc_service_config import EcdcServiceConfig
from covid19.blueprints.ecdc.ecdc_model_import import EcdcImport
from covid19.blueprints.ecdc.ecdc_model import EcdcDateReported, EcdcContinent, EcdcCountry, EcdcData


# TODO: #117 refactor EcdcServiceUpdate to new method scheme introduced 07.02.2021
class EcdcServiceUpdate:
    def __init__(self, database):
        app.logger.debug("------------------------------------------------------------")
        app.logger.debug(" ECDC Service Update [init]")
        app.logger.debug("------------------------------------------------------------")
        self.__database = database
        self.cfg = EcdcServiceConfig()
        app.logger.debug("------------------------------------------------------------")
        app.logger.debug(" ECDC Service Update [ready] ")

    def __update_date_reported(self):
        app.logger.info(" __update_date_reported [begin]")
        app.logger.info("------------------------------------------------------------")
        result_date_rep = EcdcImport.get_date_rep()
        k = 0
        for result_item in result_date_rep:
            k += 1
            #my_date_rep = result_item['date_rep']
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
        result_continent = EcdcImport.get_continent()
        for result_item in result_continent:
            #my_continent_exp = result_item['continent_exp']
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
        all_continents = EcdcContinent.get_all()
        for my_continent in all_continents:
            result_countries_of_continent = EcdcImport.get_countries_of_continent(my_continent)
            for c in result_countries_of_continent:
                o = EcdcCountry(
                    countries_and_territories=c['countries_and_territories'],
                    pop_data_2019=c['pop_data_2019'],
                    geo_id=c['geo_id'],
                    country_territory_code=c['country_territory_code'],
                    continent=my_continent)
                app.logger.info("| " + str(o) + " |")
                db.session.add(o)
            db.session.commit()
        app.logger.info(" __update_country [done]")
        app.logger.info("------------------------------------------------------------")
        return self

    def __update_data_initial(self):
        app.logger.info(" __update_data_initial [begin]")
        app.logger.info("------------------------------------------------------------")
        result_date_rep = EcdcImport.get_date_rep()
        i = 0
        for item_date_rep in result_date_rep:
            ecdc_date_reported = EcdcDateReported.find_by_date_reported(
                i_date_reported=item_date_rep['date_rep']
            )
            if ecdc_date_reported is None:
                o = EcdcDateReported.create_new_object_factory(item_date_rep['date_rep'])
                ecdc_date_reported = o
            result_ecdc_data_import = EcdcImport.find_by_date_reported(ecdc_date_reported)
            for item_ecdc_data_import in result_ecdc_data_import:
                my_a = item_ecdc_data_import.countries_and_territories
                my_b = item_ecdc_data_import.geo_id
                my_c = item_ecdc_data_import.country_territory_code
                ecdc_country = EcdcCountry.find_by(
                    countries_and_territories=my_a,
                    geo_id=my_b,
                    country_territory_code=my_c
                )
                my_d = int(item_ecdc_data_import.deaths_weekly)
                my_e = int(item_ecdc_data_import.cases_weekly)
                if item_ecdc_data_import.notification_rate_per_100000_population_14days == '':
                    my_f = 0.0
                else:
                    my_f = float(item_ecdc_data_import.notification_rate_per_100000_population_14days)
                o = EcdcData(
                    ecdc_country=ecdc_country,
                    ecdc_date_reported=ecdc_date_reported,
                    deaths_weekly=my_d,
                    cases_weekly=my_e,
                    notification_rate_per_100000_population_14days=my_f
                )
                db.session.add(o)
                item_ecdc_data_import.row_imported = True
                db.session.add(item_ecdc_data_import)
                i += 1
                if i % 500 == 0:
                    app.logger.info(" update EDCD initial ... " + str(i) + " rows")
                    db.session.commit()
        db.session.commit()
        app.logger.info(" update ECDC initial ... " + str(i) + " rows total")
        app.logger.info(" __update_data_initial [done]")
        app.logger.info("------------------------------------------------------------")
        return self

    # TODO: #117 refactor EcdcServiceUpdate to new method scheme introduced 07.02.2021
    def __update_data_short(self):
        app.logger.info(" __update_data_initial [begin]")
        app.logger.info("------------------------------------------------------------")
        app.logger.info(" ... ")
        app.logger.info(" __update_data_initial [done]")
        app.logger.info("------------------------------------------------------------")
        return self

    # TODO: #117 refactor EcdcServiceUpdate to new method scheme introduced 07.02.2021
    def update_db_initial(self):
        app.logger.info(" update_db_initial [begin]")
        app.logger.info("------------------------------------------------------------")
        EcdcData.remove_all()
        EcdcCountry.remove_all()
        EcdcContinent.remove_all()
        EcdcDateReported.remove_all()
        self.__update_date_reported()
        self.__update_continent()
        self.__update_country()
        self.__update_data_initial()
        app.logger.info(" update_db_initial [done]")
        app.logger.info("------------------------------------------------------------")
        return self

    # TODO: #117 refactor EcdcServiceUpdate to new method scheme introduced 07.02.2021
    def update_db_short(self):
        app.logger.info(" update_db_short [begin]")
        app.logger.info("------------------------------------------------------------")
        EcdcData.remove_all()
        EcdcCountry.remove_all()
        EcdcContinent.remove_all()
        EcdcDateReported.remove_all()
        self.__update_date_reported()
        self.__update_continent()
        self.__update_country()
        self.__update_data_short()
        app.logger.info(" update_db_short [done]")
        app.logger.info("------------------------------------------------------------")
        return self

    def update_dimension_tables_only(self):
        # TODO: #118 implement EcdcServiceUpdate.update_dimension_tables_only
        # TODO: #117 refactor EcdcServiceUpdate to new method scheme introduced 07.02.2021
        EcdcData.remove_all()
        EcdcCountry.remove_all()
        EcdcContinent.remove_all()
        self.__update_date_reported()
        self.__update_continent()
        self.__update_country()
        return self

    def update_fact_table_incremental_only(self):
        # TODO: #119 implement EcdcServiceUpdate.update_fact_table_incremental_only
        # TODO: #117 refactor EcdcServiceUpdate to new method scheme introduced 07.02.2021
        EcdcDateReported.remove_all()
        self.__update_data_short()
        return self

    def update_fact_table_initial_only(self):
        # TODO: #120 implement EcdcServiceUpdate.update_fact_table_initial_only
        # TODO: #117 refactor EcdcServiceUpdate to new method scheme introduced 07.02.2021
        EcdcDateReported.remove_all()
        self.__update_data_initial()
        return self

    def update_star_schema_incremental(self):
        # TODO: #121 implement EcdcServiceUpdate.update_star_schema_incremental
        # TODO: #117 refactor EcdcServiceUpdate to new method scheme introduced 07.02.2021
        EcdcData.remove_all()
        EcdcCountry.remove_all()
        EcdcContinent.remove_all()
        EcdcDateReported.remove_all()
        self.__update_date_reported()
        self.__update_continent()
        self.__update_country()
        self.__update_data_short()
        return self

    def update_star_schema_initial(self):
        # TODO: #122 implement EcdcServiceUpdate.update_star_schema_initial
        # TODO: #117 refactor EcdcServiceUpdate to new method scheme introduced 07.02.2021
        EcdcData.remove_all()
        EcdcCountry.remove_all()
        EcdcContinent.remove_all()
        EcdcDateReported.remove_all()
        self.__update_date_reported()
        self.__update_continent()
        self.__update_country()
        self.__update_data_initial()
        return self
