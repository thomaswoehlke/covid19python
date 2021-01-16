select date_reported as my_date from who_global_data_import group by date_reported not in (
select distinct d.date_reported as my_date from who_global_data as i left join who_date_reported as d on i.date_reported_id=d.id
) order by date_reported desc;
