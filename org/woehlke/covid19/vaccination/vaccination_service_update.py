import os
from database import db, app
from org.woehlke.covid19.vaccination.vaccination_model import VaccinationDataImportTable, VaccinationDateReported
from org.woehlke.covid19.vaccination.vaccination_model import VaccinationCountry, VaccinationRegion, VaccinationData


vaccination_service_update = None


class VaccinationServiceUpdate:
    def __init__(self, database):
        app.logger.info("------------------------------------------------------------")
        app.logger.info(" Vaccination Service Update [init]")
        app.logger.info("------------------------------------------------------------")
        self.__database = database
        self.limit_nr = 20
        self.__cvsfile_name = "germany_vaccinations_timeseries_v2.tsv"
        self.__src_cvsfile_name = "data" + os.sep + self.__cvsfile_name
        self.__src_cvsfile_tmp_name = "data" + os.sep + "tmp_" + self.__cvsfile_name
        self.__url_src_data = "https://impfdashboard.de/static/data/germany_vaccinations_timeseries_v2.tsv"
        app.logger.info("------------------------------------------------------------")
        app.logger.info(" Vaccination Service Update [ready]")

    def __update_who_date_reported(self):
        app.logger.info(" update who_date_reported [begin]")
        app.logger.info("------------------------------------------------------------")
        i = 0
        for i_date_reported, in VaccinationDataImportTable.get_dates_reported():
            c = VaccinationDateReported.find_by_date_reported(i_date_reported)
            if c is None:
                o = VaccinationDateReported(date_reported=i_date_reported)
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

    def __update_who_region(self):
        app.logger.info(" update who_region [begin]")
        app.logger.info("------------------------------------------------------------")
        i = 0
        for i_who_region, in db.session.query(VaccinationDataImportTable.who_region).distinct():
            c = db.session.query(VaccinationRegion).filter(VaccinationRegion.region == i_who_region).count()
            if c == 0:
                o = VaccinationRegion(region=i_who_region)
                db.session.add(o)
                app.logger.info(i_who_region +" added NEW ")
            else:
                app.logger.info(i_who_region +" not added ")
            if i % 10 == 0:
                db.session.commit()
            i += 1
        db.session.commit()
        app.logger.info("")
        app.logger.info(" update who_region [done]")
        app.logger.info("------------------------------------------------------------")
        return self

    def __update_who_country(self):
        app.logger.info(" update who_country [begin]")
        app.logger.info("------------------------------------------------------------")
        sql_text = """
        select distinct 
            who_global_data_import.country_code,
            who_global_data_import.country,
            who_global_data_import.who_region
        from who_global_data_import
        """
        result = db.session.execute(sql_text).fetchall()
        for result_item in result:
            i_country_code = result_item.country_code
            i_country = result_item.country
            i_who_region = result_item.who_region
            output = i_country_code + " " + i_country + " " + i_who_region
            my_region = VaccinationRegion.find_by_region(i_who_region)
            my_country = VaccinationCountry.find_by_country_code_and_country_and_who_region_id(
                i_country_code, i_country, my_region
            )
            if my_country is None:
                o = VaccinationCountry(
                    country=i_country,
                    country_code=i_country_code,
                    region=my_region)
                db.session.add(o)
                db.session.commit()
                my_country = VaccinationCountry.find_by_country_code_and_country_and_who_region_id(
                    i_country_code, i_country, my_region
                )
                output += " added NEW "
            else:
                output += " not added "
            output += i_country_code + " id=" + str(my_country.id)
            app.logger.info(output)
        db.session.commit()
        app.logger.info("")
        app.logger.info(" update who_country [done]")
        app.logger.info("------------------------------------------------------------")
        return self

    def __update_who_global_data(self):
        app.logger.info(" update Vaccination [begin]")
        app.logger.info("------------------------------------------------------------")
        dates_reported = VaccinationDateReported.get_all_as_dict()
        regions = VaccinationRegion.get_all_as_dict()
        countries = VaccinationCountry.get_all_as_dict()
        #
        #
        i = 0
        result = VaccinationDataImportTable.get_all()
        for result_item in result:
            my_country = countries[result_item.country_code]
            my_date_reported = dates_reported[result_item.date_reported]
            result_who_global_data = VaccinationData.find_one_or_none_by_date_and_country(
                my_date_reported,
                my_country)
            if result_who_global_data is None:
                o = VaccinationData(
                    cases_new=int(result_item.new_cases),
                    cases_cumulative=int(result_item.cumulative_cases),
                    deaths_new=int(result_item.new_deaths),
                    deaths_cumulative=int(result_item.cumulative_deaths),
                    date_reported=my_date_reported,
                    country=my_country
                )
                db.session.add(o)
            if i % 2000 == 0:
                app.logger.info(" update Vaccination ... "+str(i)+" rows")
                db.session.commit()
            i += 1
        db.session.commit()
        app.logger.info(" update Vaccination :  "+str(i)+" total rows")
        app.logger.info(" update Vaccination [done]")
        app.logger.info("------------------------------------------------------------")
        return self

    def __update_who_global_data_short(self):
        app.logger.info(" update Vaccination short [begin]")
        app.logger.info("------------------------------------------------------------")
        new_dates_reported_from_import = VaccinationDataImportTable.get_new_dates_as_array()
        i = 0
        for my_date_reported in new_dates_reported_from_import:
            my_date = VaccinationDateReported.find_by_date_reported(my_date_reported)
            for result_item in VaccinationDataImportTable.get_for_one_day(my_date_reported):
                my_country = VaccinationCountry.find_by_country_code(result_item.country_code)
                o = VaccinationData(
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
                    app.logger.info(" update Vaccination short ... "+str(i)+" rows")
                    db.session.commit()
            db.session.commit()
        app.logger.info(" update Vaccination short :  "+str(i)+" total rows")
        app.logger.info(" update Vaccination short [done]")
        app.logger.info("------------------------------------------------------------")
        return self

    def __update_who_global_data_initial(self):
        app.logger.info(" update Vaccination initial [begin]")
        app.logger.info("------------------------------------------------------------")
        VaccinationData.remove_all()
        new_dates_reported_from_import = VaccinationDataImportTable.get_new_dates_as_array()
        i = 0
        for my_date_reported in new_dates_reported_from_import:
            my_date = VaccinationDateReported.find_by_date_reported(my_date_reported)
            for result_item in VaccinationDataImportTable.get_for_one_day(my_date_reported):
                my_country = VaccinationCountry.find_by_country_code(result_item.country_code)
                o = VaccinationData(
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
                    app.logger.info(" update Vaccination initial ... "+str(i)+" rows")
                    db.session.commit()
            db.session.commit()
        app.logger.info(" update Vaccination initial :  "+str(i)+" total rows")
        app.logger.info(" update Vaccination initial [done]")
        app.logger.info("------------------------------------------------------------")
        return self

    def update_db(self):
        app.logger.info(" update db [begin]")
        app.logger.info("------------------------------------------------------------")
        self.__update_who_date_reported()
        self.__update_who_region()
        self.__update_who_country()
        self.__update_who_global_data()
        app.logger.info(" update db [done]")
        app.logger.info("------------------------------------------------------------")
        return self

    def update_db_short(self):
        app.logger.info(" update db short [begin]")
        app.logger.info("------------------------------------------------------------")
        self.__update_who_date_reported()
        self.__update_who_region()
        self.__update_who_country()
        self.__update_who_global_data_short()
        app.logger.info(" update db short [done]")
        app.logger.info("------------------------------------------------------------")
        return self

    def update_db_initial(self):
        app.logger.info(" update db initial [begin]")
        app.logger.info("------------------------------------------------------------")
        self.__update_who_date_reported()
        self.__update_who_region()
        self.__update_who_country()
        self.__update_who_global_data_initial()
        app.logger.info(" update db initial [done]")
        app.logger.info("------------------------------------------------------------")
        return self

    def update_who_country(self):
        self.__update_who_country()
        return self
