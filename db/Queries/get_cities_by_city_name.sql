SELECT weathertrip.cities.city_name, weathertrip.cities.city_id,weathertrip.countries.country_name,weathertrip.us_ca_country.internal_country_name
FROM weathertrip.cities
    LEFT JOIN weathertrip.countries
        ON weathertrip.countries.country_id=weathertrip.cities.country_ex_id
    LEFT JOIN weathertrip.us_ca_country
        ON weathertrip.us_ca_country.id_internal_country=weathertrip.cities.country_in_id
WHERE city_name = :city_name;
