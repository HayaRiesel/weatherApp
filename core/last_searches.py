import copy

from flask import Blueprint, render_template, request

from core import my_user
from db import query
from db.query import engine

last_searches_page = Blueprint('last_searches_page', __name__, template_folder='templates')

empty_search = {'my_cities': [], "start_date": "", "end_date": "", "celsius_degree": ""}
saved_search = []


@last_searches_page.route("/search_show_last_search")
def search_show_last_search():
    global saved_search
    # query - returm 5 last search by userID
    saved_search = engine.execute(query.get_last_searches_by_user_id_sql, user_id=my_user.userID).fetchall()
    # analyze the searches that return from the query
    for i in range(len(saved_search)):
        # make them to list
        saved_search[i] = list(saved_search[i])
        # check the city namr
        city_name = engine.execute(query.get_city_name_by_id, id=saved_search[i][0]).fetchone()[0]
        city_id = saved_search[i][0]
        # save to know the choice the user will choose by index
        saved_search[i][0] = [city_name, city_id]
    return render_template('last_search.html', len_last_search=len(saved_search), last_search=saved_search)


@last_searches_page.route('/choose_prev_search', methods=['POST'])
def choose_prev_search():
    global saved_search
    search_index = request.form['search_index']
    my_search = saved_search[int(search_index)]
    # make sure to delete the last search
    cities_to_choose = []
    my_user.currentSearch = copy.deepcopy(empty_search)
    # get the info of the search
    city_id = my_search[0][1]
    city_name = my_search[0][0]
    my_user.currentSearch.get('my_cities').append([city_name, city_id])
    my_user.currentSearch['start_date'] = my_search[1]
    my_user.currentSearch['end_date'] = my_search[2]
    return render_template('search_submit_date.html', len=len(cities_to_choose), cities=cities_to_choose,
                           mySearch=my_user.currentSearch)
