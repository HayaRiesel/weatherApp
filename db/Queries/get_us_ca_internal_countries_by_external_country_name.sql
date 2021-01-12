SELECT internal_country_name, id_internal_country
FROM weathertrip.us_ca_country
WHERE id_external_country = (SELECT country_id
	FROM weathertrip.countries
    WHERE country_name = :country_name);