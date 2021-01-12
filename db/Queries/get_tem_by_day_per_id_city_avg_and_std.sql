SELECT avg(avg_temperature)/10, std(avg_temperature)/10, avg(max_temperature)/10, std(max_temperature)/10, avg(min_temperature)/10, std(min_temperature)/10 FROM weathertrip.weather
where station_id  in (select station_id from weathertrip.stations where city_id = :city_id_user)
and month(date) = month(:date_user) and day(date) = day(:date_user);


