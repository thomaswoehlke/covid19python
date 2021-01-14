CREATE TABLE who_Date_reported (
   id SERIAL PRIMARY KEY,
   date_reported VARCHAR(255) NOT NULL,
   UNIQUE (date_reported)
);