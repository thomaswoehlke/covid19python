INSERT INTO who_global_data_import( 
Date_reported, 
Country_code, 
Country, 
WHO_region, 
New_cases, 
Cumulative_cases, 
New_deaths, 
Cumulative_deaths
) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
RETURNING id