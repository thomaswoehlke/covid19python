# CHANGES

## Milestones

### 0.0.1 Release
* Fixed #1 test 1 2 3

### 0.0.2 Release
* Fixed #2 start data update job via web ui 
* Fixed #4 data update: who_country
* Fixed #6 data update: who_global_data
* Fixed #3 web ui: show table of who_region

### 0.0.3 Release
* Fixed #8 view_who_today_new_deaths
* Fixed #9 view_who_global_data
* Fixed #10 view_who_today_new_cases
* Fixed #11 view_who_germany
* Fixed #12 view_max_new_deaths_who

### 0.0.4 Release
* Fixed #13 Pagination for all Tables
* Fixed #14 Running on Windows and Linux
* Fixed #15 Navigation: Region, Countries, Data per Countries order by Date

### 0.0.5 Release
* Fixed #1 Async Tasks for import and update Data with Celery and RabbitMQ
* Fixed #2 Move Repo to github

### 0.0.6 Release
* Fixed #6 data of all reported countries for WHO date reported
* Fixed #7 WHO Countries all - data for Country

### 0.0.7 Release
* Issue #8 WhoServiceUpdate.update_db_short()
* Issue #9 URL: /who/update/short 
* Issue #10 async who_update_short_task
* Issue #11 WhoServiceUpdate.__update_who_global_data_short()
* Fixed #12 better layout for flash messages

### 0.0.8 Release
* Fixed #13 /who/imported/
* Fixed #14 /europe/imported/
* Fixed #15 /who/update: Download  
* Fixed #16 /who/update: Import File to DB
* Fixed #17 /who/update: Update DB
* Fixed #21 better templates for who_global_data tables

### 0.0.9 Release
* Fixed #18 /europe/update: Download
* Fixed #19 /europe/update: Import File to DB
* Fixed #20 /europe/update: Update DB
* Fixed #21 update_date_reported
* Fixed #22 update_continent
* Fixed #23 update_country
* Fixed #24 update_data
* Fixed #25 /who/update/initial update_data_initial
* Fixed #27 /admin/database/drop
* Fixed #3 ORM: 3NF for ecdc_europa_data_import
* Fixed #4 data update for 3NF ecdc_europa_data_import

### 0.0.10 Release
* Fixed #24 update_data
* Fixed #29 /who/info 
* Fixed #30 /europa/info 
* Fixed #31 /rki/info 
* Fixed #32 /nrw/info
* Fixed #33 /europe/date_reported
* Fixed #34 /europe/continent
* Fixed #35 /europe/country
* Fixed #36 /europe/data
* Fixed #37 switch from RabbitMQ to Redis
* Fixed #38 update Celery from 4 to 5

### 0.0.11 Release
* Fixed #26 /admin/database/dump
* Fixed #43 /europe/date_reported
* Fixed #44 /europe/continent
* Fixed #45 /europe/country
* Fixed #46 /europe/country/germany
* Fixed #50 remove unused requirements from requirements.txt
* Fixed #51 /europe/imported

### 0.0.12 Release
* Fixed #55 /vaccination/tasks
* Fixed #56 /vaccination/info

### 0.0.13 Release
* Fixed #49 EuropeServiceUpdate.__update_data_short() (wontfix)
* Fixed #52 download vaccination timeline data file
* Fixed #53 import vaccination timeline data file into db
* Fixed #54 /vaccination/imported
* Fixed #57 frontend: use npm for handling 3rdParty css and javascript modules like jQuery, Bootstrap
* Fixed #58 frontend: remove jumbotron from all pageheader, put jumbotron as main content on home page
* Fixed #47 major refactoring: Routes from app.py to org...who,europe,... (Doublette von #65)
* Fixed #48 major refactoring: Tasks from server_mq.py to org...who,europe,... (Doublette von #65)
* Fixed #64 major refactoring: create two packages: for web app and for celery worker
* Fixed #68 TODO: move Queries from Services to Model-Classes 
* Fixed #65 major refactoring: add flask-blueprints for admin, common, europe, rki, vaccination, who

