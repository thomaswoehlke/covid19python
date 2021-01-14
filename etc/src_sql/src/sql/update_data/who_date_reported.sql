insert into
    who_date_reported (
        date_reported
    )
select distinct
    who_global_data_import.Date_reported as date_reported
from
    who_date_reported,
    who_global_data_import
where
    who_global_data_import.Date_reported NOT IN (
        select who_date_reported.date_reported from who_date_reported
    )