CREATE TABLE who_global_data (
     id SERIAL PRIMARY KEY,
     date_reported_id integer REFERENCES who_Date_reported,
     country_id integer REFERENCES who_country,
     new_cases integer NOT NULL,
     cumulative_cases integer NOT NULL,
     new_deaths integer NOT NULL,
     cumulative_deaths integer
);