### 0.0.14 Release
* Fixed #69 Branch: ISSUE_66_ATTEMPT_01
* Fixed #70 load package.json from Bootstrap-Template sb-admin-angular into statics
* Fixed #67 implement Flask-Login (wontfix)
* Issue #159 merge Branch ISSUE_66_ATTEMPT_01 to master
* Fixed #71 add python modules to requirements.txt for User Login, Authentication and Autorisation
* Fixed #72 add python modules to requirements.txt for Ajax and other JS Features
* Fixed #73 add python modules to requirements.txt for further research and development
* Fixed #74 add Tasks to WHO Tasks Html
* Fixed #78 add PlantUML
* Fixed #79 add Gaphor UML (wonfix)
* Fixed #80 rename WhoXYImport to WhoImport
* Fixed #81 change tablename from who_global_data_import to who_import
* Fixed #84 rename tablename from who_global_data to who_data
* Fixed #85 rename WhoData to WhoData
* Fixed #86 rename VaccinationDataXY to VaccinationData
* Fixed #89 change tablename from vaccination_germany_timeline_import to vaccination_import
* Fixed #75 add Tasks to Europe Tasks Html 
* Fixed #76 add Tasks to Vaccination Tasks Html 
* Fixed #77 add Tasks to RKI Tasks Html
* Fixed #124 rename RkiXXZBundeslaender to RkiBundeslaender
* Fixed #162 rename table vaccination_germany_timeline into vaccination_data
* Fixed #130 remove RkiGermanyDataImportTable
* ------------------------------------- 

### 0.0.15 Release
* -------------------------------------
* Fixed #88 rename VaccinationImport to VaccinationImport
* Fixed #89 change tablename from vaccination_germany_timeline_import to vaccination_import
* Fixed #86 rename VaccinationData to VaccinationData
* Fixed #162 rename table vaccination_germany_timeline into vaccination_data
* -------------------------------------
* Fixed #170 implement url_vaccination_task_update_star_schema_initial in vaccination_views.py
* Fixed #171 implement url_vaccination_task_update_starschema_incremental in vaccination_views.py
* Fixed #172 implement url_vaccination_task_import_only in vaccination_views.py
* Fixed #173 implement url_vaccination_task_import_only in vaccination_views.py
* Fixed #174 implement url_vaccination_task_update_dimensiontables_only in vaccination_views.py
* Fixed #175 implement url_vaccination_task_update_facttable_incremental_only in vaccination_views.py
* Fixed #176 implement url_vaccination_task_update_facttable_initial_only in vaccination_views.py
* -------------------------------------
* Fixed #91 implement VaccinationService.run_download_only
* Fixed #92 implement VaccinationService.run_import_only
* Fixed #93 implement VaccinationService.run_update_dimension_tables_only
* Fixed #94 implement VaccinationService.run_update_fact_table_incremental_only
* Fixed #95 implement VaccinationService.run_update_fact_table_initial_only
* Fixed #96 implement VaccinationService.run_update_star_schema_incremental
* Fixed #97 implement VaccinationService.run_update_star_schema_initial
* Fixed #101 implement VaccinationServiceUpdate.update_dimension_tables_only
* Fixed #102 implement VaccinationServiceUpdate.update_fact_table_incremental_only
* Fixed #103 implement VaccinationServiceUpdate.update_fact_table_initial_only
* Fixed #104 implement VaccinationServiceUpdate.update_star_schema_incremental
* Fixed #105 implement VaccinationServiceUpdate.update_star_schema_initial
* -------------------------------------
* Fixed #90 refactor VaccinationService to new method scheme introduced 07.02.2021
* Fixed #98 refactor VaccinationServiceDownload to new method scheme introduced 07.02.2021
* Fixed #99 refactor VaccinationServiceImport to new method scheme introduced 07.02.2021
* Fixed #100 refactor VaccinationServiceUpdate to new method scheme introduced 07.02.2021
* -------------------------------------
* Fixed #87 change to: Vaccination.datum many to one VaccinationDateReported
* Fixed #106 add Tasks and URLs for starting Tasks to vaccination_views
* -------------------------------------  

### 0.0.16 Release
* -------------------------------------   
* Issue #82 change to ORM ClassHierarchy
* Issue #108 change to ORM ClassHierarchy in: EuropeImport.get_countries_of_continent  
* Issue #129 change to ORM ClassHierarchy in: RkiLandkreiseImport.get_new_dates_as_array
* Issue #131 change to ORM ClassHierarchy in: RkiGermanyDataImportTable.get_new_dates_as_array
* -------------------------------------   
* Issue #111 refactor to new method scheme itroduced 07.02.2021
* Issue #117 refactor EuropeServiceUpdate to new method scheme introduced 07.02.2021 
* Issue #112 implement EuropeService.run_update_dimension_tables_only
* Issue #113 implement EuropeService.run_update_fact_table_incremental_only
* Issue #114 implement EuropeService.run_update_fact_table_initial_only
* Issue #115 implement EuropeService.run_update_star_schema_incremental
* Issue #116 implement EuropeService.run_update_star_schema_initial
* Issue #118 implement EuropeServiceUpdate.update_dimension_tables_only
* Issue #119 implement EuropeServiceUpdate.update_fact_table_incremental_only
* Issue #120 implement EuropeServiceUpdate.update_fact_table_initial_only
* Issue #121 implement EuropeServiceUpdate.update_star_schema_incremental
* Issue #122 implement EuropeServiceUpdate.update_star_schema_initial
* -------------------------------------
* Issue #163 implement url_europe_task_update_star_schema_initial in europe_views.py
* Issue #164 implement url_europe_task_update_starschema_incremental in europe_views.py
* Issue #165 implement url_europe_task_download_only in europe_views.py
* Issue #166 implement url_europe_task_import_only in europe_views.py
* Issue #167 implement url_europe_task_update_dimensiontables_only in europe_views.py
* Issue #168 implement url_europe_task_update_facttable_incremental_only in europe_views.py
* Issue #169 implement url_europe_task_update_facttable_initial_only in europe_views.py


