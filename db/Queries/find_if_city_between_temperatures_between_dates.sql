SELECT avg(avg_temperature)
FROM weathertrip.weather 
WHERE station_id in (SELECT station_id
	FROM weathertrip.stations
    WHERE city_id = :city_id)
	and DayOfYear(date) BETWEEN DayOfYear(:start_date) and DayOfYear(:end_date)
HAVING avg(avg_temperature) BETWEEN :min_temp*10 and :max_temp*10;