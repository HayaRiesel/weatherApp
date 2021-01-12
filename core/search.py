import copy

from flask import Blueprint, render_template
from flask import request

from core import my_user
from db import query
from db.query import engine

search_page = Blueprint('search_page', __name__, template_folder='templates')
cities_to_choose = []
empty_search = {'my_cities': [], "start_date": "", "end_date": "", "celsius_degree": ""}


def get_cities_of_country(country):
    # check if the country is us or ca - because id diffrent behavior
    us_ca = 0
    answer = engine.execute(query.get_cities_by_country_name_without_us_ca, country_name=country).fetchall()
    # if there is no result continue looking
    if answer == []:
        answer = engine.execute(query.get_cities_by_country_name_for_us_ca, country_name=country).fetchall()
    if answer == []:
        answer = engine.execute(query.get_cities_by_city_name, city_name=country).fetchall()
    if answer == []:
        answer = engine.execute(query.get_us_ca_internal_countries_by_external_country_name,
                                country_name=country).fetchall()
        us_ca = 1
    if answer == []:
        us_ca = 0
        return [], us_ca
    # analyze the answer from tuples to array
    for i in range(len(answer)):
        answer[i] = list(answer[i])

    if len(answer) > 1000:
        return [], us_ca
    return answer, us_ca


def search_and_show_cities(city_name):
    global cities_to_choose
    currentSearch = my_user.currentSearch
    country = city_name
    # query -  check all the city id belongs to the searh
    cities_to_choose, us_ca = get_cities_of_country(country)
    if us_ca == 1:
        # -2 is the state send to the html
        return render_template('search.html', len=-2, cities=[], mySearch=currentSearch)
    if cities_to_choose == []:
        # -1 is the state send to the html
        return render_template('search.html', len=-1, cities=[], mySearch=currentSearch)
    # remove cities that already choosed
    cities_to_choose = [x for x in cities_to_choose if [x[0], x[1]] not in currentSearch['my_cities']]
    if cities_to_choose == []:
        # -1 is the state send to the html
        return render_template('search.html', len=-1, cities=[], mySearch=currentSearch)
    return render_template('search.html', len=len(cities_to_choose), cities=cities_to_choose,
                           mySearch=currentSearch)


def choose_city(city_id, city_name):
    global cities_to_choose
    currentSearch = my_user.currentSearch
    # remove from the list of thecities in the search
    for city in cities_to_choose:
        if (city[1] == city_id):
            cities_to_choose.remove(city)
    # add to the currentcitie that the user choose
    currentSearch.get('my_cities').append([city_name, city_id])
    if (len(currentSearch.get('my_cities')) == 5):
        cities_to_choose = []


def remove_city(city_id):
    currentSearch = my_user.currentSearch
    # remove the city from the list
    for city in currentSearch.get('my_cities'):
        if city[1] == city_id:
            currentSearch.get('my_cities').remove(city)


@search_page.route("/search", methods=['POST'])
def do_search():
    global cities_to_choose
    currentSearch = my_user.currentSearch
    current_action = request.form['action']
    # handkle by the state that send from the http
    if current_action == "search_and_show_cities":
        city_name = request.form['city_name']
        return search_and_show_cities(city_name)
    elif current_action == "close_searches_windows":
        cities_to_choose = []
        return render_template('search.html', len=len(cities_to_choose), cities=cities_to_choose,
                               mySearch=currentSearch)
    city_id = int(request.form['city_id'])
    city_name = engine.execute(query.get_city_name_by_id, id=city_id).fetchone()[0]
    if current_action == "choose_city":
        choose_city(city_id, city_name)
    elif current_action == "remove_city":
        remove_city(city_id)
    return render_template('search.html', len=len(cities_to_choose), cities=cities_to_choose, mySearch=currentSearch)


@search_page.route("/search_submit_date", methods=['GET'])
def submit_date():
    currentSearch = my_user.currentSearch
    return render_template('search_submit_date.html', len=0, cities=[], mySearch=currentSearch)


@search_page.route('/start_new_search')
def start_new_search():
    global cities_to_choose
    # delete previous information becouse it is new seach
    cities_to_choose = []
    my_user.currentSearch = copy.deepcopy(my_user.empty_search)
    return render_template('search.html', len=0, cities=[], mySearch=my_user.currentSearch)