### 0.0.17 Release
* Issue #146 add Tasks and URLs for starting Tasks to rki_views
* Issue #140 move WhoImport to RKI in: rk_service_import.py
* Issue #139 refactor RkiBundeslaenderServiceDownload to new method scheme introduced 07.02.2021
* Issue #123 split RkiBundeslaenderService into two Services, one for bundeslaender and one for landkreise
* Issue #125 implement RkiLandkreise
* Issue #126 implement RkiBundeslaenderImport
* Issue #127 implement RkiBundeslaenderImport.get_dates_reported
* Issue #128 add fields from csv to RkiLandkreiseImport
* Issue #132 refactor RkiBundeslaenderService to new method scheme introduced 07.02.2021
* Issue #133 implement RkiBundeslaenderService.task_database_drop_create
* Issue #134 implement RkiBundeslaenderService.run_update_dimension_tables_only
* Issue #135 implement RkiBundeslaenderService.run_update_fact_table_incremental_only
* Issue #136 implement RkiBundeslaenderService.run_update_fact_table_initial_only
* Issue #137 implement RkiBundeslaenderService.run_update_star_schema_incremental
* Issue #138 implement RkiBundeslaenderService.run_update_star_schema_initial
* Issue #141 implement RkiBundeslaenderServiceUpdate.update_dimension_tables_only
* Issue #142 implement RkiBundeslaenderServiceUpdate.update_fact_table_incremental_only
* Issue #143 implement RkiBundeslaenderServiceUpdate.update_fact_table_initial_only
* Issue #144 implement RkiBundeslaenderServiceUpdate.update_star_schema_incremental
* Issue #145 implement RkiBundeslaenderServiceUpdate.update_star_schema_initial
* Issue #147 refactor RkiBundeslaenderServiceUpdate.__update_who_date_reported 
* Issue #148 refactor RkiBundeslaenderServiceUpdate.__update_who_region
* Issue #149 refactor RkiBundeslaenderServiceUpdate.__update_who_country
* Issue #150 refactor RkiBundeslaenderServiceUpdate.__update_who_global_data
* Issue #151 refactor RkiBundeslaenderServiceUpdate.__update_who_global_data_short
* Issue #152 refactor RkiBundeslaenderServiceUpdate.__update_who_global_data_initial
* Issue #153 refactor RkiBundeslaenderServiceUpdate.update_db
* Issue #154 refactor RkiBundeslaenderServiceUpdate.update_db_short
* Issue #155 refactor RkiBundeslaenderServiceUpdate.update_db_initial

### 0.0.18 Release
* Issue #39 SQLalchemy instead of SQL: AllModelClasses.remove_all()
* Issue #40 SQLalchemy instead of SQL: EuropeImport.get_date_rep()
* Issue #41 SQLalchemy instead of SQL: EuropeImport.get_countries_of_continent()
* Issue #42 SQLalchemy instead of SQL: WhoImport.get_new_dates_as_array()
* Issue #83 SQLalchemy instead of SQL in WhoImport.get_new_dates_as_array
* Issue #107 SQLalchemy instead of SQL in: EuropeImport.get_countries_of_continent
* Issue #109 SQLalchemy instead of SQL in: EuropeImport.get_date_rep
* Issue #110 SQLalchemy instead of SQL in: EuropeImport.get_continent

### 0.0.198 Release
* Issue #5 Visual Graphs for Data per Countries order by Date
* Issue #59 frontend: add correct breadcrumb to every page
* Issue #60 frontend: better design for tables
* Issue #61 frontend: better design for navtabs
* Issue #62 frontend: better design for pages
* Issue #63 frontend: add footer design

### 0.0.20 Release
* Issue #28 /admin/database/import
* Issue #66 frontend: migrate to Bootstrap Theme sb-admin-angular
* Issue #158 load Bootstrap-Template sb-admin-angular into static

### 0.0.21 Release
* -------------------------------------  
* Issue #156 run_web.sh
* Issue #157 run_worker.sh