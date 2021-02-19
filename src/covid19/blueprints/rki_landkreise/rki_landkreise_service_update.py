from database import db, app

from covid19.blueprints.application.application_model import RkiDateReported
from covid19.blueprints.rki_landkreise.rki_landkreise_model import RkiLandkreise
from covid19.blueprints.rki_landkreise.rki_landkreise_model_import import RkiLandkreiseImport
from covid19.blueprints.rki_landkreise.rki_landkreise_service_config import RkiLandkreiseServiceConfig


class RkiLandkreiseServiceUpdate:
    def __init__(self, database, config: RkiLandkreiseServiceConfig):
        app.logger.debug("------------------------------------------------------------")
        app.logger.debug(" RKI Service Update [init]")
        app.logger.debug("------------------------------------------------------------")
        self.__database = database
        self.cfg = config
        app.logger.debug("------------------------------------------------------------")
        app.logger.debug(" RKI Service Update [ready]")

    def __update_date_reported(self):
        app.logger.info(" update who_date_reported [begin]")
        app.logger.info("------------------------------------------------------------")
        i = 0
        for i_date_reported, in RkiLandkreiseImport.get_dates_reported():
            c = RkiDateReported.find_by_date_reported(i_date_reported)
            if c is None:
                o = RkiDateReported.create_new_object_factory(my_date_rep=i_date_reported)
                db.session.add(o)
                app.logger.info(" update who_date_reported "+i_date_reported+" added NEW")
            if i % 10 == 0:
                app.logger.info(" update who_date_reported "+i_date_reported+" not added")
                db.session.commit()
            i += 1
        db.session.commit()
        app.logger.info("")
        app.logger.info(" update who_date_reported [done]")
        app.logger.info("------------------------------------------------------------")
        return self

    def __update_data_incremental(self):
        app.logger.info(" update RKI short [begin]")
        app.logger.info("------------------------------------------------------------")
        new_dates_reported_from_import = RkiLandkreiseImport.get_new_dates_as_array()
        i = 0
        for my_date_reported in new_dates_reported_from_import:
            my_date = RkiDateReported.find_by_date_reported(my_date_reported)
            for result_item in RkiLandkreiseImport.get_for_one_day(my_date_reported):
                o = RkiLandkreise(
                    cases_new=int(result_item.new_cases),
                    cases_cumulative=int(result_item.cumulative_cases),
                    deaths_new=int(result_item.new_deaths),
                    deaths_cumulative=int(result_item.cumulative_deaths),
                    date_reported=my_date,
                )
                db.session.add(o)
                result_item.row_imported = True
                db.session.add(result_item)
                i += 1
                if i % 500 == 0:
                    app.logger.info(" update WHO short ... "+str(i)+" rows")
                    db.session.commit()
            db.session.commit()
        app.logger.info(" update RKI short :  "+str(i)+" total rows")
        app.logger.info(" update RKI short [done]")
        app.logger.info("------------------------------------------------------------")
        return self

    def __update_data_initial(self):
        app.logger.info(" update RKI initial [begin]")
        app.logger.info("------------------------------------------------------------")
        RkiLandkreise.remove_all()
        new_dates_reported_from_import = RkiLandkreiseImport.get_new_dates_as_array()
        i = 0
        for my_date_reported in new_dates_reported_from_import:
            my_date = RkiDateReported.find_by_date_reported(my_date_reported)
            for result_item in RkiLandkreiseImport.get_for_one_day(my_date_reported):
                o = RkiLandkreise(
                    cases_new=int(result_item.new_cases),
                    cases_cumulative=int(result_item.cumulative_cases),
                    deaths_new=int(result_item.new_deaths),
                    deaths_cumulative=int(result_item.cumulative_deaths),
                    date_reported=my_date
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
        app.logger.info(" update WHO initial [done]")
        app.logger.info("------------------------------------------------------------")
        return self

    # TODO: #153 refactor RkiBundeslaenderServiceUpdate.update_db
    def update_db(self):
        app.logger.info(" update db [begin]")
        app.logger.info("------------------------------------------------------------")
        self.__update_date_reported()
        self.__update_region()
        self.__update_who_country()
        self.__update_who_global_data()
        app.logger.info(" update db [done]")
        app.logger.info("------------------------------------------------------------")
        return self

    # TODO: #154 refactor RkiBundeslaenderServiceUpdate.update_db_short
    def update_db_short(self):
        app.logger.info(" update db short [begin]")
        app.logger.info("------------------------------------------------------------")
        self.__update_date_reported()
        self.__update_region()
        self.__update_who_country()
        self.__update_who_global_data_short()
        app.logger.info(" update db short [done]")
        app.logger.info("------------------------------------------------------------")
        return self

    # TODO: #155 refactor RkiBundeslaenderServiceUpdate.update_db_initial
    def update_db_initial(self):
        app.logger.info(" update db initial [begin]")
        app.logger.info("------------------------------------------------------------")
        self.__update_date_reported()
        self.__update_region()
        self.__update_who_country()
        self.__update_who_global_data_initial()
        app.logger.info(" update db initial [done]")
        app.logger.info("------------------------------------------------------------")
        return self

    def update_dimension_tables_only(self):
        #TODO: #123 split RkiBundeslaenderService into two Services, one for bundeslaender and one for landkreise
        #TODO: #141 implement RkiBundeslaenderServiceUpdate.update_dimension_tables_only
        return self

    def update_fact_table_incremental_only(self):
        #TODO: #123 split RkiBundeslaenderService into two Services, one for bundeslaender and one for landkreise
        #TODO: #142 implement RkiBundeslaenderServiceUpdate.update_fact_table_incremental_only
        return self

    def update_fact_table_initial_only(self):
        #TODO: #123 split RkiBundeslaenderService into two Services, one for bundeslaender and one for landkreise
        #TODO: #143 implement RkiBundeslaenderServiceUpdate.update_fact_table_initial_only
        return self

    def update_star_schema_incremental(self):
        #TODO: #123 split RkiBundeslaenderService into two Services, one for bundeslaender and one for landkreise
        #TODO: #144 implement RkiBundeslaenderServiceUpdate.update_star_schema_incremental
        return self

    def update_star_schema_initial(self):
        #TODO: #123 split RkiBundeslaenderService into two Services, one for bundeslaender and one for landkreise
        #TODO: #145 implement RkiBundeslaenderServiceUpdate.update_star_schema_initial
        return self

