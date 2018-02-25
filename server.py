import datetime
import json
import os
import re
import psycopg2 as dbapi2

from flask import Flask, url_for
from flask import render_template
from flask import redirect
from flask import request, session, flash
from uwp import UWP
from PowerBoat import PowerBoat

from Polo_Store import Polo_Store
from diving import Diver
from diving import Competition
from diving import Record
from diving import DiverStore
from users import Users
from spear_fishing import Spear_fishing

app = Flask(__name__)

def get_elephantsql_dsn(vcap_services):
    """Returns the data source name for ElephantSQL."""
    parsed = json.loads(vcap_services)
    uri = parsed["elephantsql"][0]["credentials"]["uri"]
    match = re.match('postgres://(.*?):(.*?)@(.*?)(:(\d+))?/(.*)', uri)
    user, password, host, _, port, dbname = match.groups()
    dsn = """user='{}' password='{}' host='{}' port={}
             dbname='{}'""".format(user, password, host, port, dbname)
    return dsn

@app.route('/')
def home():
    return render_template('home.html')

######################  Power Boat Racing  functions #################
# all of the class functions are taken from PowerBoat.py file

@app.route('/oper2powerboat',methods=['GET', 'POST'])
def oper2powerboat():
    dsn = app.config['dsn']
    page = PowerBoat(dsn)
    if request.method == 'GET':
        return page.disp_second()
    elif 'Join1' in request.form:
        return page.join1()
    elif 'Join2' in request.form:
        return page.join2()
    elif 'LJoin' in request.form:
        return page.Ljoin()
    elif 'RJoin' in request.form:
        return page.Rjoin()
    elif 'FJoin' in request.form:
        return page.Fjoin()
    elif 'Union' in request.form:
        return page.union()
    elif 'Intersect' in request.form:
        return page.intersect()
    elif 'Minus' in request.form:
        return page.minus()
    elif 'Best' in request.form:
        return page.best()
    ###################
    # this place will go on
    ###################


# for initialization
@app.route('/initPowerBoat')
def table_init():
    dsn=app.config['dsn']
    page = PowerBoat(dsn)
    return page.initdb()

# /drivers route
# Power Boat Anasayfası burada
@app.route('/drivers',methods=['GET', 'POST'])
def power_boat():
    dsn=app.config['dsn']
    page = PowerBoat(dsn)

    if request.method == 'GET':
        return page.show_all()  # change is made here
    elif 'Add' in request.form:
        name = request.form['name']
        team = request.form['team']
        boat = request.form['boat']
        table = request.form['table']
        return page.add(name ,team , boat ,table)
    elif 'Delete' in request.form:
        id = request.form['select']
        table = request.form['table']
        return page.delete(id ,table)
    elif 'Update' in request.form:
        id = request.form['select']
        name = request.form['name']
        team = request.form['team']
        boat = request.form['boat']
        table = request.form['table']
        return page.update(id,name,team,boat,table)
    elif 'Reset' in request.form:
        table = request.form['table']
        return page.reset_driver()

# for /teams route
@app.route('/teams',methods=['GET', 'POST'])
def show_teams():
    dsn=app.config['dsn']
    page = PowerBoat(dsn)
    if request.method == 'GET':
        return page.show_teams()

# for /boats route
@app.route('/boats',methods=['GET', 'POST'])
def show_boats():
    dsn=app.config['dsn']
    page = PowerBoat(dsn)
    if request.method == 'GET':
        return page.show_boats()

# for /league15 route
@app.route('/league15',methods=['GET', 'POST'])
def show_league15():
    dsn=app.config['dsn']
    page = PowerBoat(dsn)
    if request.method == 'GET':
        return page.show_league15()

# for /oldraces route
@app.route('/oldraces',methods=['GET', 'POST'])
def show_oldraces():
    dsn=app.config['dsn']
    page = PowerBoat(dsn)
    if request.method == 'GET':
        return page.show_oldraces()


#################  end of Power Boat Racing Functions ###########

