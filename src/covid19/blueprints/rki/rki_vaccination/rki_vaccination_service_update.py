from database import db, app

from covid19.blueprints.application.application_service_config import ApplicationServiceConfig
from covid19.blueprints.rki.rki_vaccination.rki_vaccination_model_import import RkiVaccinationImport
from covid19.blueprints.rki.rki_vaccination.rki_vaccination_model import RkiVaccinationDateReported, RkiVaccinationData


class RkiVaccinationServiceUpdate:
    def __init__(self, database, config: ApplicationServiceConfig):
        app.logger.debug("------------------------------------------------------------")
        app.logger.debug(" Europe Service Update [init]")
        app.logger.debug("------------------------------------------------------------")
        self.__database = database
        self.cfg = config
        app.logger.debug("------------------------------------------------------------")
        app.logger.debug(" Europe Service Update [ready] ")

    def __update_date_reported(self):
        app.logger.info(" __update_date_reported [begin]")
        app.logger.info("------------------------------------------------------------")
        RkiVaccinationData.remove_all()
        RkiVaccinationDateReported.remove_all()
        date_reported_list = RkiVaccinationImport.get_date_reported_as_array()
        i = 0
        for one_date_reported in date_reported_list:
            i += 1
            output = " [ " + str(i) + " ] " + one_date_reported + " added"
            o = RkiVaccinationDateReported.create_new_object_factory(one_date_reported)
            db.session.add(o)
            app.logger.info(output)
        db.session.commit()
        app.logger.info(" __update_date_reported [done]")
        app.logger.info("------------------------------------------------------------")
        return self

    def __update_fact_table_initial(self):
        app.logger.info(" __update_data_initial [begin]")
        app.logger.info("------------------------------------------------------------")
        RkiVaccinationData.remove_all()
        result_date_rep = RkiVaccinationImport.get_date_rep()
        i = 0
        for item_date_rep, in result_date_rep:
            date_reported = RkiVaccinationDateReported.find_by_date_reported(
                p_date_reported=item_date_rep
            )
            if date_reported is None:
                o = RkiVaccinationDateReported.create_new_object_factory(my_date_rep=item_date_rep)
                date_reported = o
            result_data_import = RkiVaccinationImport.find_by_datum(date_reported.date_reported)
            for item_import in result_data_import:
                o = RkiVaccinationData(
                    date_reported=date_reported,
                    dosen_kumulativ=item_import.dosen_kumulativ,
                    dosen_differenz_zum_vortag=item_import.dosen_differenz_zum_vortag,
                    dosen_biontech_kumulativ=item_import.dosen_biontech_kumulativ,
                    dosen_moderna_kumulativ=item_import.dosen_moderna_kumulativ,
                    personen_erst_kumulativ=item_import.personen_erst_kumulativ,
                    personen_voll_kumulativ=item_import.personen_voll_kumulativ,
                    impf_quote_erst=item_import.impf_quote_erst,
                    impf_quote_voll=item_import.impf_quote_voll,
                    indikation_alter_dosen=item_import.indikation_alter_dosen,
                    indikation_beruf_dosen=item_import.indikation_beruf_dosen,
                    indikation_medizinisch_dosen=item_import.indikation_medizinisch_dosen,
                    indikation_pflegeheim_dosen=item_import.indikation_pflegeheim_dosen,
                    indikation_alter_erst=item_import.indikation_alter_erst,
                    indikation_beruf_erst=item_import.indikation_beruf_erst,
                    indikation_medizinisch_erst=item_import.indikation_medizinisch_erst,
                    indikation_pflegeheim_erst=item_import.indikation_pflegeheim_erst,
                    indikation_alter_voll=item_import.indikation_alter_voll,
                    indikation_beruf_voll=item_import.indikation_beruf_voll,
                    indikation_medizinisch_voll=item_import.indikation_medizinisch_voll,
                    indikation_pflegeheim_voll=item_import.indikation_pflegeheim_voll
                )
                db.session.add(o)
                i += 1
                if i % 500 == 0:
                    app.logger.info(" update Vaccination initial ... " + str(i) + " rows")
                    db.session.commit()
        db.session.commit()
        app.logger.info(" update Vaccination initial ... " + str(i) + " rows total")
        app.logger.info(" __update_data_initial [done]")
        app.logger.info("------------------------------------------------------------")
        return self

    def __update_fact_table_incremental(self):
        app.logger.info(" __update_fact_table_incremental Vaccination [begin]")
        app.logger.info("------------------------------------------------------------")
        result_date_rep = RkiVaccinationImport.get_daterep_missing_in_vaccination_data()
        i = 0
        for item_date_rep in result_date_rep:
            date_reported = RkiVaccinationDateReported.find_by_date_reported(item_date_rep)
            #date_reported = RkiVaccinationDateReported.create_new_object_factory(item_date_rep)
            result_data_import = RkiVaccinationImport.find_by_datum(item_date_rep)
            for item_data_import in result_data_import:
                o = RkiVaccinationData(
                    date_reported=date_reported,
                    dosen_kumulativ=item_data_import.dosen_kumulativ,
                    dosen_differenz_zum_vortag=item_data_import.dosen_differenz_zum_vortag,
                    dosen_biontech_kumulativ=item_data_import.dosen_biontech_kumulativ,
                    dosen_moderna_kumulativ=item_data_import.dosen_moderna_kumulativ,
                    personen_erst_kumulativ=item_data_import.personen_erst_kumulativ,
                    personen_voll_kumulativ=item_data_import.personen_voll_kumulativ,
                    impf_quote_erst=item_data_import.impf_quote_erst,
                    impf_quote_voll=item_data_import.impf_quote_voll,
                    indikation_alter_dosen=item_data_import.indikation_alter_dosen,
                    indikation_beruf_dosen=item_data_import.indikation_beruf_dosen,
                    indikation_medizinisch_dosen=item_data_import.indikation_medizinisch_dosen,
                    indikation_pflegeheim_dosen=item_data_import.indikation_pflegeheim_dosen,
                    indikation_alter_erst=item_data_import.indikation_alter_erst,
                    indikation_beruf_erst=item_data_import.indikation_beruf_erst,
                    indikation_medizinisch_erst=item_data_import.indikation_medizinisch_erst,
                    indikation_pflegeheim_erst=item_data_import.indikation_pflegeheim_erst,
                    indikation_alter_voll=item_data_import.indikation_alter_voll,
                    indikation_beruf_voll=item_data_import.indikation_beruf_voll,
                    indikation_medizinisch_voll=item_data_import.indikation_medizinisch_voll,
                    indikation_pflegeheim_voll=item_data_import.indikation_pflegeheim_voll
                )
                db.session.add(o)
                i += 1
                if i % 500 == 0:
                    app.logger.info(" update Vaccination incremental ... " + str(i) + " rows")
                    db.session.commit()
        db.session.commit()
        app.logger.info(" update Vaccination incremental ... " + str(i) + " rows total")
        app.logger.info(" __update_fact_table_incremental Vaccination [done]")
        app.logger.info("------------------------------------------------------------")
        return self

    def __update_dimension_table_date_reported(self):
        self.__update_date_reported()
        return self

    def update_dimension_tables_only(self):
        self.__update_dimension_table_date_reported()
        return self

    def update_fact_table_incremental_only(self):
        self.__update_fact_table_incremental()
        return self

    def update_fact_table_initial_only(self):
        self.__update_fact_table_initial()
        return self

    def update_star_schema_incremental(self):
        self.__update_dimension_table_date_reported()
        self.__update_fact_table_incremental()
        return self

    def update_star_schema_initial(self):
        RkiVaccinationData.remove_all()
        RkiVaccinationDateReported.remove_all()
        self.__update_dimension_table_date_reported()
        self.__update_fact_table_initial()
        return self
