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
        app.logger.info(" update RkiLandkreiseServiceUpdate [begin]")
        app.logger.info("------------------------------------------------------------")
        i = 0
        for last_update in RkiLandkreiseImport.get_last_updates():
            i += 1
            output = " [ " + str(i) + " ] " + last_update
            c = RkiDateReported.find_by_date_reported(last_update)
            if c is None:
                o = RkiDateReported.create_new_object_factory(aktualisierung=last_update)
                db.session.add(o)
                db.session.commit()
                output += " added"
            else:
                output += " NOT added " + str(c.id)
            app.logger.info(output)
        app.logger.info("")
        app.logger.info(" update RkiLandkreiseServiceUpdate [done]")
        app.logger.info("------------------------------------------------------------")
        return self

    def __update_data_incremental(self):
        app.logger.info(" update RkiLandkreiseServiceUpdate short [begin]")
        app.logger.info("------------------------------------------------------------")
        new_dates_reported_from_import = RkiLandkreiseImport.get_new_last_update_as_array()
        i = 0
        for my_date_reported in new_dates_reported_from_import:
            my_date = RkiDateReported.find_by_date_reported(my_date_reported)
            for result_item in RkiLandkreiseImport.find_by_last_update(my_date_reported):
                o = RkiLandkreise(
                    objectid=int(result_item.objectid),
                    ade=int(result_item.ade),
                    gf=int(result_item.gf),
                    bsg=int(result_item.bsg),
                    rs=result_item.rs,
                    ags=result_item.ags,
                    sdv_rs=result_item.sdv_rs,
                    gen=result_item.gen,
                    bez=result_item.bez,
                    ibz=int(result_item.ibz),
                    bem=result_item.bem,
                    nbd=result_item.nbd,
                    sn_l=result_item.sn_l,
                    sn_r=int(result_item.sn_r),
                    sn_k=result_item.sn_k,
                    sn_v1=result_item.sn_v1,
                    sn_v2=result_item.sn_v2,
                    sn_g=result_item.sn_g,
                    fk_s3=result_item.fk_s3,
                    nuts=result_item.nuts,
                    rs_0=result_item.rs_0,
                    ags_0=int(result_item.ags_0),
                    wsk=int(result_item.wsk),
                    ewz=int(result_item.ewz),
                    kfl=int(result_item.kfl),
                    debkg_id=result_item.debkg_id,
                    death_rate=int(result_item.death_rate),
                    cases=int(result_item.cases),
                    deaths=int(result_item.deaths),
                    cases_per_100k=int(result_item.cases_per_100k),
                    cases_per_population=float(result_item.cases_per_population),
                    bl=result_item.bl,
                    bl_id=result_item.bl_id,
                    county=result_item.county,
                    last_update=result_item.last_update,
                    cases7_per_100k=int(result_item.cases7_per_100k),
                    recovered=int(result_item.recovered),
                    ewz_bl=int(result_item.ewz_bl),
                    cases7_bl_per_100k=float(result_item.cases7_bl_per_100k),
                    cases7_bl=int(result_item.cases7_bl),
                    death7_bl=int(result_item.death7_bl),
                    cases7_lk=int(result_item.cases7_lk),
                    death7_lk=int(result_item.death7_lk),
                    cases7_per_100k_txt=result_item.cases7_per_100k_txt,
                    adm_unit_id=int(result_item.adm_unit_id),
                    shape_length=float(result_item.shape_length),
                    shape_area=float(result_item.shape_area),
                )
                db.session.add(o)
                i += 1
                if i % 500 == 0:
                    app.logger.info(" update RkiLandkreiseServiceUpdate short ... "+str(i)+" rows")
                    db.session.commit()
            db.session.commit()
        app.logger.info(" update RkiLandkreiseServiceUpdate short :  "+str(i)+" total rows")
        app.logger.info(" update RkiLandkreiseServiceUpdate short [done]")
        app.logger.info("------------------------------------------------------------")
        return self

    def __update_data_initial(self):
        app.logger.info(" update RkiLandkreiseServiceUpdate initial [begin]")
        app.logger.info("------------------------------------------------------------")
        RkiLandkreise.remove_all()
        last_updates_from_import = RkiLandkreiseImport.get_last_updates()
        i = 0
        for last_update_from_import in last_updates_from_import:
            my_date = RkiDateReported.find_by_date_reported(last_update_from_import)
            for result_item in RkiLandkreiseImport.find_by_last_update(last_update_from_import):
                o = RkiLandkreise(
                    objectid=int(result_item.objectid),
                    ade=int(result_item.ade),
                    gf=int(result_item.gf),
                    bsg=int(result_item.bsg),
                    rs=result_item.rs,
                    ags=result_item.ags,
                    sdv_rs=result_item.sdv_rs,
                    gen=result_item.gen,
                    bez=result_item.bez,
                    ibz=int(result_item.ibz),
                    bem=result_item.bem,
                    nbd=result_item.nbd,
                    sn_l=result_item.sn_l,
                    sn_r=int(result_item.sn_r),
                    sn_k=result_item.sn_k,
                    sn_v1=result_item.sn_v1,
                    sn_v2=result_item.sn_v2,
                    sn_g=result_item.sn_g,
                    fk_s3=result_item.fk_s3,
                    nuts=result_item.nuts,
                    rs_0=result_item.rs_0,
                    ags_0=int(result_item.ags_0),
                    wsk=int(result_item.wsk),
                    ewz=int(result_item.ewz),
                    kfl=int(result_item.kfl),
                    debkg_id=result_item.debkg_id,
                    death_rate=int(result_item.death_rate),
                    cases=int(result_item.cases),
                    deaths=int(result_item.deaths),
                    cases_per_100k=int(result_item.cases_per_100k),
                    cases_per_population=float(result_item.cases_per_population),
                    bl=result_item.bl,
                    bl_id=result_item.bl_id,
                    county=result_item.county,
                    last_update=result_item.last_update,
                    cases7_per_100k=int(result_item.cases7_per_100k),
                    recovered=int(result_item.recovered),
                    ewz_bl=int(result_item.ewz_bl),
                    cases7_bl_per_100k=float(result_item.cases7_bl_per_100k),
                    cases7_bl=int(result_item.cases7_bl),
                    death7_bl=int(result_item.death7_bl),
                    cases7_lk=int(result_item.cases7_lk),
                    death7_lk=int(result_item.death7_lk),
                    cases7_per_100k_txt=result_item.cases7_per_100k_txt,
                    adm_unit_id=int(result_item.adm_unit_id),
                    shape_length=float(result_item.shape_length),
                    shape_area=float(result_item.shape_area),
                )
                db.session.add(o)
                i += 1
                if i % 500 == 0:
                    app.logger.info(" update RkiLandkreiseServiceUpdate initial ... "+str(i)+" rows")
                    db.session.commit()
            db.session.commit()
        app.logger.info(" update RkiLandkreiseServiceUpdate initial :  "+str(i)+" total rows")
        app.logger.info(" update RkiLandkreiseServiceUpdate initial [done]")
        app.logger.info("------------------------------------------------------------")
        return self

    def update_dimension_tables_only(self):
        self.__update_date_reported()
        return self

    def update_fact_table_incremental_only(self):
        self.__update_data_incremental()
        return self

    def update_fact_table_initial_only(self):
        self.__update_data_initial()
        return self

    def update_star_schema_incremental(self):
        self.__update_date_reported()
        self.__update_data_incremental()
        return self

    def update_star_schema_initial(self):
        self.__update_date_reported()
        self.__update_data_initial()
        return self


