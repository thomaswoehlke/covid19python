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
* Fixed #49 EcdcServiceUpdate.__update_data_short() (wontfix)
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
* Fixed #80 rename WhoXYImport to OwidImport
* Fixed #81 change tablename from who_global_data_import to who_import
* Fixed #84 rename tablename from who_global_data to who_data
* Fixed #85 rename WhoData to WhoData
* Fixed #86 rename VaccinationDataXY to RkiVaccinationData
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
* Fixed #88 rename RkiVaccinationImport to RkiVaccinationImport
* Fixed #89 change tablename from vaccination_germany_timeline_import to vaccination_import
* Fixed #86 rename RkiVaccinationData to RkiVaccinationData
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
* Fixed #91 implement RkiVaccinationService.run_download_only
* Fixed #92 implement RkiVaccinationService.run_import_only
* Fixed #93 implement RkiVaccinationService.run_update_dimension_tables_only
* Fixed #94 implement RkiVaccinationService.run_update_fact_table_incremental_only
* Fixed #95 implement RkiVaccinationService.run_update_fact_table_initial_only
* Fixed #96 implement RkiVaccinationService.run_update_star_schema_incremental
* Fixed #97 implement RkiVaccinationService.run_update_star_schema_initial
* Fixed #101 implement RkiVaccinationServiceUpdate.update_dimension_tables_only
* Fixed #102 implement RkiVaccinationServiceUpdate.update_fact_table_incremental_only
* Fixed #103 implement RkiVaccinationServiceUpdate.update_fact_table_initial_only
* Fixed #104 implement RkiVaccinationServiceUpdate.update_star_schema_incremental
* Fixed #105 implement RkiVaccinationServiceUpdate.update_star_schema_initial
* -------------------------------------
* Fixed #90 refactor RkiVaccinationService to new method scheme introduced 07.02.2021
* Fixed #98 refactor RkiVaccinationServiceDownload to new method scheme introduced 07.02.2021
* Fixed #99 refactor RkiVaccinationServiceImport to new method scheme introduced 07.02.2021
* Fixed #100 refactor RkiVaccinationServiceUpdate to new method scheme introduced 07.02.2021
* -------------------------------------
* Fixed #87 change to: Vaccination.datum many to one RkiVaccinationDateReported
* Fixed #106 add Tasks and URLs for starting Tasks to vaccination_views
* -------------------------------------  

### 0.0.16 Release
* Fixed #111 refactor to new method scheme introduced 07.02.2021
* Fixed #117 refactor EcdcServiceUpdate to new method scheme introduced 07.02.2021 
* Fixed #112 implement EcdcService.run_update_dimension_tables_only
* Fixed #113 implement EcdcService.run_update_fact_table_incremental_only
* Fixed #114 implement EcdcService.run_update_fact_table_initial_only
* Fixed #115 implement EcdcService.run_update_star_schema_incremental
* Fixed #116 implement EcdcService.run_update_star_schema_initial
* Fixed #118 implement EcdcServiceUpdate.update_dimension_tables_only
* Fixed #119 implement EcdcServiceUpdate.update_fact_table_incremental_only
* Fixed #120 implement EcdcServiceUpdate.update_fact_table_initial_only
* Fixed #121 implement EcdcServiceUpdate.update_star_schema_incremental
* Fixed #122 implement EcdcServiceUpdate.update_star_schema_initial
* -------------------------------------
* Fixed #163 implement url_europe_task_update_star_schema_initial in europe_views.py
* Fixed #164 implement url_europe_task_update_starschema_incremental in europe_views.py
* Fixed #165 implement url_europe_task_download_only in europe_views.py
* Fixed #166 implement url_europe_task_import_only in europe_views.py
* Fixed #167 implement url_europe_task_update_dimensiontables_only in europe_views.py
* Fixed #168 implement url_europe_task_update_facttable_incremental_only in europe_views.py
* Fixed #169 implement url_europe_task_update_facttable_initial_only in europe_views.py


