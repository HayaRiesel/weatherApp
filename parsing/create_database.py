import glob
import pandas as pd
from sqlalchemy import create_engine


def fill_table(engine, csv_path, table_name):
    # Replace Excel_file_name with your excel sheet name
    df = pd.read_csv(csv_path, sep=',', quotechar='\'', encoding='utf8')
    # Replace Table_name with your sql table name
    df.to_sql(table_name, con=engine, index=False, if_exists='append')
    print("finish fill " + table_name + " table\n")


def insert_weather(engine):
    csv_files = glob.glob("year_filter/*.csv")
    for file in csv_files:
        chunk_size = 100000
        count = 0
        for chunk in pd.read_csv(file, chunksize=chunk_size, sep=',', encoding='utf8'):
            chunk.to_sql('weather', con=engine, index=False, if_exists='append')
            print(count)
            count += 1
        print("DONE " + file)


def create_tables(engine):
    countries_table = "CREATE TABLE `countries` (`country_id` varchar(2) NOT NULL,`country_name` varchar(100) NOT " \
                      "NULL,PRIMARY KEY (`country_id`),UNIQUE KEY `country_id_UNIQUE` (`country_id`),UNIQUE KEY " \
                      "`country_name_UNIQUE` (`country_name`)) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 " \
                      "COLLATE=utf8mb4_0900_ai_ci"
    engine.execute(countries_table)

    us_ca_country_table = "CREATE TABLE `us_ca_country` (`id_external_country` varchar(2) NOT NULL," \
                          "`id_internal_country` varchar(2) NOT NULL,`internal_country_name` varchar(100) NOT NULL," \
                          "PRIMARY KEY (`id_internal_country`,`id_external_country`)," \
                          "KEY `internal_country_name_INDEX` (`internal_country_name`)," \
                          "KEY `id_external_country_FK_idx` (`id_external_country`),CONSTRAINT " \
                          "`id_external_country_FK` FOREIGN KEY (`id_external_country`) REFERENCES `countries` (" \
                          "`country_id`)) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci"
    engine.execute(us_ca_country_table)

    cities_table = "CREATE TABLE `cities` (`city_id` smallint NOT NULL,`country_ex_id` varchar(2) NOT NULL," \
                   "`country_in_id` varchar(2) DEFAULT NULL,`city_name` varchar(45) NOT NULL,PRIMARY KEY (`city_id`)," \
                   "UNIQUE KEY `city_id_UNIQUE` (`city_id`),KEY `country_ex_id_INDEX` (`country_ex_id`)," \
                   "KEY `country_in_id_INDEX` (`country_in_id`),CONSTRAINT `country_ex_id_FK` FOREIGN KEY (" \
                   "`country_ex_id`) REFERENCES `countries` (`country_id`),CONSTRAINT `country_in_id_FK` FOREIGN KEY " \
                   "(`country_in_id`) REFERENCES `us_ca_country` (`id_internal_country`)) ENGINE=InnoDB DEFAULT " \
                   "CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci"
    engine.execute(cities_table)

    stations_table = "CREATE TABLE `stations` (`station_id` varchar(12) NOT NULL,`city_id` smallint NOT NULL," \
                     "PRIMARY KEY (`station_id`),UNIQUE KEY `station_id_UNIQUE` (`station_id`),KEY `city_id_INDEX` (" \
                     "`city_id`),CONSTRAINT `city_id_FK` FOREIGN KEY (`city_id`) REFERENCES `cities` (`city_id`)) " \
                     "ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci"
    engine.execute(stations_table)

    weather_table = "CREATE TABLE `weather` (`station_id` varchar(12) NOT NULL,`date` date NOT NULL,`avg_temperature` " \
                    "smallint DEFAULT NULL,`max_temperature` smallint DEFAULT NULL,`min_temperature` smallint DEFAULT " \
                    "NULL,`snowfall` smallint DEFAULT NULL,`snow_depth` int DEFAULT NULL,`precipitation` smallint " \
                    "DEFAULT NULL,PRIMARY KEY (`station_id`,`date`),CONSTRAINT `station_id_FK` FOREIGN KEY (" \
                    "`station_id`) REFERENCES `stations` (`station_id`)) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 " \
                    "COLLATE=utf8mb4_0900_ai_ci"
    engine.execute(weather_table)

    users_table = "CREATE TABLE `users` (`user_id` varchar(15) NOT NULL,`password` varchar(16) NOT NULL,PRIMARY KEY (" \
                  "`user_id`),UNIQUE KEY `user_id_UNIQUE` (`user_id`)) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 " \
                  "COLLATE=utf8mb4_0900_ai_ci"
    engine.execute(users_table)

    searches_table = "CREATE TABLE `searches` (`user_id` varchar(15) NOT NULL,`city_id` smallint NOT NULL," \
                     "`start_date` date NOT NULL,`end_date` date NOT NULL,`time` datetime NOT NULL,PRIMARY KEY (" \
                     "`user_id`,`city_id`,`start_date`,`end_date`),KEY `city_id_FK_idx` (`city_id`),CONSTRAINT " \
                     "`city_FK` FOREIGN KEY (`city_id`) REFERENCES `cities` (`city_id`),CONSTRAINT `user_id_FK` " \
                     "FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`)) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 " \
                     "COLLATE=utf8mb4_0900_ai_ci"
    engine.execute(searches_table)


def main():
    # Enter your password and database names here
    engine = create_engine('mysql+pymysql://user:password@host:port/weathertrip')
    # Create tables
    create_tables(engine)
    # Fill tables
    fill_table(engine, "upload\\country.csv", 'countries')
    fill_table(engine, "upload\\usCa.csv", 'us_ca_country')
    fill_table(engine, "upload\\city.csv", 'cities')
    fill_table(engine, "upload\\stations.csv", 'stations')
    insert_weather(engine)


if __name__ == "__main__":
    main()
