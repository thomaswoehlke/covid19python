from database import db, app

from covid19.blueprints.application.application_service_config import ApplicationServiceConfig
from covid19.blueprints.application.application_model import RkiDateReported
from covid19.blueprints.rki_bundeslaender.rki_bundeslaender_model import RkiBundeslaender
from covid19.blueprints.rki_bundeslaender.rki_bundeslaender_model_import import RkiBundeslaenderImport


class RkiBundeslaenderServiceUpdate:
    def __init__(self, database, config: ApplicationServiceConfig):
        app.logger.debug("------------------------------------------------------------")
        app.logger.debug(" RKI Service Update [init]")
        app.logger.debug("------------------------------------------------------------")
        self.__database = database
        self.cfg = config
        app.logger.debug("------------------------------------------------------------")
        app.logger.debug(" RKI Service Update [ready]")

    def __update_date_reported(self):
        app.logger.info(" update RkiDateReported [begin]")
        app.logger.info("------------------------------------------------------------")
        i = 0
        for aktualisierung in RkiBundeslaenderImport.get_aktualisierungen_as_array():
            i += 1
            output = " [ " + str(i) + " ] " + aktualisierung
            c = RkiDateReported.find_by_date_reported(aktualisierung)
            if c is None:
                o = RkiDateReported.create_new_object_factory(aktualisierung=aktualisierung)
                db.session.add(o)
                db.session.commit()
                output += " added"
            else:
                output += " NOT added " + str(c.id)
            app.logger.info(output)
        db.session.commit()
        app.logger.info("")
        app.logger.info(" update RkiDateReported [done]")
        app.logger.info("------------------------------------------------------------")
        return self

    def __update_data_incremental(self):
        app.logger.info(" update RkiBundeslaender short [begin]")
        app.logger.info("------------------------------------------------------------")
        aktualisierungen_from_import = RkiBundeslaenderImport.get_aktualisierungen_as_array()
        i = 0
        for aktualisierung_from_import in aktualisierungen_from_import:
            my_date = RkiDateReported.find_by_aktualisierung(aktualisierung_from_import)
            for result_item in RkiBundeslaenderImport.find_by_aktualisierung(aktualisierung_from_import):
                o = RkiBundeslaender(
                    object_id_1=int(result_item.OBJECTID_1),
                    lan_ew_ags=int(result_item.LAN_ew_AGS),
                    lan_ew_gen=result_item.LAN_ew_GEN,
                    lan_ew_bez=result_item.LAN_ew_BEZ,
                    lan_ew_ewz=int(result_item.LAN_ew_EWZ),
                    object_id=int(result_item.OBJECTID),
                    fallzahl=int(result_item.Fallzahl),
                    aktualisierung=result_item.Aktualisierung,
                    ags_txt=int(result_item.AGS_TXT),
                    global_id=result_item.GlobalID,  # uuid?
                    faelle_100000_ew=float(result_item.faelle_100000_EW),
                    death=int(result_item.Death),
                    cases7_bl_per_100k=int(result_item.cases7_bl_per_100k),
                    cases7_bl=int(result_item.cases7_bl),
                    death7_bl=int(result_item.death7_bl),
                    cases7_bl_per_100k_txt=result_item.cases7_bl_per_100k_txt,
                    adm_unit_id=int(result_item.AdmUnitId),
                    shape_length=float(result_item.SHAPE_Length),
                    shape_area=float(result_item.SHAPE_Area),
                )
                db.session.add(o)
                i += 1
                if i % 500 == 0:
                    app.logger.info(" update RkiBundeslaender short ... "+str(i)+" rows")
                    db.session.commit()
            db.session.commit()
        app.logger.info(" update RkiBundeslaender short :  "+str(i)+" total rows")
        app.logger.info(" update RkiBundeslaender short [done]")
        app.logger.info("------------------------------------------------------------")
        return self

    def __update_data_initial(self):
        app.logger.info(" update RKI initial [begin]")
        app.logger.info("------------------------------------------------------------")
        RkiBundeslaender.remove_all()
        aktualisierungen_from_import = RkiBundeslaenderImport.get_new_aktualisierungen_as_array()
        i = 0
        for aktualisierung_from_import in aktualisierungen_from_import:
            my_date = RkiDateReported.find_by_aktualisierung(aktualisierung_from_import)
            for result_item in RkiBundeslaenderImport.find_by_aktualisierung(aktualisierung_from_import):
                o = RkiBundeslaender(
                    object_id_1=int(result_item.OBJECTID_1),
                    lan_ew_ags=int(result_item.LAN_ew_AGS),
                    lan_ew_gen=result_item.LAN_ew_GEN,
                    lan_ew_bez=result_item.LAN_ew_BEZ,
                    lan_ew_ewz=int(result_item.LAN_ew_EWZ),
                    object_id=int(result_item.OBJECTID),
                    fallzahl=int(result_item.Fallzahl),
                    aktualisierung=result_item.Aktualisierung,
                    ags_txt=int(result_item.AGS_TXT),
                    global_id=result_item.GlobalID, # uuid?
                    faelle_100000_ew=float(result_item.faelle_100000_EW),
                    death=int(result_item.Death),
                    cases7_bl_per_100k=int(result_item.cases7_bl_per_100k),
                    cases7_bl=int(result_item.cases7_bl),
                    death7_bl=int(result_item.death7_bl),
                    cases7_bl_per_100k_txt=result_item.cases7_bl_per_100k_txt,
                    adm_unit_id=int(result_item.AdmUnitId),
                    shape_length=float(result_item.SHAPE_Length),
                    shape_area=float(result_item.SHAPE_Area),
                )
                db.session.add(o)
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

