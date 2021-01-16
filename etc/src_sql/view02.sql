select date_reported as my_date from who_global_data_import group by date_reported order by date_reported desc ;

select distinct d.date_reported as my_date from who_global_data as i left join who_date_reported as d on i.date_reported_id=d.id order by d.date_reported desc ;

select * from who_global_data where date_reported_id = 226 order by country_id;

delete from who_global_data where date_reported_id = 226;
delete from who_global_data where date_reported_id = 284;






