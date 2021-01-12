import csv
import glob


def filter_file():
    dict_city_countery_ex = {}
    dict_country_id = {}
    # open file
    extennal_city = open("worldcities.csv", "r")
    station_names = open("station_names.csv", "r")

    country_id = open("upload\\country.csv", "r")
    country_id_reader = csv.reader(country_id)
    for row in country_id_reader:
        dict_country_id[row[0]] = (row[1].lower())
    country_id.close()

    country_id = open("upload\\usCa.csv", "r")
    country_id_reader = csv.reader(country_id)
    for row in country_id_reader:
        key = "*"+row[1]
        dict_country_id[key] = (row[1].lower())
    country_id.close()

    wtite_station_with_city = open("station_with_city.csv", "w")
    wtite_station_with_city_writer = csv.writer(wtite_station_with_city, lineterminator='\n')
    station_names_reader = csv.reader(station_names)
    extennal_city_reader = csv.reader(extennal_city)
    a = extennal_city_reader
    for row in extennal_city_reader:
        row[0] = row[0].lower()
        row[1] = row[1].lower()
        dict_city_countery_ex[row[0]] = row[1]
    for row in station_names_reader:
        station_name = row[4].lower()
        if row[0] == 'UPM00034622' or row[0] == 'BY000064397':
            x = 1
        for city_ex, country_ex in dict_city_countery_ex.items():
            country_id = row[1]
            country = dict_country_id[row[1]]
            if city_ex == "sioux falls":
                x = 1
            if row[2] is not "0":
                country_id = row[2]
                station_name = row[4][3:].lower()
                country = dict_country_id["*"+country_id]
            if station_name.startswith(city_ex + " ") or station_name == city_ex:
                if country == country_ex or country_ex == "" or dict_country_id[row[1]] == country_ex:
                    row = [row[0], row[1],row[2], city_ex, row[3], station_name]
                    print(row)
                    wtite_station_with_city_writer.writerow(row)
                break
    wtite_station_with_city.close()
    extennal_city.close()
    station_names.close()


def main():
    filter_file()


if __name__ == "__main__":
    main()
