INSERT INTO weathertrip.searches
values(:user_id, :city_id, :start_date, :end_date, :search_time)
ON DUPLICATE KEY UPDATE time = :search_time;