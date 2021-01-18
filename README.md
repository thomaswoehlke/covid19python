# covid19python
* Version 0.0.5 SNAPSHOT

## git
### gitlab 
* https://git.noc.ruhr-uni-bochum.de/learn_r_and_python/covid19python.git
### github
* https://github.com/thomaswoehlke/covid19python.git

## Data Sources:
* [WHO](https://covid19.who.int/WHO-COVID-19-global-data.csv)
* [ecdc.europa](https://opendata.ecdc.europa.eu/covid19/casedistribution/csv)
* [ecdc.europa - Information](https://www.ecdc.europa.eu/en/publications-data/download-todays-data-geographic-distribution-covid-19-cases-worldwide)

## Python
* [flask](https://flask.palletsprojects.com/en/1.1.x/)
* [flask: pypi](https://pypi.org/project/Flask/)
* [flask: flask-admin](https://github.com/flask-admin/flask-admin/)
* [flask: werkzeug](https://werkzeug.palletsprojects.com/en/1.0.x/)
* [flask: sqlalchemy](https://flask.palletsprojects.com/en/1.1.x/patterns/sqlalchemy/)
* [sqlalchemy](https://docs.sqlalchemy.org/en/13/)
* [sqlite](https://sqlite.org/docs.html)
* [jinja](https://jinja.palletsprojects.com/en/2.11.x/)
* [jinja: markupsafe](https://palletsprojects.com/p/markupsafe/)
* [jinja: itsdangerous](https://palletsprojects.com/p/itsdangerous/)
* [jinja: click](https://palletsprojects.com/p/click/)

### Info
* http://www.leeladharan.com/sqlalchemy-query-with-or-and-like-common-filters
* https://riptutorial.com/flask/example/22201/pagination-route-example-with-flask-sqlalchemy-paginate

## Database

### WHO

#### who_date_reported
````postgresql
CREATE TABLE public.who_date_reported (
    id integer NOT NULL,
    date_reported character varying(255) NOT NULL
);
````
````python
class WhoDateReported(db.Model):
    __tablename__ = 'who_date_reported'

    id = db.Column(db.Integer, primary_key=True)
    date_reported = db.Column(db.String(255), unique=True, nullable=False)
````

#### who_region
````postgresql
CREATE TABLE public.who_region (
    id integer NOT NULL,
    region character varying(255) NOT NULL
);
````
````python
class WhoRegion(db.Model):
    __tablename__ = 'who_region'

    id = db.Column(db.Integer, primary_key=True)
    region = db.Column(db.String(255), unique=True, nullable=False)
````

#### who_country
````postgresql
CREATE TABLE public.who_country (
    id integer NOT NULL,
    country_code character varying(255) NOT NULL,
    country character varying(255) NOT NULL,
    region_id integer NOT NULL
);
````
````python
class WhoCountry(db.Model):
    __tablename__ = 'who_country'

    id = db.Column(db.Integer, primary_key=True)
    country_code = db.Column(db.String(255), unique=True, nullable=False)
    country = db.Column(db.String(255), unique=False, nullable=False)
    region_id = db.Column(db.Integer, db.ForeignKey('who_region.id'), nullable=False)
    region = db.relationship('WhoRegion', lazy='joined') 
````

#### who_global_data
````postgresql
CREATE TABLE public.who_global_data (
    id integer NOT NULL,
    cases_new integer NOT NULL,
    cases_cumulative integer NOT NULL,
    deaths_new integer NOT NULL,
    deaths_cumulative integer NOT NULL,
    date_reported_id integer NOT NULL,
    country_id integer NOT NULL
);
````
````python
class WhoGlobalData(db.Model):
    __tablename__ = 'who_global_data'

    id = db.Column(db.Integer, primary_key=True)
    cases_new = db.Column(db.Integer, nullable=False)
    cases_cumulative = db.Column(db.Integer, nullable=False)
    deaths_new = db.Column(db.Integer, nullable=False)
    deaths_cumulative = db.Column(db.Integer, nullable=False)

    date_reported_id = db.Column(db.Integer, db.ForeignKey('who_date_reported.id'), nullable=False)
    date_reported = db.relationship('WhoDateReported', lazy='joined')

    country_id = db.Column(db.Integer, db.ForeignKey('who_country.id'), nullable=False)
    country = db.relationship('WhoCountry', lazy='joined')
````

#### who_global_data_import
````postgresql
CREATE TABLE public.who_global_data_import (
    id integer NOT NULL,
    date_reported character varying(255) NOT NULL,
    country_code character varying(255) NOT NULL,
    country character varying(255) NOT NULL,
    who_region character varying(255) NOT NULL,
    new_cases character varying(255) NOT NULL,
    cumulative_cases character varying(255) NOT NULL,
    new_deaths character varying(255) NOT NULL,
    cumulative_deaths character varying(255) NOT NULL,
    row_imported boolean NOT NULL
);
````
````python
class WhoGlobalDataImportTable(db.Model):
    __tablename__ = 'who_global_data_import'

    id = db.Column(db.Integer, primary_key=True)
    date_reported = db.Column(db.String(255), nullable=False)
    country_code = db.Column(db.String(255), nullable=False)
    country = db.Column(db.String(255), nullable=False)
    who_region = db.Column(db.String(255), nullable=False)
    new_cases = db.Column(db.String(255), nullable=False)
    cumulative_cases = db.Column(db.String(255), nullable=False)
    new_deaths = db.Column(db.String(255), nullable=False)
    cumulative_deaths = db.Column(db.String(255), nullable=False)
    row_imported = db.Column(db.Boolean, nullable=False)
````


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
* Issue #20 /europe/update: Update DB
* Issue #3 ORM: 3NF for ecdc_europa_data_import
* Issue #4 data update for 3NF ecdc_europa_data_import

### 0.0.10 Release
* Issue #5 Visual Graphs for Data per Countries order by Date


