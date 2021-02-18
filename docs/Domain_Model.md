# Domain Model

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
class WhoData(db.Model):
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
class OwidImport(db.Model):
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
