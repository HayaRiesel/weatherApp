import copy

from flask import Blueprint, render_template, request

from core import my_user
from db import query
from db.query import engine

login_page = Blueprint('login_page', __name__, template_folder='templates')


@login_page.route("/login", methods=['POST'])
def log():
    user_name = request.form['username']
    sur_name = request.form['password']
    email = request.form['email']
    state = request.form['state']
    answer = engine.execute(query.get_user_by_id_and_pass_sql, id=user_name, email=email).fetchone()
    # create new user
    if state == "sign":
        # check if the user excist
        if answer != None:
            return render_template('login.html', wrongTry=3)
        engine.execute(query.insert_new_user_sql, nameid=user_name, pas=sur_name, email=email)
    if state == "log":
        # check if the user id not exist
        if answer == None:
            return render_template('login.html', wrongTry=1)
        # check if the password fit
        if answer[0] != sur_name:
            return render_template('login.html', wrongTry=2)
    my_user.userID = user_name
    my_user.currentSearch = copy.deepcopy(my_user.empty_search)
    my_user.cities_to_choose = []
    return render_template('search.html', len=0, cities=[], mySearch=my_user.currentSearch)
