from database import db, app

from covid19.blueprints.rki_vaccination.rki_vaccination_service_config import RkiVaccinationServiceConfig
from covid19.blueprints.rki_vaccination.rki_vaccination_model_import import RkiVaccinationImport
from covid19.blueprints.rki_vaccination.rki_vaccination_model import VaccinationDateReported, VaccinationData


class RkiVaccinationServiceUpdate:
    def __init__(self, database):
        app.logger.debug("------------------------------------------------------------")
        app.logger.debug(" Europe Service Update [init]")
        app.logger.debug("------------------------------------------------------------")
        self.__database = database
        self.cfg = RkiVaccinationServiceConfig()
        app.logger.debug("------------------------------------------------------------")
        app.logger.debug(" Europe Service Update [ready] ")

    def __update_date_reported(self):
        app.logger.info(" __update_date_reported [begin]")
        app.logger.info("------------------------------------------------------------")
        VaccinationData.remove_all()
        VaccinationDateReported.remove_all()
        date_reported_list = RkiVaccinationImport.get_date_reported_as_array()
        i = 0
        for one_date_reported in date_reported_list:
            i += 1
            output = " [ " + str(i) + " ] " + one_date_reported + " added"
            o = VaccinationDateReported.create_new_object_factory(one_date_reported)
            db.session.add(o)
            app.logger.info(output)
        db.session.commit()
        app.logger.info(" __update_date_reported [done]")
        app.logger.info("------------------------------------------------------------")
        return self

    def __update_data_initial(self):
        app.logger.info(" __update_data_initial [begin]")
        app.logger.info("------------------------------------------------------------")
        VaccinationData.remove_all()
        result_date_rep = RkiVaccinationImport.get_date_rep()
        i = 0
        for item_date_rep, in result_date_rep:
            #dt = item_date_rep['date_rep']
            europe_date_reported = VaccinationDateReported.find_by_date_reported(
                i_date_reported=item_date_rep
            )
            if europe_date_reported is None:
                o = VaccinationDateReported.create_new_object_factory(item_date_rep)
                europe_date_reported = o
            result_europe_data_import = RkiVaccinationImport.find_by_datum(europe_date_reported.date_reported)
            for item_europe_data_import in result_europe_data_import:
                o = VaccinationData(
                    date_reported=europe_date_reported,
                    dosen_kumulativ=item_europe_data_import.dosen_kumulativ,
                    dosen_differenz_zum_vortag=item_europe_data_import.dosen_differenz_zum_vortag,
                    dosen_biontech_kumulativ=item_europe_data_import.dosen_biontech_kumulativ,
                    dosen_moderna_kumulativ=item_europe_data_import.dosen_moderna_kumulativ,
                    personen_erst_kumulativ=item_europe_data_import.personen_erst_kumulativ,
                    personen_voll_kumulativ=item_europe_data_import.personen_voll_kumulativ,
                    impf_quote_erst=item_europe_data_import.impf_quote_erst,
                    impf_quote_voll=item_europe_data_import.impf_quote_voll,
                    indikation_alter_dosen=item_europe_data_import.indikation_alter_dosen,
                    indikation_beruf_dosen=item_europe_data_import.indikation_beruf_dosen,
                    indikation_medizinisch_dosen=item_europe_data_import.indikation_medizinisch_dosen,
                    indikation_pflegeheim_dosen=item_europe_data_import.indikation_pflegeheim_dosen,
                    indikation_alter_erst=item_europe_data_import.indikation_alter_erst,
                    indikation_beruf_erst=item_europe_data_import.indikation_beruf_erst,
                    indikation_medizinisch_erst=item_europe_data_import.indikation_medizinisch_erst,
                    indikation_pflegeheim_erst=item_europe_data_import.indikation_pflegeheim_erst,
                    indikation_alter_voll=item_europe_data_import.indikation_alter_voll,
                    indikation_beruf_voll=item_europe_data_import.indikation_beruf_voll,
                    indikation_medizinisch_voll=item_europe_data_import.indikation_medizinisch_voll,
                    indikation_pflegeheim_voll=item_europe_data_import.indikation_pflegeheim_voll
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

    def __update_data_incremental(self):
        app.logger.info(" __update_data_initial [begin]")
        app.logger.info("------------------------------------------------------------")
        result_date_rep = RkiVaccinationImport.get_daterep_missing_in_vaccination_data()
        i = 0
        for item_date_rep in result_date_rep:
            europe_date_reported = VaccinationDateReported.create_new_object_factory(item_date_rep)
            result_europe_data_import = RkiVaccinationImport.find_by_datum(europe_date_reported)
            for item_europe_data_import in result_europe_data_import:
                o = VaccinationData(
                    date_reported=europe_date_reported,
                    dosen_kumulativ=item_europe_data_import.dosen_kumulativ,
                    dosen_differenz_zum_vortag=item_europe_data_import.dosen_differenz_zum_vortag,
                    dosen_biontech_kumulativ=item_europe_data_import.dosen_biontech_kumulativ,
                    dosen_moderna_kumulativ=item_europe_data_import.dosen_moderna_kumulativ,
                    personen_erst_kumulativ=item_europe_data_import.personen_erst_kumulativ,
                    personen_voll_kumulativ=item_europe_data_import.personen_voll_kumulativ,
                    impf_quote_erst=item_europe_data_import.impf_quote_erst,
                    impf_quote_voll=item_europe_data_import.impf_quote_voll,
                    indikation_alter_dosen=item_europe_data_import.indikation_alter_dosen,
                    indikation_beruf_dosen=item_europe_data_import.indikation_beruf_dosen,
                    indikation_medizinisch_dosen=item_europe_data_import.indikation_medizinisch_dosen,
                    indikation_pflegeheim_dosen=item_europe_data_import.indikation_pflegeheim_dosen,
                    indikation_alter_erst=item_europe_data_import.indikation_alter_erst,
                    indikation_beruf_erst=item_europe_data_import.indikation_beruf_erst,
                    indikation_medizinisch_erst=item_europe_data_import.indikation_medizinisch_erst,
                    indikation_pflegeheim_erst=item_europe_data_import.indikation_pflegeheim_erst,
                    indikation_alter_voll=item_europe_data_import.indikation_alter_voll,
                    indikation_beruf_voll=item_europe_data_import.indikation_beruf_voll,
                    indikation_medizinisch_voll=item_europe_data_import.indikation_medizinisch_voll,
                    indikation_pflegeheim_voll=item_europe_data_import.indikation_pflegeheim_voll
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

    # TODO: remove DEPRECATED
    #def __update_data_short_DEPRECATED(self):
    #    app.logger.info(" __update_data_initial [begin]")
    #    app.logger.info("------------------------------------------------------------")
    #    app.logger.info(" ... ")
    #    app.logger.info(" __update_data_initial [done]")
    #    app.logger.info("------------------------------------------------------------")
    #    return self

    # TODO: remove DEPRECATED
    #def update_db_initial_DEPRECATED(self):
    #    app.logger.info(" update_db_initial [begin]")
    #    app.logger.info("------------------------------------------------------------")
    #    VaccinationDateReported.remove_all()
    #    VaccinationData.remove_all()
    #    self.__update_date_reported()
    #    self.__update_data_initial()
    #    app.logger.info(" update_db_initial [done]")
    #    app.logger.info("------------------------------------------------------------")
    #    return self

    # TODO: remove DEPRECATED
    #def update_db_short_DEPRECATED(self):
    #    app.logger.info(" update_db_short [begin]")
    #    app.logger.info("------------------------------------------------------------")
    #    VaccinationDateReported.remove_all()
    #    VaccinationData.remove_all()
    #    self.__update_date_reported()
    #    self.__update_data_short_DEPRECATED()
    #    app.logger.info(" update_db_short [done]")
    #    app.logger.info("------------------------------------------------------------")
    #    return self

    # Delegate
    def __update_dimension_table_date_reported(self):
        self.__update_date_reported()
        return self

    def update_dimension_tables_only(self):
        self.__update_dimension_table_date_reported()
        return self

    def update_fact_table_incremental_only(self):
        self.__update_data_incremental()
        return self

    def update_fact_table_initial_only(self):
        self.__update_data_initial()
        return self

    def update_star_schema_incremental(self):
        self.__update_dimension_table_date_reported()
        self.__update_data_incremental()
        return self

    def update_star_schema_initial(self):
        VaccinationData.remove_all()
        VaccinationDateReported.remove_all()
        self.__update_dimension_table_date_reported()
        self.__update_data_initial()
        return self
