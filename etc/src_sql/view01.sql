CREATE VIEW view_who_global_data
AS SELECT DISTINCT
    date_reported,
    country_code,
    country,
    new_cases,
    new_deaths,
    cumulative_cases,
    cumulative_deaths
FROM who_global_data
     LEFT JOIN who_country wc ON wc.id = who_global_data.country_id
     LEFT JOIN who_date_reported wdr ON wdr.id = who_global_data.date_reported_id
ORDER BY
    date_reported DESC,
    new_deaths DESC,
    cumulative_deaths DESC,
    new_cases DESC,
    cumulative_cases DESC
LIMIT 500