@app.route('/users', methods=['GET', 'POST'])
def users():
    dsn = app.config['dsn']
    page = Users(dsn)
    if session['admin']:
        if request.method == 'GET':
            return page.show_users()
        elif 'Add' in request.form:
            username = request.form['UserName']
            password = request.form['Password']
            type = request.form['UserType']
            if username and password and type:
                return page.add_user_from_table(username, password, type)
            else:
                flash("You need to enter all the fields")
                return page.show_users()
        elif 'Delete' in request.form:
            id = request.form.get('select', '')
            if id:
                return page.delete_user(id)
            else:
                flash("You need to select the user you want to delete using the radio buttons!")
                return page.show_users()
        elif 'Update' in request.form:
            id = request.form.get('select', '')
            username = request.form['UserName']
            password = request.form['Password']
            type = request.form['UserType']
            if username and password and type and id:
                return page.update_user(username, password, type, id)
            else:
                if not id:
                    flash("You need to select the user you want to update using the radio buttons!")
                if not username or not password or not type:
                    flash("You need to enter all the fields")
                return page.show_users()
        elif 'Reset' in request.form:
            return page.reset_table()

    else:
        flash("Only admins can access that page!")
        return redirect(url_for('home'))

@app.route('/logout', methods=['GET'])
def logout():
    flash("Logged out!")
    session.pop('username', None)
    session.pop('admin', None)
    return redirect(url_for('home'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    dsn = app.config['dsn']
    page = Users(dsn)
    if request.method == 'GET':
        return render_template('user/login.html')
    else:
        username = request.form['username']
        password = request.form['password']
        return page.login(username, password)


@app.route('/signup', methods=['GET', 'POST'])
def sign_up():
    dsn = app.config['dsn']
    page = Users(dsn)
    if request.method == 'GET':
        return render_template('user/signup.html')
    else:
        username = request.form['username']
        password = request.form['password']
        if username and password:
            return page.sign_up(username, password)
        else:
            flash("You must enter a username and a password!")
            return render_template('user/signup.html')

@app.route('/underwater_photography', methods=['GET', 'POST'])
def uwp():
    return redirect(url_for('uwp_comp'))

@app.route('/underwater_photography/competitors', methods=['GET', 'POST'])
def uwp_comp():
    dsn = app.config['dsn']
    page = UWP(dsn)
    if request.method == 'GET':
        return page.show_page_comp()
    elif 'Add' in request.form:
        name = request.form['Name']
        surname = request.form['Surname']
        country = request.form['Country']
        role = request.form['Role']
        if name and surname:
            return page.add_competitor(name, surname, country, role)
        else:
            flash("You need to enter a name and a surname!")
            return page.show_page_comp()
    elif 'Delete' in request.form:
        id = request.form.get('select', '')
        if id:
            return page.delete_competitor(id)
        else:
            flash("You need to select the competitor you want to delete using the radio buttons!")
            return page.show_page_comp()

    elif 'Update' in request.form:
        id = request.form.get('select', '')
        name = request.form['Name']
        surname = request.form['Surname']
        country = request.form['Country']
        role = request.form['Role']
        if id and name and surname:
            return page.update_competitor(name, surname, country, role, id)
        else:
            if not id:
                flash("You need to select the competitor you want to update using the radio buttons!")
            if not name or not surname:
                flash("You need to enter a name and a surname!")
            return page.show_page_comp()
    elif 'Reset' in request.form:
        return page.reset_table()

@app.route('/underwater_photography/teams', methods=['GET', 'POST'])
def uwp_team():
    dsn = app.config['dsn']
    page = UWP(dsn)
    if request.method == 'GET':
        return page.show_page_team()
    elif 'Add' in request.form:
        country = request.form['Country']
        if country:
            return page.add_team(country)
        else:
            flash("You need to enter a country name!")
            return page.show_page_team()
    elif 'Delete' in request.form:
        id = request.form.get('select', '')
        if id:
            return page.delete_team(id)
        else:
            flash("You need to select the team you want to delete using the radio buttons!")
            return page.show_page_team()
    elif 'Update' in request.form:
        id = request.form.get('select', '')
        country = request.form['Country']
        if country and id:
            return page.update_team(country, id)
        else:
            if not id:
                flash("You need to select the team you want to update using the radio buttons!")
            if not country:
                flash("You need to enter a country name!")
            return page.show_page_team()

############### End of Underwater Photography Functions ##############

@app.route('/diving', methods=['GET', 'POST'])
def diving():
    ds = DiverStore(app.config['dsn'])

    if request.method == 'GET':
        return ds.firstrun()
    else:
        if 'add1' in request.form:
            diverID = request.form['id']
            name = request.form['name']
            age = request.form['age']
            country = request.form['country']
            return ds.add_diver(Diver(diverID, name, age, country), 1)
        elif 'add2' in request.form:
            competitionID = request.form['competitionID']
            winnerID = request.form['winnerID']
            year = request.form['year']
            return ds.add_diver(Competition(competitionID, winnerID, year), 2)
        elif 'add3' in request.form:
            competitionID = request.form['competitionID']
            diverID = request.form['diverID']
            record = request.form['record']
            return ds.add_diver(Record(competitionID, diverID, record), 3)


        elif 'update1' in request.form:
            diverID = request.form['id']
            name = request.form['name']
            age = request.form['age']
            country = request.form['country']
            searchID = request.form['select']
            return ds.update_diver(Diver(diverID, name, age, country), searchID, 1)
        elif 'update2' in request.form:
            competitionID = request.form['competitionID']
            winnerID = request.form['winnerID']
            year = request.form['year']
            searchID = request.form['select']
            return ds.update_diver(Competition(competitionID, winnerID, year), searchID, 2)
        elif 'update3' in request.form:
            competitionID = request.form['competitionID']
            diverID = request.form['diverID']
            record = request.form['record']
            combinedSearchID = request.form['select']
            return ds.update_diver(Record(competitionID, diverID, record), combinedSearchID, 3)


        elif 'find1' in request.form:
            diverID = request.form['id']
            name = request.form['name']
            age = request.form['age']
            country = request.form['country']
            return ds.find_diver(Diver(diverID, name, age, country), 1)
        elif 'find2' in request.form:
            competitionID = request.form['competitionID']
            winnerID = request.form['winnerID']
            year = request.form['year']
            return ds.find_diver(Competition(competitionID, winnerID, year), 2)
        elif 'find3' in request.form:
            competitionID = request.form['competitionID']
            diverID = request.form['diverID']
            record = request.form['record']
            return ds.find_diver(Record(competitionID, diverID, record), 3)


        elif 'recreate' in request.form:
            #  create new tables and add some rows
            ds.recreate()
            return redirect(url_for('diving'))
        elif 'return' in request.form:
            #  return to main diving page
             return redirect(url_for('diving'))


############### End of Diving ##############




@app.route('/Water_Polo', methods=['GET', 'POST'])
def Water_Polo():
    dsn = app.config['dsn']
    page = Polo_Store(dsn)
    with dbapi2.connect(dsn) as connection:
            cursor = connection.cursor()

    if request.method == 'GET':
        return page.show_water_polo_page()

####### Add,Delete and Update for PLayers #############

    elif 'Add_Player' in request.form:
        Name = request.form['name']
        Surname = request.form['surname']
        Position = request.form['position']
        Goals = request.form['goals']
        Assists = request.form['assists']
        team= request.form['team']

        query = "SELECT team_name FROM water_polo_team"
        cursor.execute(query)
        teams = cursor.fetchone()
        teams_temp = ''.join(teams) # Convert tuple to string
        while (teams is not None):
            if team == teams_temp: # When we add a team which is in team table, it will add to water_polo_player table
                 return page.add_player(Name, Surname, Position,Goals,Assists,team)
            teams = cursor.fetchone()
            if(teams is None):     # When we update a team which isn't in team table, you will be redirected to error html #
                return render_template('/WaterPolo/Add_Team_Error.html')
            teams_temp = ''.join(teams)

    elif 'Delete_Player' in request.form:
        try:
            ID = request.form['select']
            return page.delete_player(ID)
        except:
            return render_template('WaterPolo/Delete_Player_Error.html')
    elif 'Upd_Player' in request.form:
        return page.Upd_Player()
    elif 'Update_Player' in request.form:
        try:
            id = request.form['select']
        except:
            return render_template('/WaterPolo/Update_Player_Error.html')

        Name = request.form['name']
        Surname = request.form['surname']
        Position = request.form['position']
        Goals = request.form['goals']
        Assists = request.form['assists']
        team= request.form['team']

        query = "SELECT team_name FROM water_polo_team"
        cursor.execute(query)
        teams = cursor.fetchone()
        teams_temp = ''.join(teams) # Convert tuple to string
        while (teams is not None):
            if team == teams_temp: # When we update a team which is in team table, it will update
                return page.update_player(Name, Surname, Position,Goals,Assists,team,id)
            teams = cursor.fetchone()
            if(teams is None):     # When we update a team which isn't in team table, you will be redirected to error html #
                return render_template('/WaterPolo/Add_Team_Error.html')
            teams_temp = ''.join(teams)


    ####### Add,Delete and Update for Teams #############

    elif 'Add_Team' in request.form:
        Name = request.form['team_name']
        City = request.form['team_city']
        Team_Point = request.form['team_point']
        stand = request.form['stand']
        return page.add_Team(Name,City,Team_Point,stand)
    elif 'Delete_Team' in request.form:
        try:
            ID = request.form['select']
            return page.delete_player(ID)
        except:
            return render_template('WaterPolo/Delete_Team_Error.html')
    elif 'Upd_Team' in request.form:
        return page.Upd_Team()
    elif 'Update_Team' in request.form:
        try:
            id = request.form['select']
        except:
            return render_template('/WaterPolo/Update_Team_Error.html')
        Name = request.form['team_name']
        City = request.form['team_city']
        Team_Point = request.form['team_point']
        stand = request.form['stand']
        return page.update_Team(Name, City,Team_Point,stand, id)

    ####### Add,Delete and Update for Wounded #############

    elif 'Add_Wounded' in request.form:
        ID = request.form['w_id']
        name = request.form['w_name']
        surname = request.form['w_surname']
        injury_type = request.form['injury_type']
        team_id = request.form['team_id']
        team_name = request.form['team_name']
        return page.add_wounded(ID,name,surname,injury_type,team_id,team_name)

    elif 'Upd_Wounded' in request.form:
        return page.Upd_Wounded()

    elif 'Delete_Wounded' in request.form:
        try:
            ID = request.form['select']
            return page.delete_wounded(ID)
        except :
            return render_template('/WaterPolo/Delete_Wounded_Error.html')

    elif 'Update_Wounded' in request.form:
        try:
            id = request.form['select']
        except:
            return render_template('/WaterPolo/Update_Wounded_Error.html')
        Name = request.form['w_name']
        Surname = request.form['w_surname']
        injury_type = request.form['injury_type']
        team_id = request.form['team_id']
        team_name = request.form['team_name']

        full_name = Name+Surname

        check_team = True
        check_player = True

        query = "SELECT team_name FROM water_polo_team"
        cursor.execute(query)
        teams = cursor.fetchone()
        teams_temp = ''.join(teams) # Convert tuple to string

        while (teams is not None):
            if team_name == teams_temp:
                check_team=False
            teams = cursor.fetchone()
            if teams is None:
                break
            teams_temp = ''.join(teams) # Convert tuple to string


        query = "SELECT name,surname FROM water_polo_player"
        cursor.execute(query)
        name = cursor.fetchone()
        player_name = ''.join(name)


        while (name is not None):
            if full_name == player_name:
                check_player=False
            name = cursor.fetchone()
            if name is None:
                break
            player_name = ''.join(name) # Convert tuple to string

        if(check_player==False & check_team == False):
            return page.update_wounded(Name,Surname,injury_type,team_id,team_name,id)
        else:
            return render_template('/WaterPolo/Wounded_Error.html')


    elif 'Reset_Tables' in request.form:
        return page.init_table()

@app.route('/spear_fishing', methods=['GET', 'POST'])
def spear_fishing():
    dsn = app.config['dsn']
    page = Spear_fishing(dsn)

    if request.method == 'GET':
        return page.show_spearfishing_page()

    elif 'init_table' in request.form:
         return page.init_table()

    elif 'Add_Fisher' in request.form:
        Name = request.form['fisher_name']
        Surname = request.form['fisher_surname']
        Team_id = request.form['team_id']
        Team_name= request.form['team_name']
        Degree = request.form['degree']
        Point = request.form['point']
        return page.add_fisher(Name, Surname, Team_id,Team_name,Degree,Point)
    elif 'Delete_Fisher' in request.form:
        ID = request.form['select']
        return page.delete_fisher(ID)
    elif 'Upd_Fisher' in request.form:
        return page.Upd_Fisher()
    elif 'Update_Fisher' in request.form:
        fisher_id = request.form['select']
        Name = request.form['fisher_name']
        Surname = request.form['fisher_surname']
        Team_id = request.form['team_id']
        Team_name = request.form['team_name']
        Degree = request.form['degree']
        Point= request.form['point']
        return page.update_fisher(Name, Surname, Team_id,Team_name,Degree,Point,fisher_id)

    elif 'Add_Point' in request.form:
        Fisher_id = request.form['fisher_id']
        Fisher_name = request.form['fisher_name']
        Fish_name = request.form['fish_name']
        Gram = request.form['gram']
        return page.add_point(Fisher_id,Fisher_name,Fish_name,Gram)
    elif 'Delete_Point' in request.form:
        ID = request.form['select']
        return page.delete_point(ID)
    elif 'Upd_Point' in request.form:
        return page.Upd_Point()
    elif 'Update_Point' in request.form:
        id = request.form['select']
        Fisher_id = request.form['fisher_id']
        Fisher_name = request.form['fisher_name']
        Fish_name= request.form['fish_name']
        Gram = request.form['gram']
        return page.update_point(Fisher_id,Fisher_name,Fish_name,Gram, id)

    elif 'Add_Team' in request.form:
        Name = request.form['team_name']
        degree = request.form['team_degree']
        Point = request.form['team_point']
        return page.add_team(Name,degree,Point)
    elif 'Delete_Team' in request.form:
        ID = request.form['select']
        return page.delete_team(ID)
    elif 'Upd_Team' in request.form:
        return page.Upd_Team()
    elif 'Update_Team' in request.form:
        team_id = request.form['select']
        Name = request.form['team_name']
        Degree = request.form['team_degree']
        Point= request.form['team_point']
        return page.update_team(Name,Degree,Point,team_id)

    elif 'Reset_Tables' in request.form:
        return page.init_table()


if __name__ == '__main__':
     VCAP_APP_PORT = os.getenv('VCAP_APP_PORT')
     if VCAP_APP_PORT is not None:
        port, debug = int(VCAP_APP_PORT), False
     else:
        port, debug = 5000, True
     VCAP_SERVICES = os.getenv('VCAP_SERVICES')
     if VCAP_SERVICES is not None:
        app.config['dsn'] = get_elephantsql_dsn(VCAP_SERVICES)
     else:
        app.config['dsn'] = """user='vagrant' password='vagrant'
                               host='localhost' port=54321 dbname='itucsdb'"""
     app.secret_key = 'Hjdksahdjksahjkd'
     app.run(host='0.0.0.0', port=port, debug=debug)

    #app.run(host='0.0.0.0', port=5000,debug=True)




