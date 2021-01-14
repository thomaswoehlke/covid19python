insert into who_country(
    country_code,
    country,
    who_region_id
)
select distinct
    country_code,
    country,
    who_region.id as who_region_id
from
    who_global_data_import,
    who_region
where
    (country_code) NOT IN (
        select country_code from who_country
    )