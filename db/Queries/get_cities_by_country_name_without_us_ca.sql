SELECT city_name, city_id
FROM weathertrip.cities
WHERE country_ex_id = (SELECT country_id
	FROM weathertrip.countries
	WHERE country_name = :country_name)
ORDER BY city_name;