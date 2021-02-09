from database import db, app
from covid19.blueprints.who.who_model import WhoRegion, WhoDateReported, WhoCountry, WhoData
from covid19.blueprints.who.who_model_import import WhoImport
from covid19.blueprints.who.who_service_download import WhoServiceConfig


class WhoServiceUpdate:
    def __init__(self, database):
        app.logger.debug("------------------------------------------------------------")
        app.logger.debug(" WHO Service Update [init]")
        app.logger.debug("------------------------------------------------------------")
        self.__database = database
        self.cfg = WhoServiceConfig()
        app.logger.debug("------------------------------------------------------------")
        app.logger.debug(" WHO Service Update [ready]")

    def __update_who_date_reported(self):
        app.logger.info(" __update_who_date_reported [begin]")
        app.logger.info("------------------------------------------------------------")
        i = 0
        for i_date_reported, in WhoImport.get_dates_reported():
            i += 1
            output = " [ " + str(i) + " ] " + i_date_reported
            c = WhoDateReported.find_by_date_reported(i_date_reported)
            if c is None:
                o = WhoDateReported.create_new_object_factory(my_date_rep=i_date_reported)
                db.session.add(o)
                db.session.commit()
                output += " added"
            else:
                output += " NOT added "+str(c.id)
        app.logger.info("")
        app.logger.info(" __update_who_date_reported [done]")
        app.logger.info("------------------------------------------------------------")
        return self

    def __update_who_region(self):
        app.logger.info(" __update_who_region [begin]")
        app.logger.info("------------------------------------------------------------")
        i = 0
        for i_who_region, in WhoImport.get_regions():
            i += 1
            output = " [ " + str(i) + " ] " + i_who_region
            c = WhoRegion.find_by_region(i_who_region)
            if c is None:
                o = WhoRegion(region=i_who_region)
                db.session.add(o)
                db.session.commit()
                output += " added"
            else:
                output += " NOT added ( " + str(c.id) + " ) "
        app.logger.info("")
        app.logger.info(" __update_who_region [done]")
        app.logger.info("------------------------------------------------------------")
        return self

    def __update_who_country(self):
        app.logger.info(" __update_who_country [begin]")
        app.logger.info("------------------------------------------------------------")
        result = WhoImport.countries()
        i = 0
        for result_item in result:
            i += 1
            i_country_code = result_item.country_code
            i_country = result_item.country
            i_who_region = result_item.who_region
            output = " [ " + str(i) + " ] " + i_country_code + " | " + i_country + " | " + i_who_region + " | "
            my_region = WhoRegion.find_by_region(i_who_region)
            my_country = WhoCountry.find_by_country_code_and_country_and_who_region_id(
                i_country_code, i_country, my_region
            )
            if my_country is None:
                o = WhoCountry(
                    country=i_country,
                    country_code=i_country_code,
                    region=my_region)
                db.session.add(o)
                db.session.commit()
                output2 = " added "
            else:
                output2 = " NOT added ( " + str(my_country.id) + " ) "
            output += i_country_code + output2
            app.logger.info(output)
        db.session.commit()
        app.logger.info("")
        app.logger.info(" __update_who_country [done]")
        app.logger.info("------------------------------------------------------------")
        return self

    def __update_fact_table_incremental(self):
        app.logger.info(" __update_fact_tables_incremental [begin]")
        app.logger.info("------------------------------------------------------------")
        new_dates_reported_from_import = WhoImport.get_new_dates_as_array()
        i = 0
        for my_date_reported in new_dates_reported_from_import:
            my_date = WhoDateReported.find_by_date_reported(my_date_reported)
            if my_date is None:
                myday = WhoDateReported.create_new_object_factory(my_date_reported)
                db.session.add(myday)
                db.session.commit()
            my_date = WhoDateReported.get_by_date_reported(my_date_reported)
            k = 0
            for result_item in WhoImport.get_for_one_day(my_date_reported):
                if result_item.country_code == "":
                    my_country = WhoCountry.get_by_country(result_item.country)
                else:
                    my_country = WhoCountry.get_by_country_code(result_item.country_code)
                o = WhoData(
                    cases_new=int(result_item.new_cases),
                    cases_cumulative=int(result_item.cumulative_cases),
                    deaths_new=int(result_item.new_deaths),
                    deaths_cumulative=int(result_item.cumulative_deaths),
                    date_reported=my_date,
                    country=my_country
                )
                db.session.add(o)
                i += 1
                k += 1
                if i % 500 == 0:
                    app.logger.debug(" update WHO incremental ... "+str(i)+" rows")
            db.session.commit()
            app.logger.info(" update WHO incremental ... " + str(i) + " rows [" + str(my_date) + "] (" + str(k) + ")")
        app.logger.info(" update WHO incremental :  "+str(i)+" rows total")
        app.logger.info(" __update_fact_tables_incremental [done]")
        app.logger.info("------------------------------------------------------------")
        return self

    def __update_fact_table_initial(self):
        app.logger.info(" __update_fact_table_initial [begin]")
        app.logger.info("------------------------------------------------------------")
        WhoData.remove_all()
        new_dates_reported_from_import = WhoImport.get_new_dates_as_array()
        i = 0
        for my_date_reported in new_dates_reported_from_import:
            my_date = WhoDateReported.find_by_date_reported(my_date_reported)
            if my_date is None:
                myday = WhoDateReported.create_new_object_factory(my_date_reported)
                db.session.add(myday)
                my_date = myday
            for result_item in WhoImport.get_for_one_day(my_date_reported):
                my_country = WhoCountry.find_by_country_code(result_item.country_code)
                o = WhoData(
                    cases_new=int(result_item.new_cases),
                    cases_cumulative=int(result_item.cumulative_cases),
                    deaths_new=int(result_item.new_deaths),
                    deaths_cumulative=int(result_item.cumulative_deaths),
                    date_reported=my_date,
                    country=my_country
                )
                db.session.add(o)
                result_item.row_imported = True
                db.session.add(result_item)
                i += 1
                if i % 500 == 0:
                    app.logger.info(" update WHO initial ... "+str(i)+" rows")
                    db.session.commit()
            db.session.commit()
        app.logger.info(" update WHO initial :  "+str(i)+" total rows")
        app.logger.info(" __update_fact_table_initial [done]")
        app.logger.info("------------------------------------------------------------")
        return self

    def __update_dimension_tables(self):
        self.__update_who_date_reported()
        self.__update_who_region()
        self.__update_who_country()
        return self

    def update_dimension_tables_only(self):
        app.logger.info(" update_dimension_tables_only [begin]")
        app.logger.info("------------------------------------------------------------")
        self.__update_dimension_tables()
        app.logger.info(" update_dimension_tables_only [done]")
        app.logger.info("------------------------------------------------------------")
        return self

    def update_fact_table_incremental_only(self):
        app.logger.info(" update_fact_tables_incremental_only [begin]")
        app.logger.info("------------------------------------------------------------")
        self.__update_fact_table_incremental()
        app.logger.info(" update_fact_tables_incremental_only [done]")
        app.logger.info("------------------------------------------------------------")
        return self

    def update_fact_table_initial_only(self):
        app.logger.info(" update_fact_tables_initial_only [begin]")
        app.logger.info("------------------------------------------------------------")
        self.__update_fact_table_initial()
        app.logger.info(" update_fact_tables_initial_only [done]")
        app.logger.info("------------------------------------------------------------")
        return self

    def update_star_schema_incremental(self):
        app.logger.info(" update_star_schema_incremental [begin]")
        app.logger.info("------------------------------------------------------------")
        self.__update_dimension_tables()
        self.__update_fact_table_incremental()
        app.logger.info(" update_star_schema_incremental [done]")
        app.logger.info("------------------------------------------------------------")
        return self

    def update_star_schema_initial(self):
        app.logger.info(" update_star_schema_initial [begin]")
        app.logger.info("------------------------------------------------------------")
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
