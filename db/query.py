import sqlalchemy
from sqlalchemy import create_engine
import config as cfg


engine = create_engine('mysql+pymysql://'+cfg.mysql['user'] +':'+cfg.mysql['password']+'@'+ cfg.mysql['host']+'/'+cfg.mysql['db'])

con = engine.connect()
script = open('db/Queries/insert_new_user.sql', 'r')
insert_new_user_sql = sqlalchemy.text(script.read())
script.close()
# a = engine.execute(insert_new_user_sql, num='1').fetchall()

script = open('db/Queries/get_user_by_id_and_pass.sql', 'r')
get_user_by_id_and_pass_sql = sqlalchemy.text(script.read())
# a = engine.execute(get_user_by_id_and_pass_sql, num='1').fetchall()
script.close()

script = open('db/Queries/get_user_by_id_and_pass.sql', 'r')
get_user_by_id_and_pass_sql = sqlalchemy.text(script.read())
script.close()
# a = engine.execute(get_user_by_id_and_pass_sql, num='1').fetchall()

script = open('db/Queries/insert_search.sql', 'r')
insert_search_sql = sqlalchemy.text(script.read())
script.close()
# engine.execute(insert_search_sql, num='1').fetchall()

script = open('db/Queries/get_last_searches_by_user_id.sql', 'r')
get_last_searches_by_user_id_sql = sqlalchemy.text(script.read())
script.close()
# a = engine.execute(get_last_searches_by_user_id_sql, num='1').fetchall()

script = open('db/Queries/get_city_name_by_id.sql', 'r')
get_city_name_by_id = sqlalchemy.text(script.read())
script.close()
# a = engine.execute(get_city_name_by_id, num='1').fetchall()

script = open('db/Queries/get_cities_by_country_name_for_us_ca.sql', 'r')
get_cities_by_country_name_for_us_ca = sqlalchemy.text(script.read())
script.close()
# a = engine.execute(get_cities_by_country_name_for_us_ca, num='1').fetchall()

script = open('db/Queries/get_cities_by_country_name_without_us_ca.sql', 'r')
get_cities_by_country_name_without_us_ca = sqlalchemy.text(script.read())
script.close()
# a = engine.execute(get_cities_by_country_name_without_us_ca, num='1').fetchall()

script = open('db/Queries/get_us_ca_internal_countries_by_external_country_name.sql', 'r')
get_us_ca_internal_countries_by_external_country_name = sqlalchemy.text(script.read())
script.close()
# a = engine.execute(get_cities_by_country_name_without_us_ca, num='1').fetchall()

script = open('db/Queries/get_percentage_of_rainy_and_snowy_days_per_month.sql', 'r')
get_percentage_of_rainy_and_snowy_days_per_month = sqlalchemy.text(script.read())
script.close()

script = open('db/Queries/get_tem_by_day_per_id_city_avg_and_std.sql', 'r')
get_tem_by_day_per_id_city_avg_and_std = sqlalchemy.text(script.read())
script.close()

script = open('db/Queries/find_if_city_between_temperatures_between_dates.sql', 'r')
find_if_city_between_temperatures_between_dates = sqlalchemy.text(script.read())
script.close()

script = open('db/Queries/get_cities_by_city_name.sql', 'r')
get_cities_by_city_name = sqlalchemy.text(script.read())
script.close()
