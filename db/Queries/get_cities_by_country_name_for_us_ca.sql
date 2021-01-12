SELECT city_name, city_id
FROM weathertrip.cities
WHERE country_in_id = (SELECT id_internal_country
	FROM weathertrip.us_ca_country
	WHERE internal_country_name = :country_name)
ORDER BY city_name;