### 0.0.17 Release
* Fixed #82 change to ORM ClassHierarchy
* Fixed #42 SQLalchemy instead of SQL: OwidImport.get_new_dates_as_array()
* Fixed #83 SQLalchemy instead of SQL in OwidImport.get_new_dates_as_array
* Fixed #108 change to ORM ClassHierarchy in: EcdcImport.get_countries_of_continent
* Fixed #39 SQLalchemy instead of SQL: AllModelClasses.remove_all()
* Fixed #40 SQLalchemy instead of SQL: EcdcImport.get_date_rep()
* Fixed #41 SQLalchemy instead of SQL: EcdcImport.get_countries_of_continent()
* Fixed #107 SQLalchemy instead of SQL in: EcdcImport.get_countries_of_continent
* Fixed #109 SQLalchemy instead of SQL in: EcdcImport.get_date_rep
* Fixed #110 SQLalchemy instead of SQL in: EcdcImport.get_continent
* Fixed #123 split RkiBundeslaenderService into two Services, one for bundeslaender and one for landkreise
* Fixed #128 add fields from csv to RkiLandkreiseImport
* Fixed #139 refactor RkiBundeslaenderServiceDownload to new method scheme introduced 07.02.2021
* Fixed #140 move OwidImport to RKI in: rk_service_import.py
* Fixed #125 implement RkiLandkreise
* Fixed #126 implement RkiBundeslaenderImport


### 0.0.18 Release
* Fixed #133 implement RkiBundeslaenderService.task_database_drop_create
* Fixed #134 implement RkiBundeslaenderService.run_update_dimension_tables_only
* Fixed #135 implement RkiBundeslaenderService.run_update_fact_table_incremental_only
* Fixed #136 implement RkiBundeslaenderService.run_update_fact_table_initial_only
* Fixed #137 implement RkiBundeslaenderService.run_update_star_schema_incremental
* Fixed #138 implement RkiBundeslaenderService.run_update_star_schema_initial
* Fixed #132 refactor RkiBundeslaenderService to new method scheme introduced 07.02.2021
* -------------------------------------
* Fixed #147 refactor RkiBundeslaenderServiceUpdate.__update_who_date_reported 
* Fixed #148 refactor RkiBundeslaenderServiceUpdate.__update_who_region
* Fixed #149 refactor RkiBundeslaenderServiceUpdate.__update_who_country
* Fixed #150 refactor RkiBundeslaenderServiceUpdate.__update_who_global_data
* Fixed #151 refactor RkiBundeslaenderServiceUpdate.__update_who_global_data_short
* Fixed #152 refactor RkiBundeslaenderServiceUpdate.__update_who_global_data_initial
* Fixed #153 refactor RkiBundeslaenderServiceUpdate.update_db
* Fixed #154 refactor RkiBundeslaenderServiceUpdate.update_db_short
* Fixed #155 refactor RkiBundeslaenderServiceUpdate.update_db_initial
* -------------------------------------
* Fixed #131 change to ORM ClassHierarchy in: RkiGermanyDataImportTable.get_new_dates_as_array
* Fixed #129 change to ORM ClassHierarchy in: RkiLandkreiseImport.get_new_dates_as_array
* Fixed #146 add Tasks and URLs for starting Tasks to rki_views  
* Fixed #127 implement RkiBundeslaenderImport.get_dates_reported
* -------------------------------------
* Fixed #141 implement RkiBundeslaenderServiceUpdate.update_dimension_tables_only
* Fixed #142 implement RkiBundeslaenderServiceUpdate.update_fact_table_incremental_only
* Fixed #143 implement RkiBundeslaenderServiceUpdate.update_fact_table_initial_only
* Fixed #144 implement RkiBundeslaenderServiceUpdate.update_star_schema_incremental
* Fixed #145 implement RkiBundeslaenderServiceUpdate.update_star_schema_initial

### 0.0.19 Release
* ------------------------------------- 

### 0.0.20 Release
* ------------------------------------- 

### 0.0.21 Release
* -------------------------------------  

### 0.0.22 Release
* -------------------------------------

