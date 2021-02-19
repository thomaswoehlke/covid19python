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
                    objectid=int(result_item.objectid),
                    ade=int(result_item.ade),
                    gf=int(result_item.gf),
                    bsg=int(result_item.bsg),
                    rs=int(result_item.rs),
                    ags=int(result_item.ags),
                    sdv_rs=int(result_item.sdv_rs),
                    gen=int(result_item.gen),
                    bez=int(result_item.bez),
                    ibz=int(result_item.ibz),
                    bem=int(result_item.bem),
                    nbd=int(result_item.nbd),
                    sn_l=int(result_item.sn_l),
                    sn_r=int(result_item.sn_r),
                    sn_k=int(result_item.sn_k),
                    sn_v1=int(result_item.sn_v1),
                    sn_v2=int(result_item.sn_v2),
                    sn_g=int(result_item.sn_g),
                    fk_s3=int(result_item.fk_s3),
                    nuts=int(result_item.nuts),
                    rs_0=int(result_item.rs_0),
                    ags_0=int(result_item.ags_0),
                    wsk=int(result_item.wsk),
                    ewz=int(result_item.ewz),
                    kfl=int(result_item.kfl),
                    debkg_id=int(result_item.debkg_id),
                    death_rate=int(result_item.death_rate),
                    cases=int(result_item.cases),
                    deaths=int(result_item.deaths),
                    cases_per_100k=int(result_item.cases_per_100k),
                    cases_per_population=int(result_item.cases_per_population),
                    bl=int(result_item.bl),
                    bl_id=int(result_item.bl_id),
                    county=int(result_item.county),
                    last_update=int(result_item.last_update),
                    cases7_per_100k=int(result_item.cases7_per_100k),
                    recovered=int(result_item.recovered),
                    ewz_bl=int(result_item.ewz_bl),
                    cases7_bl_per_100k=int(result_item.cases7_bl_per_100k),
                    cases7_bl=int(result_item.cases7_bl),
                    death7_bl=int(result_item.death7_bl),
                    cases7_lk=int(result_item.cases7_lk),
                    death7_lk=int(result_item.death7_lk),
                    cases7_per_100k_txt=int(result_item.cases7_per_100k_txt),
                    adm_unit_id=int(result_item.adm_unit_id),
                    shape_length=int(result_item.shape_length),
                    shape_area=int(result_item.shape_area),
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
                    objectid=int(result_item.objectid),
                    ade=int(result_item.ade),
                    gf=int(result_item.gf),
                    bsg=int(result_item.bsg),
                    rs=int(result_item.rs),
                    ags=int(result_item.ags),
                    sdv_rs=int(result_item.sdv_rs),
                    gen=int(result_item.gen),
                    bez=int(result_item.bez),
                    ibz=int(result_item.ibz),
                    bem=int(result_item.bem),
                    nbd=int(result_item.nbd),
                    sn_l=int(result_item.sn_l),
                    sn_r=int(result_item.sn_r),
                    sn_k=int(result_item.sn_k),
                    sn_v1=int(result_item.sn_v1),
                    sn_v2=int(result_item.sn_v2),
                    sn_g=int(result_item.sn_g),
                    fk_s3=int(result_item.fk_s3),
                    nuts=int(result_item.nuts),
                    rs_0=int(result_item.rs_0),
                    ags_0=int(result_item.ags_0),
                    wsk=int(result_item.wsk),
                    ewz=int(result_item.ewz),
                    kfl=int(result_item.kfl),
                    debkg_id=int(result_item.debkg_id),
                    death_rate=int(result_item.death_rate),
                    cases=int(result_item.cases),
                    deaths=int(result_item.deaths),
                    cases_per_100k=int(result_item.cases_per_100k),
                    cases_per_population=int(result_item.cases_per_population),
                    bl=int(result_item.bl),
                    bl_id=int(result_item.bl_id),
                    county=int(result_item.county),
                    last_update=int(result_item.last_update),
                    cases7_per_100k=int(result_item.cases7_per_100k),
                    recovered=int(result_item.recovered),
                    ewz_bl=int(result_item.ewz_bl),
                    cases7_bl_per_100k=int(result_item.cases7_bl_per_100k),
                    cases7_bl=int(result_item.cases7_bl),
                    death7_bl=int(result_item.death7_bl),
                    cases7_lk=int(result_item.cases7_lk),
                    death7_lk=int(result_item.death7_lk),
                    cases7_per_100k_txt=int(result_item.cases7_per_100k_txt),
                    adm_unit_id=int(result_item.adm_unit_id),
                    shape_length=int(result_item.shape_length),
                    shape_area=int(result_item.shape_area),
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

