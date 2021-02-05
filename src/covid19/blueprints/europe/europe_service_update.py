from database import db, app
from covid19.blueprints.europe.europe_service_config import EuropeServiceDownloadConfig
from covid19.blueprints.europe.europe_model_import import EuropeDataImportTable
from covid19.blueprints.europe.europe_model import EuropeDateReported, EuropeContinent, EuropeCountry, EuropeData


class EuropeServiceUpdate:
    def __init__(self, database):
        app.logger.debug("------------------------------------------------------------")
        app.logger.debug(" Europe Service Update [init]")
        app.logger.debug("------------------------------------------------------------")
        self.__database = database
        self.cfg = EuropeServiceDownloadConfig()
        app.logger.debug("------------------------------------------------------------")
        app.logger.debug(" Europe Service Update [ready] ")

    def __update_date_reported(self):
        app.logger.info(" __update_date_reported [begin]")
        app.logger.info("------------------------------------------------------------")
        result_date_rep = EuropeDataImportTable.get_date_rep()
        k = 0
        for result_item in result_date_rep:
            k += 1
            my_date_rep = result_item['date_rep']
            my_year_week = result_item['year_week']
            o = EuropeDateReported.create_new_object_factory(
                my_date_rep=my_date_rep
            )
            db.session.add(o)
            app.logger.info("| " + my_date_rep + " | " + my_year_week + " | " + str(k) + " rows ")
        db.session.commit()
        app.logger.info(" __update_date_reported [done]")
        app.logger.info("------------------------------------------------------------")
        return self

    def __update_continent(self):
        app.logger.info(" __update_continent [begin]")
        app.logger.info("------------------------------------------------------------")
        result_continent = EuropeDataImportTable.get_continent()
        for result_item in result_continent:
            my_continent_exp = result_item['continent_exp']
            o = EuropeContinent(
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
        all_continents = EuropeContinent.get_all()
        for my_continent in all_continents:
            result_countries_of_continent = EuropeDataImportTable.get_countries_of_continent(my_continent)
            for c in result_countries_of_continent:
                o = EuropeCountry(
                    countries_and_territories=c['countries_and_territories'],
                    geo_id=c['geo_id'],
                    country_territory_code=c['country_territory_code'],
                    pop_data_2019=c['pop_data_2019'],
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
        result_date_rep = EuropeDataImportTable.get_date_rep()
        i = 0
        for item_date_rep in result_date_rep:
            europe_date_reported = EuropeDateReported.find_by_date_reported(
                i_date_reported=item_date_rep['date_rep']
            )
            if europe_date_reported is None:
                o = EuropeDateReported.create_new_object_factory(item_date_rep['date_rep'])
                europe_date_reported = o
            result_europe_data_import = EuropeDataImportTable.find_by_date_reported(europe_date_reported)
            for item_europe_data_import in result_europe_data_import:
                my_a = item_europe_data_import.countries_and_territories
                my_b = item_europe_data_import.geo_id
                my_c = item_europe_data_import.country_territory_code
                europe_country = EuropeCountry.find_by(
                    countries_and_territories=my_a,
                    geo_id=my_b,
                    country_territory_code=my_c
                )
                my_d = int(item_europe_data_import.deaths_weekly)
                my_e = int(item_europe_data_import.cases_weekly)
                if item_europe_data_import.notification_rate_per_100000_population_14days == '':
                    my_f = 0.0
                else:
                    my_f = float(item_europe_data_import.notification_rate_per_100000_population_14days)
                o = EuropeData(
                    europe_country=europe_country,
                    europe_date_reported=europe_date_reported,
                    deaths_weekly=my_d,
                    cases_weekly=my_e,
                    notification_rate_per_100000_population_14days=my_f
                )
                db.session.add(o)
                item_europe_data_import.row_imported = True
                db.session.add(item_europe_data_import)
                i += 1
                if i % 500 == 0:
                    app.logger.info(" update Europa initial ... " + str(i) + " rows")
                    db.session.commit()
        db.session.commit()
        app.logger.info(" update Europa initial ... " + str(i) + " rows total")
        app.logger.info(" __update_data_initial [done]")
        app.logger.info("------------------------------------------------------------")
        return self

    #TODO
    def __update_data_short(self):
        app.logger.info(" __update_data_initial [begin]")
        app.logger.info("------------------------------------------------------------")
        app.logger.info(" ... ")
        app.logger.info(" __update_data_initial [done]")
        app.logger.info("------------------------------------------------------------")
        return self

    def update_db_initial(self):
        app.logger.info(" update_db_initial [begin]")
        app.logger.info("------------------------------------------------------------")
        EuropeData.remove_all()
        EuropeCountry.remove_all()
        EuropeContinent.remove_all()
        EuropeDateReported.remove_all()
        self.__update_date_reported()
        self.__update_continent()
        self.__update_country()
        self.__update_data_initial()
        app.logger.info(" update_db_initial [done]")
        app.logger.info("------------------------------------------------------------")
        return self

    def update_db_short(self):
        app.logger.info(" update_db_short [begin]")
        app.logger.info("------------------------------------------------------------")
        EuropeData.remove_all()
        EuropeCountry.remove_all()
        EuropeContinent.remove_all()
        EuropeDateReported.remove_all()
        self.__update_date_reported()
        self.__update_continent()
        self.__update_country()
        self.__update_data_short()
        app.logger.info(" update_db_short [done]")
        app.logger.info("------------------------------------------------------------")
        return self