### 0.0.23 Release
* -------------------------------------

### 0.0.24 Release
* -------------------------------------
* Fixed #28 /admin/database/import
* Fixed #66 frontend: migrate to Bootstrap Theme sb-admin-angular
* Fixed #158 load Bootstrap-Template sb-admin-angular into static
* Fixed #191 setup plantuml for engineering and docs 
* Fixed #156 run_web.sh
* Fixed #157 run_worker.sh
* Fixed #62 frontend: better design for pages
* Fixed #60 frontend: better design for tables

### 0.0.25 Release
* -------------------------------------  

### 0.0.26 Release
* Fixed #194 dependency is unsecure

### 0.0.27 Release
* Fixed #60 frontend: better design for tables
* Fixed #62 frontend: better design for pages
* Fixed #197 UML use cases for OWID reports and Visual Data  

### 0.0.28 Release
* Fixed #199 Database export without gzip
* Fixed #200 Database import without gzip

### 0.0.29 Release
* Fixed #201 UML: blueprint user 
* Fixed #205 navbar is broken
* Fixed #202 add blueprint user
* Fixed #203 find python module for blueprint user
* Fixed #204 add python module for blueprint user

### 0.0.30 Release
* Fixed #206 implement user login and authorization using blueprint user and flask-login

### 0.0.31 Release
* -------------------------------------
* Fixed #211 ECDC-templates: change URL to for_url()
* Fixed #213 WHO-template: change URL to for_url() 
* -------------------------------------    
* Issue #195 RkiVaccinationImport.get_daterep_missing_in_vaccination_data(): native SQL to SQLalechemy Query
* Issue #83  WhoImport.get_new_dates_as_array() SQLalchemy instead of SQL
* Fixed #219 WhoImport.countries() SQLalchemy instead of SQL
* -------------------------------------
* Issue #207 remove deprecated: database.port
* Issue #208 remove deprecated: database.run_run_with_debug
* Issue #209 remove deprecated: database.ITEMS_PER_PAGE
* -------------------------------------  
* Issue #210 database.py: logging for Celery on Windows
*-------------------------------------
* Issue #196 OwidImport.get_new_dates_reported_as_array() needs implementation
* -------------------------------------
* Issue #212 implement OwidService.task_database_drop_create()
* -------------------------------------
* Issue #214 implement OwidServiceUpdate.update_dimension_tables_only()
* Issue #215 implement OwidServiceUpdate.update_fact_table_incremental_only()
* Issue #216 implement OwidServiceUpdate.update_fact_table_initial_only()
* Issue #217 implement OwidServiceUpdate.update_star_schema_incremental()
* Issue #218 implement OwidServiceUpdate.update_star_schema_initial()
* -------------------------------------


### 00 Inbox
* -------------------------------------

### 01 Next
* -------------------------------------
* Issue #198 UML: WHO Visual Graphs for Data per Countries order by Date
* Issue #5 WHO Visual Graphs for Data per Countries order by Date
* -------------------------------------
* Issue #177 BUG: RkiBundeslaenderServiceImport.import_file 
* Issue #178 BUG: RkiLandkreiseServiceImport.import_file

### 02 Soon
* -------------------------------------
* Issue #189 setup unit tests
* Issue #190 setup docs with sphinx

### 03 Nice to Have
* -------------------------------------
* Issue #59 frontend: add correct breadcrumb to every page
* Issue #61 frontend: better design for navtabs
* Issue #63 frontend: add footer design

### 04 Dropped
* -------------------------------------
* Issue #185 add Flask-Redisboard
* Issue #186 add Flask-Monitoring

### 05 Later maybe
* -------------------------------------
* Issue #179 add Flask-Caching
* Issue #180 add build.cmd script
* Issue #181 add flask-filealchemy
* Issue #182 add flask-whooshalchemy3
* Issue #183 add flask-resources
* Issue #184 add Flask-Babel
* Issue #187 add Flask-Caching
* Issue #188 add flask-healthz
* Issue #192 flask-healthz
* Issue #193 add Flask-Moment


