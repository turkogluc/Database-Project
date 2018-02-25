import psycopg2 as dbapi2
from flask import render_template
from flask import redirect
from flask import url_for

class Polo_Store:

    def About_Page(self):
        return render_template('index.html')

    def __init__(self, key):
        self.key = key
        return

    def show_water_polo_page(self):
        with dbapi2.connect(self.key) as connection:
            cursor = connection.cursor()

            query = """ CREATE TABLE IF NOT EXISTS water_polo_team (
                        team_id serial PRIMARY KEY,
                        team_name text UNIQUE NOT NULL,
                        team_city text NOT NULL,
                        team_point integer NOT NULL,
                        stand integer NOT NULL)"""
            cursor.execute(query)

            query = """ CREATE TABLE IF NOT EXISTS water_polo_player (
                        id serial PRIMARY key,
                        name text NOT NULL,
                        surname text NOT NULL,
                        position integer,
                        goals integer,
                        assists integer,
                        team text NOT NULL)"""
            cursor.execute(query)

            query = """ CREATE TABLE IF NOT EXISTS wounded (
                        w_id integer NOT NULL,
                        w_name name NOT NULL,
                        w_surname text NOT NULL,
                        injury_type text NOT NULL,
                        team_id integer NOT NULL,
                        team_name text NOT NULL,
                        PRIMARY KEY(w_id,injury_type)
                        )"""
            cursor.execute(query)

            query = "SELECT * FROM water_polo_player"
            cursor.execute(query)
            players = cursor.fetchall()

            query = "SELECT * FROM water_polo_team"
            cursor.execute(query)
            teams = cursor.fetchall()

            query = "SELECT w_id,w_name,w_surname,injury_type,team_name FROM wounded"
            cursor.execute(query)
            wounded = cursor.fetchall()


            query = """WITH point_leader AS (SELECT ROW_NUMBER() OVER (ORDER BY goals+assists DESC) AS order,name, surname,
                        team,team_city, goals+assists AS point
                        FROM water_polo_player,water_polo_team
                    WHERE( team = water_polo_team.team_name)
                    ORDER BY point DESC)
                    SELECT "order",name,surname,team,team_city,point from point_leader
                    WHERE("order" < 6)
             """
            cursor.execute(query)
            point_leader = cursor.fetchall()

            query = """WITH goal_leader AS (SELECT ROW_NUMBER() OVER (ORDER BY goals DESC) AS order,name,surname,goals, team,team_city
                FROM water_polo_player,water_polo_team
                WHERE( (team = water_polo_team.team_name))
                ORDER BY goals DESC)
                SELECT "order",name,surname,goals,team,team_city FROM goal_leader
                WHERE("order"<6)
            """
            cursor.execute(query)
            goal_leaders = cursor.fetchall()



            query = """(WITH point_leader AS (SELECT ROW_NUMBER() OVER (ORDER BY goals+assists DESC) AS order,name, surname,
                    team,team_city,goals,goals+assists AS point
                        FROM water_polo_player,water_polo_team
                    WHERE( team= water_polo_team.team_name)
                    ORDER BY point DESC)
                    SELECT name,surname,team,team_city,goals,point from point_leader
                    WHERE("order" < 6))
                        INTERSECT
                    (WITH goal_leader AS (SELECT ROW_NUMBER() OVER (ORDER BY goals DESC) AS order,name,surname,
                    team,team_city,goals,goals+assists AS point
                    FROM water_polo_player,water_polo_team
                WHERE( team = water_polo_team.team_name)
                ORDER BY goals DESC)
                SELECT name,surname,team,team_city,goals,point FROM goal_leader
                 WHERE("order" < 6))

             """
            cursor.execute(query)
            pointandgoal_leader = cursor.fetchall()


            query = """SELECT wounded.team_name,COUNT(injury_type) FROM wounded,water_polo_team
                        WHERE(wounded.team_id =water_polo_team.team_id)
                        GROUP BY wounded.team_name
            """
            cursor.execute(query)
            team_wounded = cursor.fetchall()



        return render_template('WaterPolo/Store.html',players=players,teams = teams,wounded=wounded,team_wounded = team_wounded,
                                point_leader = point_leader,goal_leaders=goal_leaders,pointandgoal_leader = pointandgoal_leader)
        " "



    def init_table(self):
        with dbapi2.connect(self.key) as connection:
            cursor = connection.cursor()

            query = """DROP TABLE IF EXISTS water_polo_player CASCADE"""
            cursor.execute(query)
            query = """DROP TABLE IF EXISTS water_polo_team CASCADE"""
            cursor.execute(query)
            query = """DROP TABLE IF EXISTS wounded CASCADE """
            cursor.execute(query)

            query = """CREATE TABLE IF NOT EXISTS water_polo_team (
                        team_id serial PRIMARY KEY,
                        team_name text UNIQUE NOT NULL,
                        team_city text NOT NULL,
                        team_point integer NOT NULL,
                        stand integer NOT NULL)"""
            cursor.execute(query)

            query = """CREATE TABLE IF NOT EXISTS water_polo_player (
                        id serial PRIMARY key,
                        name text NOT NULL,
                        surname text NOT NULL,
                        position integer,
                        goals integer,
                        assists integer,
                        team text NOT NULL
                        )
                        """
            cursor.execute(query)

            query = """ CREATE TABLE IF NOT EXISTS wounded (
                        w_id integer NOT NULL,
                        w_name name NOT NULL,
                        w_surname text NOT NULL,
                        injury_type text NOT NULL,
                        team_id integer NOT NULL,
                        team_name text NOT NULL,
                        PRIMARY KEY(w_id,injury_type)
                        )"""
            cursor.execute(query)


            query = """ALTER TABLE wounded ADD CONSTRAINT FK_player_id
                      FOREIGN KEY (w_id)
                      REFERENCES water_polo_player(id)
                      ON DELETE CASCADE
                      ON UPDATE CASCADE"""
            cursor.execute(query)

            query = """ALTER TABLE water_polo_player ADD CONSTRAINT FK_team
                      FOREIGN KEY (team)
                      REFERENCES water_polo_team (team_name)
                      ON DELETE CASCADE
                      ON UPDATE CASCADE"""


            query = """ALTER TABLE wounded ADD CONSTRAINT FK_team_id
                      FOREIGN KEY (team_id)
                      REFERENCES water_polo_team(team_id)
                      ON DELETE CASCADE
                      ON UPDATE CASCADE"""
            cursor.execute(query)

            query = """INSERT INTO water_polo_team(team_name,team_city,team_point,stand)
                        VALUES
                        ('Alumni','Houstin', '9','6'),
                        ('USA_White', 'Seetle', '22','4'),
                        ('International', 'Austin', '9','7'),
                        ('Olympic_Club', 'San Francisco', '33','1'),
                        ('USA_Red', 'Portland', '21','5'),
                        ('USA_Blue', 'Boston', '25','2'),
                        ('NY_Athletic_Club', 'Philadelphia', '24','3')
                        """
            cursor.execute(query)


            query = """INSERT INTO water_polo_player(name, surname, position,goals,assists,team)
                        VALUES
                        ('Nick','Corniglia', '10','9','4','International'),
                        ('Paul', 'Reynolds', '7','35','4','USA_Blue'),
                        ('Cullen', 'Hennessy', '15','30','6','NY_Athletic_Club'),
                        ('Brian', 'Dudley', '8','33','11','USA_Red'),
                        ('Richie', 'Hyden', '9','43','5','USA_White'),
                        ('Andrew', 'Reego', '6','16','3','Alumni'),
                        ('Zac', 'Monsees', '11','27','13','Olympic_Club'),
                        ('Brian', 'Alexander','3','16','10','USA_Blue'),
                        ('Marin', 'Balarin','3','11','12','NY_Athletic_Club'),
                        ('Colin','Mulcohy', '12','19','7','Alumni'),
                        ('Alex', 'Roelse', '4','17','4','USA_White'),
                        ('Alex', 'Bowen', '3','34','6','Olympic_Club')
                        """
            cursor.execute(query)

            query = """INSERT INTO wounded(w_id,w_name,w_surname,injury_type,team_id,team_name)
                        VALUES
                        ('2','Nick','Corniglia','Muscle strains','3','USA_Blue'),
                        ('4','Brian', 'Dudley','Torn meniscus','5','USA_Red'),
                        ('5','Richie', 'Hyden','Ankle sprains and strains','2','USA_White'),
                        ('6','Andrew', 'Reego','Shoulder_tendinitis','1','Alumni'),
                        ('10','Collin','Mulcohy','Torn hamstrings','2','USA_White'),
                        ('8','Brian','Alexander','Shoulder dislocation','3','USA_Blue')
                        """
            cursor.execute(query)



            connection.commit()
        return redirect(url_for('Water_Polo'))

    def add_player(self, Name, Surname,Position,Goals,Assists,Team_Name):
        with dbapi2.connect(self.key) as connection:
            cursor = connection.cursor()

            query = """INSERT INTO water_polo_player(name, surname,position,goals,assists,team)
                        VALUES
                        ('%s', '%s', '%s', '%s', '%s','%s')""" % (Name, Surname,Position,Goals,Assists,Team_Name)
            cursor.execute(query)

            connection.commit()
        return redirect(url_for('Water_Polo'))

    def delete_player(self, id):
        with dbapi2.connect(self.key) as connection:
            cursor = connection.cursor()

            query = "DELETE FROM water_polo_player WHERE id = '%s'" % (id)
            cursor.execute(query)

            connection.commit()
        return redirect(url_for('Water_Polo'))
    def Upd_Player(self):
        with dbapi2.connect(self.key) as connection:
            cursor = connection.cursor()

            query = """ CREATE TABLE IF NOT EXISTS water_polo_team (
                        team_id serial PRIMARY KEY,
                        team_name text UNIQUE NOT NULL,
                        team_city text NOT NULL,
                        team_point integer NOT NULL,
                        stand integer NOT NULL)"""
            cursor.execute(query)

            query = """ CREATE TABLE IF NOT EXISTS water_polo_player (
                        id serial PRIMARY key,
                        name text NOT NULL,
                        surname text NOT NULL,
                        position integer NOT NULL,
                        goals integer NOT NULL,
                        assists integer NOT NULL,
                        team text NOT NULL)"""
            cursor.execute(query)

            query = "SELECT * FROM water_polo_player"
            cursor.execute(query)
            players = cursor.fetchall()

            return render_template('WaterPolo/UpdatePlayer.html',players=players)

    def update_player(self, Name, Surname,Position,Goals,Assists,Team_name, id):
        with dbapi2.connect(self.key) as connection:
            cursor = connection.cursor()

            query = """UPDATE water_polo_player
                        SET name='%s',surname='%s',position='%s',goals='%s',assists='%s',team = '%s'
                        WHERE id = '%s'""" % (Name, Surname,Position,Goals,Assists,Team_name, id)
            cursor.execute(query)

            connection.commit()
        return redirect(url_for('Water_Polo'))


    def add_Team(self, Name, City,Point,Stands):
        with dbapi2.connect(self.key) as connection:
            cursor = connection.cursor()

            query = """INSERT INTO water_polo_team(team_name, team_city,team_point,stand)
                        VALUES
                        ('%s', '%s', '%s', '%s')""" % (Name, City, Point,Stands)
            cursor.execute(query)

            connection.commit()
        return redirect(url_for('Water_Polo'))

    def delete_Team(self, Teamid):
        with dbapi2.connect(self.key) as connection:
            cursor = connection.cursor()

            query = "DELETE FROM water_polo_team WHERE team_id = '%s'" % (Teamid)
            cursor.execute(query)

            connection.commit()
        return redirect(url_for('Water_Polo'))
    def Upd_Team(self):
        with dbapi2.connect(self.key) as connection:
            cursor = connection.cursor()
            query = "SELECT * FROM water_polo_team"
            cursor.execute(query)
            team = cursor.fetchall()

            return render_template('WaterPolo/UpdateTeam.html',team=team)

    def update_Team(self, Name, City,Points,Stands, ID):
        with dbapi2.connect(self.key) as connection:
            cursor = connection.cursor()

            query = """UPDATE water_polo_team
                        SET team_name='%s',team_city='%s', team_point='%s', stand='%s'
                        WHERE team_id = '%s'""" % (Name,City,Points,Stands, ID)
            cursor.execute(query)

            connection.commit()
        return redirect(url_for('Water_Polo'))


    def add_wounded(self,Player_id, Name, Surname,Injury_type,Team_id,Team_Name):
        with dbapi2.connect(self.key) as connection:
            cursor = connection.cursor()

            query = """INSERT INTO wounded(w_id,w_name,w_surname,injury_type,team_id,team_name)
                        VALUES
                        ('%s', '%s', '%s', '%s', '%s','%s')""" % (Player_id,Name, Surname,Injury_type,Team_id,Team_Name)
            cursor.execute(query)

            connection.commit()
        return redirect(url_for('Water_Polo'))
    def delete_wounded(self, id):
        with dbapi2.connect(self.key) as connection:
            cursor = connection.cursor()

            query = "DELETE FROM wounded WHERE (w_id = '%s')" % (id)
            cursor.execute(query)

            connection.commit()
        return redirect(url_for('Water_Polo'))

    def Upd_Wounded(self):
        with dbapi2.connect(self.key) as connection:
            cursor = connection.cursor()
            query = "SELECT * FROM wounded"
            cursor.execute(query)
            wounded = cursor.fetchall()

            return render_template('WaterPolo/UpdateWounded.html',wounded=wounded)

    def update_wounded(self,Name, Surname,Injury_type,Team_id,Team_Name,Player_id):
        with dbapi2.connect(self.key) as connection:
            cursor = connection.cursor()

            query = """UPDATE wounded
                        SET w_name='%s', w_surname='%s', injury_type='%s',team_id='%s',team_name='%s'
                        WHERE w_id = '%s'""" % (Name, Surname,Injury_type,Team_id,Team_Name,Player_id)
            cursor.execute(query)

            connection.commit()
        return redirect(url_for('Water_Polo'))