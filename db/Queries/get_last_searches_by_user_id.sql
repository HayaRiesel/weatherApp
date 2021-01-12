SELECT city_id, start_date, end_date
FROM weathertrip.searches
WHERE user_id = :user_id
ORDER BY time DESC
LIMIT 5;