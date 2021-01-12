import copy
from datetime import datetime

import pandas as pd
from flask import Blueprint, render_template, request

import config as cfg
from core import my_user
from core import search
from db import query
from db.query import engine

result_page = Blueprint('result_page', __name__, template_folder='templates')

empty_search = {'my_cities': [], "start_date": "", "end_date": "", "celsius_degree": ""}


# get the cities that fit the weather the user want
def get_best_city(my_cities, celsius_degree, start_date, end_date):
    good_cities = []
    for city in my_cities:
        city_id = city[1]
        avg_tmp_city = engine.execute(query.find_if_city_between_temperatures_between_dates,
                                      city_id=city_id,
                                      start_date=start_date,
                                      end_date=end_date,
                                      min_temp=cfg.Weather_type[celsius_degree][1],
                                      max_temp=cfg.Weather_type[celsius_degree][2]).fetchone()
        if avg_tmp_city != None:
            good_cities.append(city)
    return good_cities


def get_temp_by_day(dates_list, city_id):
    list_temp_of_days = []
    for date in dates_list:
        answer = engine.execute(query.get_tem_by_day_per_id_city_avg_and_std, date_user=date,
                                city_id_user=city_id).fetchall()
        list_temp_of_days.append(answer)
    return list_temp_of_days


# dates from start to end
def create_dates_list(start_date, end_date):
    start = datetime.strptime(start_date, "%Y-%m-%d")
    end = datetime.strptime(end_date, "%Y-%m-%d")
    datesList = pd.date_range(start=start, end=end)
    return datesList.strftime("%Y-%m-%d")


# check if the data not None do make the num in formal 0.00 and make tuples to list
def manageData(rainy_and_snowy, temp_by_day):
    for i in range(len(temp_by_day)):
        temp_by_day[i] = list(temp_by_day[i][0])
    rainy_and_snowy = list(rainy_and_snowy[0])
    # count the num of times there is details. if error = 0 there is no details at all
    error = 0
    for i in range(len(temp_by_day)):
        error += (temp_by_day[i].count(None) != len(temp_by_day[i]))
    error += (rainy_and_snowy.count(None) != len(rainy_and_snowy))
    # make to format 0.00
    for i in range(len(rainy_and_snowy)):
        if rainy_and_snowy[i] != None:
            rainy_and_snowy[i] = float("{:.2f}".format(rainy_and_snowy[i]))
    for arr in temp_by_day:
        for i in range(len(arr)):
            if arr[i] != None:
                arr[i] = float("{:.2f}".format(arr[i]))

    return rainy_and_snowy, temp_by_day, error


# decide what is th fit image to describe the weather best
def get_img_by_day(temp_avg, rain_percentage, precipitation_avg, snow_percentage, snow_depth_avg):
    if temp_avg == None:
        return ""
    if snow_percentage != None and snow_percentage > 40:
        if snow_depth_avg == None:
            return "snowy-2.svg"
        if snow_depth_avg > 130:
            return "snowy-3.svg"
        if snow_depth_avg > 60:
            if temp_avg > 35:
                return "snowy-2-sun.svg"
            elif temp_avg > 10:
                return "snowy-2-sun-low.svg"
            else:
                return "snowy-2.svg"
        if snow_depth_avg >= 0:
            if temp_avg > 10:
                return "snowy-1-sun.svg"
    if rain_percentage != None and rain_percentage > 40:
        if precipitation_avg == None:
            return "rainy-2.svg"
        if precipitation_avg > 90:
            return "rainy-3.svg"
        if precipitation_avg > 60:
            if temp_avg > 35:
                return "rainy-2-sun.svg"
            elif temp_avg > 25:
                return "rainy-2-sun-low.svg"
            else:
                return "rainy-2.svg"
        if precipitation_avg >= 0:
            if temp_avg > 25:
                return "rainy-1-sun.svg"
    if temp_avg > 30:
        return "day.svg"
    if temp_avg > 20:
        return "cloudy-day-2.svg"
    if temp_avg > 15:
        return "cloudy-day-3.svg"
    return "cloudy.svg"


def get_img_list(temp_by_day, rainy_and_snowy):
    img_list = []
    rain_percentage = rainy_and_snowy[0]
    precipitation_avg = rainy_and_snowy[1]
    snow_percentage = rainy_and_snowy[2]
    snow_depth_avg = rainy_and_snowy[3]
    for i in range(len(temp_by_day)):
        if temp_by_day[i][0] != None:
            img_list.append(
                "static/image/animated/" + get_img_by_day(temp_by_day[i][0], rain_percentage, precipitation_avg,
                                                          snow_percentage, snow_depth_avg))
        elif temp_by_day[i][2] != None:
            img_list.append(
                "static/image/animated/" + get_img_by_day(temp_by_day[i][2], rain_percentage, precipitation_avg,
                                                          snow_percentage, snow_depth_avg))
        else:
            img_list.append(
                "static/image/animated/" + get_img_by_day(temp_by_day[i][4], rain_percentage, precipitation_avg,
                                                          snow_percentage, snow_depth_avg))
    return img_list


@result_page.route("/results", methods=['POST'])
def results():
    # delete the last search
    my_cities = copy.deepcopy(my_user.currentSearch.get('my_cities'))
    my_user.currentSearch = copy.deepcopy(empty_search)

    start_date = request.form["start_date"]
    end_date = request.form["end_date"]

    # check is this is a state that the user need to choose from a list of country
    if len(my_cities) == 0:
        try:
            city_id = request.form["city_id"]
            city_name = request.form["city_name"]
        except:
            return search.start_new_search()
    else:
        # get the search from the search details
        city_id = my_cities[0][1]
        city_name = my_cities[0][0]
    # need to see if the cities fit the weather
    if (len(my_cities) > 1):
        celsius_degree = int(request.form["celsius_degree"])
        good_cities = get_best_city(my_cities, celsius_degree, start_date, end_date)
        # no country fit
        if (good_cities == []):
            return render_template('result_style.html', state=0)
        # there is some countries that fit - user need to choose
        elif len(good_cities) > 1:
            return render_template('chooseOneCity.html', state=-1, good_cities=good_cities, start_date=start_date,
                                   end_date=end_date)
        else:
            # thre is only one city that fit - excellent
            city_id = good_cities[0][1]
            city_name = good_cities[0][0]

    # save the search in the last searches - sql query
    now = datetime.now();
    engine.execute(query.insert_search_sql, user_id=my_user.userID, city_id=city_id, start_date=start_date,
                   end_date=end_date, search_time=now)
    year, month, date = start_date.split('-')

    # get the inormation from the data base
    datesList = create_dates_list(start_date, end_date)
    rainy_and_snowy = engine.execute(query.get_percentage_of_rainy_and_snowy_days_per_month, city_id=city_id,
                                     selected_month=month).fetchall()
    temp_by_day = get_temp_by_day(datesList, city_id)

    # analyze the data
    rainy_and_snowy, temp_by_day, error = manageData(rainy_and_snowy, temp_by_day)
    weather_img = get_img_list(temp_by_day, rainy_and_snowy)

    return render_template('result_style.html', city_name=city_name, state=error, dates=datesList,
                           rainy_and_snowy=rainy_and_snowy, temp_by_day=temp_by_day, weather_img=weather_img)
