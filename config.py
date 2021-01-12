
import configparser
my_config_parser = configparser.SafeConfigParser()
my_config_parser.read('config.ini')


mysql = {
    "host": my_config_parser.get('DEFAULT','sql_host'),
    "user": my_config_parser.get('DEFAULT','sql_user'),
    "password": my_config_parser.get('DEFAULT','sql_password'),
    "db": my_config_parser.get('DEFAULT','sql_db')
}

port = my_config_parser.get('DEFAULT','port')
host = my_config_parser.get('DEFAULT','host')


Weather_type = [
    #temp declare,min,max
    ["hot",my_config_parser.get('DEFAULT','weather_type_min_hot'),my_config_parser.get('DEFAULT','weather_type_max_hot')], #1
    ["nice",my_config_parser.get('DEFAULT','weather_type_min_nice'),my_config_parser.get('DEFAULT','weather_type_max_nice')], #2
    ["cold",my_config_parser.get('DEFAULT','weather_type_min_cold'),my_config_parser.get('DEFAULT','weather_type_max_cold')] #3
]
