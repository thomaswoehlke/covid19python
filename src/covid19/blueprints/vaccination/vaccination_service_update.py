from database import db, app

from covid19.blueprints.vaccination.vaccination_service_config import VaccinationServiceDownloadConfig
from covid19.blueprints.vaccination.vaccination_model_import import VaccinationGermanyTimeline
from covid19.blueprints.vaccination.vaccination_model import VaccinationDateReported, VaccinationGermanyTimelineAAA


# TODO: refactor VaccinationsServiceUpdate to new method scheme introduced 07.02.2021
class VaccinationsServiceUpdate:
    def __init__(self, database):
        app.logger.debug("------------------------------------------------------------")
        app.logger.debug(" Europe Service Update [init]")
        app.logger.debug("------------------------------------------------------------")
        self.__database = database
        self.cfg = VaccinationServiceDownloadConfig()
        app.logger.debug("------------------------------------------------------------")
        app.logger.debug(" Europe Service Update [ready] ")

    # TODO: refactor VaccinationsServiceUpdate to new method scheme introduced 07.02.2021
    def __update_date_reported(self):
        app.logger.info(" __update_date_reported [begin]")
        app.logger.info("------------------------------------------------------------")
        result_date_rep = VaccinationGermanyTimeline.get_date_rep()
        k = 0
        for result_item in result_date_rep:
            k += 1
            my_date_rep = result_item['date_rep']
            my_year_week = result_item['year_week']
            o = VaccinationGermanyTimelineAAA.create_new_object_factory(
                my_date_rep=my_date_rep
            )
            db.session.add(o)
            app.logger.info("| " + my_date_rep + " | " + my_year_week + " | " + str(k) + " rows ")
        db.session.commit()
        app.logger.info(" __update_date_reported [done]")
        app.logger.info("------------------------------------------------------------")
        return self

    # TODO: refactor VaccinationsServiceUpdate to new method scheme introduced 07.02.2021
    def __update_data_initial(self):
        app.logger.info(" __update_data_initial [begin]")
        app.logger.info("------------------------------------------------------------")
        result_date_rep = VaccinationGermanyTimeline.get_date_rep()
        i = 0
        for item_date_rep in result_date_rep:
            europe_date_reported = VaccinationDateReported.find_by_date_reported(
                i_date_reported=item_date_rep['date_rep']
            )
            if europe_date_reported is None:
                o = VaccinationDateReported.create_new_object_factory(item_date_rep['date_rep'])
                europe_date_reported = o
            result_europe_data_import = VaccinationGermanyTimeline.find_by_date_reported(europe_date_reported)
            for item_europe_data_import in result_europe_data_import:
                #my_d = int(item_europe_data_import.deaths_weekly)
                #my_e = int(item_europe_data_import.cases_weekly)
                #if item_europe_data_import.notification_rate_per_100000_population_14days == '':
                #    my_f = 0.0
                #else:
                #    my_f = float(item_europe_data_import.notification_rate_per_100000_population_14days)
                o = VaccinationGermanyTimelineAAA(
                    #europe_country=europe_country,
                    #europe_date_reported=europe_date_reported,
                    #deaths_weekly=my_d,
                    #cases_weekly=my_e,
                    #notification_rate_per_100000_population_14days=my_f
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

    # TODO: refactor VaccinationsServiceUpdate to new method scheme introduced 07.02.2021
    def __update_data_short(self):
        app.logger.info(" __update_data_initial [begin]")
        app.logger.info("------------------------------------------------------------")
        app.logger.info(" ... ")
        app.logger.info(" __update_data_initial [done]")
        app.logger.info("------------------------------------------------------------")
        return self

    # TODO: refactor VaccinationsServiceUpdate to new method scheme introduced 07.02.2021
    def update_db_initial(self):
        app.logger.info(" update_db_initial [begin]")
        app.logger.info("------------------------------------------------------------")
        VaccinationDateReported.remove_all()
        VaccinationGermanyTimelineAAA.remove_all()
        self.__update_date_reported()
        self.__update_data_initial()
        app.logger.info(" update_db_initial [done]")
        app.logger.info("------------------------------------------------------------")
        return self

    # TODO: refactor VaccinationsServiceUpdate to new method scheme introduced 07.02.2021
    def update_db_short(self):
        app.logger.info(" update_db_short [begin]")
        app.logger.info("------------------------------------------------------------")
        VaccinationDateReported.remove_all()
        VaccinationGermanyTimelineAAA.remove_all()
        self.__update_date_reported()
        self.__update_data_short()
        app.logger.info(" update_db_short [done]")
        app.logger.info("------------------------------------------------------------")
        return self

    def update_dimension_tables_only(self):
        # TODO: implement VaccinationsServiceUpdate.update_dimension_tables_only
        # TODO: refactor VaccinationsServiceUpdate to new method scheme introduced 07.02.2021
        return self

    def update_fact_table_incremental_only(self):
        # TODO: implement VaccinationsServiceUpdate.update_fact_table_incremental_only
        # TODO: refactor VaccinationsServiceUpdate to new method scheme introduced 07.02.2021
        return self

    def update_fact_table_initial_only(self):
        # TODO: implement VaccinationsServiceUpdate.update_fact_table_initial_only
        # TODO: refactor VaccinationsServiceUpdate to new method scheme introduced 07.02.2021
        return self

    def update_star_schema_incremental(self):
        # TODO: implement VaccinationsServiceUpdate.update_star_schema_incremental
        # TODO: refactor VaccinationsServiceUpdate to new method scheme introduced 07.02.2021
        return self

    def update_star_schema_initial(self):
        # TODO: implement VaccinationsServiceUpdate.update_star_schema_initial
        # TODO: refactor VaccinationsServiceUpdate to new method scheme introduced 07.02.2021
        return self
