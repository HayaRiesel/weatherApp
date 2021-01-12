SELECT (COUNT(DISTINCT CASE WHEN precipitation > 0 THEN date END) / COUNT(DISTINCT date)) * 100
as "percentage_of_rainy_days",
SUM(precipitation) / COUNT(*) as "average_precipitation_per_day",
(COUNT(DISTINCT CASE WHEN snow_depth > 0 THEN date END) / COUNT(DISTINCT date)) * 100
as "percentage_of_snowy_days",
SUM(snow_depth) / COUNT(*) as "average_snow_depth_per_day"
FROM weathertrip.weather
WHERE station_id in (SELECT station_id
	FROM weathertrip.stations
    WHERE city_id = :city_id)
    and month(date) = :selected_month;