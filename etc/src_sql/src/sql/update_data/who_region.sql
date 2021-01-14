select distinct
    who_region
from
    who_global_data_import
where
    who_global_data_import.WHO_region NOT IN (
        select who_region from who_region
    ) order by who_global_data_import.WHO_region