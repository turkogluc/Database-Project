import psycopg2 as dbapi2
from flask import render_template
from flask import redirect
from flask import url_for

class PowerBoat:
    def __init__(self, dsn):
        self.dsn = dsn
        return


###### initializating all tables ####################
    def initdb(self):
        with dbapi2.connect(self.dsn) as connection:
            cursor = connection.cursor()

            query = """DROP TABLE IF EXISTS teams,boats,drivers,league15,oldraces CASCADE"""
            cursor.execute(query)

            query = """CREATE TABLE IF NOT EXISTS teams(
                      id serial primary key,
                      name text,
                      captain integer,
                      championship integer default 0)
                      """
            cursor.execute(query)

            query = """CREATE TABLE IF NOT EXISTS boats(
                      id serial primary key,
                      driver integer default 0,
                      speed integer default 0)
                      """
            cursor.execute(query)

            query = """CREATE TABLE IF NOT EXISTS drivers(
                      id serial primary key,
                      name text,
                      team integer default 0,
                      boat integer default 0)
                      """
            cursor.execute(query)

            query = """CREATE TABLE IF NOT EXISTS league15(
                      pos serial primary key,
                      boat integer default 0,
                      point integer default 0)
                      """
            cursor.execute(query)

            query = """CREATE TABLE IF NOT EXISTS oldraces(
                      race_id serial primary key,
                      class integer,
                      date integer,
                      location text,
                      winner integer default 0)
                      """
            cursor.execute(query)

# initiating first values for driver
            query = """INSERT INTO drivers (name,team,boat) VALUES
                    ('michael',1,1
                    )"""
            cursor.execute(query)
            query = """INSERT INTO drivers (name,team,boat) VALUES
                    ('mustafa',1,2
                    )"""
            cursor.execute(query)
            query = """INSERT INTO drivers (name,team,boat) VALUES
                    ('cemal',1,3
                    )"""
            cursor.execute(query)
            query = """INSERT INTO drivers (name,team,boat) VALUES
                    ('Jane',2,4
                    )"""
            cursor.execute(query)
            query = """INSERT INTO drivers (name,team,boat) VALUES
                    ('Patcick',2,5
                    )"""
            cursor.execute(query)
            query = """INSERT INTO drivers (name,team,boat) VALUES
                    ('Lisbon',3,6
                    )"""
            cursor.execute(query)
            query = """INSERT INTO drivers (name,team,boat) VALUES
                    ('Cho',3,7
                    )"""
            cursor.execute(query)
            query = """INSERT INTO drivers (name,team,boat) VALUES
                    ('Kimball',3,8
                    )"""
            cursor.execute(query)
            query = """INSERT INTO drivers (name,team,boat) VALUES
                    ('Elif',4,9
                    )"""
            cursor.execute(query)
            query = """INSERT INTO drivers (name,team,boat) VALUES
                    ('Salih',4,10
                    )"""
            cursor.execute(query)
            query = """INSERT INTO drivers (name,team,boat) VALUES
                    ('Emre',5,11
                    )"""
            cursor.execute(query)
            query = """INSERT INTO drivers (name,team,boat) VALUES
                    ('Ozan',5,12
                    )"""
            cursor.execute(query)
            query = """INSERT INTO drivers (name,team,boat) VALUES
                    ('Nur',5,13
                    )"""
            cursor.execute(query)
            query = """INSERT INTO drivers (name,team,boat) VALUES
                    ('Esat',6,14
                    )"""
            cursor.execute(query)
            query = """INSERT INTO drivers (name,team,boat) VALUES
                    ('ibrahim',6,15
                    )"""
            cursor.execute(query)
# initiating first values for teams
            query = """INSERT INTO teams (name,captain,championship) VALUES
                    ('Lions',1,20
                    )"""
            cursor.execute(query)
            query = """INSERT INTO teams (name,captain,championship) VALUES
                    ('Rose',4,18
                    )"""
            cursor.execute(query)
            query = """INSERT INTO teams (name,captain,championship) VALUES
                    ('Bigbang',7,15
                    )"""
            cursor.execute(query)
            query = """INSERT INTO teams (name,captain,championship) VALUES
                    ('XLarge',9,15
                    )"""
            cursor.execute(query)
            query = """INSERT INTO teams (name,captain,championship) VALUES
                    ('BigBoys',13,12
                    )"""
            cursor.execute(query)
            query = """INSERT INTO teams (name,captain,championship) VALUES
                    ('Sacremento',15,10
                    )"""
            cursor.execute(query)
# initiating boats
            query = """INSERT INTO boats (driver,speed) VALUES
                     (1,165
                    )"""
            cursor.execute(query)
            query = """INSERT INTO boats (driver,speed) VALUES
                     (2,158
                    )"""
            cursor.execute(query)
            query = """INSERT INTO boats (driver,speed) VALUES
                     (3,140
                    )"""
            cursor.execute(query)
            query = """INSERT INTO boats (driver,speed) VALUES
                     (4,150
                    )"""
            cursor.execute(query)
            query = """INSERT INTO boats (driver,speed) VALUES
                     (5,140
                    )"""

            cursor.execute(query)
            query = """INSERT INTO boats (driver,speed) VALUES
                     (6,135
                    )"""
            cursor.execute(query)
            query = """INSERT INTO boats (driver,speed) VALUES
                     (7,138
                    )"""
            cursor.execute(query)
            query = """INSERT INTO boats (driver,speed) VALUES
                     (8,160
                    )"""
            cursor.execute(query)
            query = """INSERT INTO boats (driver,speed) VALUES
                     (9,152
                    )"""
            cursor.execute(query)
            query = """INSERT INTO boats (driver,speed) VALUES
                     (10,120
                    )"""
            cursor.execute(query)
            query = """INSERT INTO boats (driver,speed) VALUES
                     (11,140
                    )"""
            cursor.execute(query)
            query = """INSERT INTO boats (driver,speed) VALUES
                     (12,122
                    )"""
            cursor.execute(query)
            query = """INSERT INTO boats (driver,speed) VALUES
                     (13,143
                    )"""
            cursor.execute(query)
            query = """INSERT INTO boats (driver,speed) VALUES
                     (14,144
                    )"""
            cursor.execute(query)
            query = """INSERT INTO boats (driver,speed) VALUES
                     (15,115
                    )"""
            cursor.execute(query)
# initiating league15 table

            query = """INSERT INTO league15 (boat,point) VALUES
                     (1,1580
                    )"""
            cursor.execute(query)
            query = """INSERT INTO league15 (boat,point) VALUES
                     (7,1500
                    )"""
            cursor.execute(query)
            query = """INSERT INTO league15 (boat,point) VALUES
                     (2,1400
                    )"""
            cursor.execute(query)
            query = """INSERT INTO league15 (boat,point) VALUES
                     (6,1380
                    )"""
            cursor.execute(query)
            query = """INSERT INTO league15 (boat,point) VALUES
                     (3,1300
                    )"""
            cursor.execute(query)
            query = """INSERT INTO league15 (boat,point) VALUES
                     (5,1275
                    )"""
            cursor.execute(query)
            query = """INSERT INTO league15 (boat,point) VALUES
                     (4,1250
                    )"""
            cursor.execute(query)
            query = """INSERT INTO league15 (boat,point) VALUES
                     (10,1240
                    )"""
            cursor.execute(query)
            query = """INSERT INTO league15 (boat,point) VALUES
                     (11,1233
                    )"""
            cursor.execute(query)
            query = """INSERT INTO league15 (boat,point) VALUES
                     (12,1230
                    )"""
            cursor.execute(query)
            query = """INSERT INTO league15 (boat,point) VALUES
                     (13,1220
                    )"""
            cursor.execute(query)
            query = """INSERT INTO league15 (boat,point) VALUES
                     (14,1210
                    )"""
            cursor.execute(query)

# initialization of old races
            query = """INSERT INTO oldraces (race_id,class,date,location,winner) VALUES
                     (1001,1,1999,'Istanbul',1)"""
            cursor.execute(query)
            query = """INSERT INTO oldraces (race_id,class,date,location,winner) VALUES
                     (1002,1,2003,'Paris',4)"""
            cursor.execute(query)
            query = """INSERT INTO oldraces (race_id,class,date,location,winner) VALUES
                     (1003,2,2004,'London',6)"""
            cursor.execute(query)
            query = """INSERT INTO oldraces (race_id,class,date,location,winner) VALUES
                     (1004,3,2004,'Berlin',1)"""
            cursor.execute(query)
            query = """INSERT INTO oldraces (race_id,class,date,location,winner) VALUES
                     (1005,1,2005,'Barcelona',1)"""
            cursor.execute(query)
            query = """INSERT INTO oldraces (race_id,class,date,location,winner) VALUES
                     (1006,2,2006,'Chicago',10)"""
            cursor.execute(query)
            query = """INSERT INTO oldraces (race_id,class,date,location,winner) VALUES
                     (1007,1,2007,'New York',9)"""
            cursor.execute(query)
            query = """INSERT INTO oldraces (race_id,class,date,location,winner) VALUES
                     (1008,3,2009,'Bursa',5)"""
            cursor.execute(query)
            query = """INSERT INTO oldraces (race_id,class,date,location,winner) VALUES
                     (1009,2,2010,'Madrid',4)"""
            cursor.execute(query)
            query = """INSERT INTO oldraces (race_id,class,date,location,winner) VALUES
                     (10010,1,2010,'Manchester',3)"""
            cursor.execute(query)

############### foreign key additions #####################################
            query = """ALTER TABLE drivers ADD CONSTRAINT FK_Drivers_team
                      FOREIGN KEY (team)
                      REFERENCES teams (id)
                      ON DELETE CASCADE
                      ON UPDATE CASCADE"""
            cursor.execute(query)

            query = """ALTER TABLE drivers ADD CONSTRAINT FK_Drivers_boat
                      FOREIGN KEY (boat)
                      REFERENCES boats (id)
                      ON DELETE CASCADE
                      ON UPDATE CASCADE"""
            cursor.execute(query)

            query = """ALTER TABLE oldraces ADD CONSTRAINT FK_oldraces_winner
                      FOREIGN KEY (winner)
                      REFERENCES drivers (id)
                      ON DELETE CASCADE
                      ON UPDATE CASCADE"""
            cursor.execute(query)

            query = """ALTER TABLE teams ADD CONSTRAINT FK_teams_captain
                      FOREIGN KEY (captain)
                      REFERENCES drivers (id)
                      ON DELETE CASCADE
                      ON UPDATE CASCADE"""
            cursor.execute(query)

            query = """ALTER TABLE boats ADD CONSTRAINT FK_boats_driver
                      FOREIGN KEY (driver)
                      REFERENCES drivers (id)
                      ON DELETE CASCADE
                      ON UPDATE CASCADE"""
            cursor.execute(query)

            query = """ALTER TABLE league15 ADD CONSTRAINT FK_league15_boat
                      FOREIGN KEY (boat)
                      REFERENCES boats (id)
                      ON DELETE CASCADE
                      ON UPDATE CASCADE"""
            cursor.execute(query)

            cursor.close()
        return redirect(url_for('power_boat'))
### end of initialization


########### displaying tables with select functions #######

# for displaying all tables

    def show_all(self):
        with dbapi2.connect(self.dsn) as connection:
            cursor = connection.cursor()

            query = "SELECT * FROM boats order by id"
            cursor.execute(query)
            boats = cursor.fetchall()

            query = "SELECT * FROM teams order by id"
            cursor.execute(query)
            teams = cursor.fetchall()

            query = "SELECT * FROM league15 order by pos"
            cursor.execute(query)
            league15 = cursor.fetchall()

            query = "SELECT * FROM oldraces order by race_id"
            cursor.execute(query)
            oldraces = cursor.fetchall()

            query = "SELECT * FROM drivers order by id"
            cursor.execute(query)
            drivers = cursor.fetchall()
        return render_template('PowerBoat/Powerboat.html',boats=boats,teams=teams,league15=league15,oldraces=oldraces,drivers=drivers)

# for displayin just one table at once
    def show_boats(self):
        with dbapi2.connect(self.dsn) as connection:
            cursor = connection.cursor()

            query = "SELECT * FROM boats order by id"
            cursor.execute(query)
            boats = cursor.fetchall()
        return render_template('PowerBoat/Powerboat.html', boats = sorted(boats , key=lambda p: p[1]))

    def show_teams(self):
        with dbapi2.connect(self.dsn) as connection:
            cursor = connection.cursor()

            query = "SELECT * FROM teams order by id"
            cursor.execute(query)
            teams = cursor.fetchall()
        return render_template('PowerBoat/Powerboat.html', teams = sorted(teams , key=lambda p: p[1]))

    def show_league15(self):
        with dbapi2.connect(self.dsn) as connection:
            cursor = connection.cursor()

            query = "SELECT * FROM league15 order by pos"
            cursor.execute(query)
            league15 = cursor.fetchall()
        return render_template('PowerBoat/Powerboat.html', league15 = sorted(league15 , key=lambda p: p[1]))

    def show_oldraces(self):
        with dbapi2.connect(self.dsn) as connection:
            cursor = connection.cursor()

            query = "SELECT * FROM oldraces order by race_id"
            cursor.execute(query)
            oldraces = cursor.fetchall()
        return render_template('PowerBoat/Powerboat.html', oldraces = sorted(oldraces , key=lambda p: p[1]))

    def show_drivers(self):
        with dbapi2.connect(self.dsn) as connection:
            cursor = connection.cursor()

            query = "SELECT * FROM drivers order by id"
            cursor.execute(query)
            drivers = cursor.fetchall()
        return render_template('PowerBoat/Powerboat.html', drivers = sorted(drivers, key=lambda p: p[1]))
######  end of show functions


######  operations #############
    def add(self,name,team,boat,table):
        with dbapi2.connect(self.dsn) as connection:
            cursor = connection.cursor()

            query = """INSERT INTO %s (name, team, boat)
                        VALUES
                        ('%s', %s ,%s)""" % (table , name, team , boat)
            cursor.execute(query)

            connection.commit()
        return redirect(url_for('power_boat'))

    def delete(self,id,table):

        with dbapi2.connect(self.dsn) as connection:
            cursor = connection.cursor()

            query = """DELETE FROM %s WHERE id = '%s' """ %(table,id)
            cursor.execute(query)

            connection.commit()
        return redirect(url_for('power_boat'))

    def update(self, id, name, team, boat,table):
        with dbapi2.connect(self.dsn) as connection:
            cursor = connection.cursor()

            query = """UPDATE %s
                        SET name='%s',team='%s',boat='%s'
                        WHERE id = '%s'""" % (table,name,team,boat, id)
            cursor.execute(query)

            connection.commit()
        return redirect(url_for('power_boat'))

    def reset_driver(self):
        with dbapi2.connect(self.dsn) as connection:
            cursor = connection.cursor()

            query = """DROP TABLE IF EXISTS drivers"""
            cursor.execute(query)

            query = """CREATE TABLE IF NOT EXISTS drivers(
                      id serial primary key,
                      name text,
                      team integer default 0,
                      boat integer default 0)
                      """
            cursor.execute(query)

            connection.commit()
        return redirect(url_for('power_boat'))
### end of operations


### baginnig of operation of 2 entities

    def disp_second(self):
        return render_template('PowerBoat/disp_second.html')

    def join1(self):
        with dbapi2.connect(self.dsn) as connection:
            cursor = connection.cursor()

            query = """ SELECT * FROM drivers JOIN teams ON (drivers.team=teams.id)
                      """
            cursor.execute(query)
            joinfirst = cursor.fetchall()
            cursor.close()
        return render_template('PowerBoat/join1.html',joinfirst = sorted(joinfirst , key=lambda p: p[1]))

    def join2(self):
        with dbapi2.connect(self.dsn) as connection:
            cursor = connection.cursor()

            query = """ SELECT * FROM league15 JOIN boats ON (league15.boat=boats.id)
                      """
            cursor.execute(query)
            joinsec = cursor.fetchall()
            cursor.close()
        return render_template('PowerBoat/join2.html',joinsec=joinsec)
    ###### !!!!!!!!!!! parametreleri gönderirken bu şekilde gönderirsen
    #####  (lambda kullanmadan) düzgün sıralamada calisir.
    def Ljoin(self):
        with dbapi2.connect(self.dsn) as connection:
            cursor = connection.cursor()

            query = """ SELECT * FROM drivers LEFT OUTER JOIN oldraces ON (drivers.id=oldraces.winner)
                      """
            cursor.execute(query)
            join = cursor.fetchall()
            cursor.close()
            direction = "LEFT"
        return render_template('PowerBoat/join3.html',join=join,direction=direction)

    def Rjoin(self):
        with dbapi2.connect(self.dsn) as connection:
            cursor = connection.cursor()

            query = """ SELECT * FROM drivers RIGHT OUTER JOIN oldraces ON (drivers.id=oldraces.winner)
                      """
            cursor.execute(query)
            join = cursor.fetchall()
            cursor.close()
            direction = "RIGHT"
        return render_template('PowerBoat/join3.html',join=join,direction=direction)

    def Fjoin(self):
        with dbapi2.connect(self.dsn) as connection:
            cursor = connection.cursor()

            query = """ SELECT * FROM drivers FULL JOIN oldraces ON (drivers.id=oldraces.winner)
                      """
            cursor.execute(query)
            join = cursor.fetchall()
            cursor.close()
            direction = "FULL"
        return render_template('PowerBoat/join3.html',join=join,direction=direction)

    def intersect(self):
        with dbapi2.connect(self.dsn) as connection:
            cursor = connection.cursor()

            query = """SELECT drivers.boat FROM oldraces JOIN drivers ON (oldraces.winner=drivers.id)
                    INTERSECT
                    SELECT boat FROM league15
                    """
            cursor.execute(query)

            intersect = cursor.fetchall()

            query = """SELECT drivers.boat FROM oldraces JOIN drivers ON (oldraces.winner=drivers.id)
                    INTERSECT
                    SELECT boat FROM league15 where pos in (1,2,3)
                    """
            cursor.execute(query)
            intersect2 = cursor.fetchall()
            cursor.close()
        return render_template('PowerBoat/intersect.html',intersect=intersect,intersect2=intersect2)

    def union(self):
        with dbapi2.connect(self.dsn) as connection:
            cursor = connection.cursor()

            query = """SELECT id,name from drivers where id in (SELECT winner FROM oldraces
                                                                UNION
                                                              SELECT captain FROM teams)
                    """
            cursor.execute(query)

            union = cursor.fetchall()

            cursor.close()
        return render_template('PowerBoat/union.html',union=union)
    def minus(self):
        with dbapi2.connect(self.dsn) as connection:
            cursor = connection.cursor()

            query = """SELECT id,name FROM drivers where id in (SELECT id from drivers
                                                                   EXCEPT
                                                               SELECT captain FROM teams)
                    """
            cursor.execute(query)

            minus = cursor.fetchall()

            cursor.close()
        return render_template('PowerBoat/minus.html',minus=minus)
    def best(self):
        with dbapi2.connect(self.dsn) as connection:
            cursor = connection.cursor()

            query = """ SELECT winner,name,count(*) from oldraces join drivers on (winner=id)
                        group by winner,name
                        having count(*) = (SELECT count(*) from oldraces
                                            GROUP BY winner
                                            order by count(*) DESC limit 1 offset 0
                                            )
                     """
            cursor.execute(query)
            best = cursor.fetchall()
            cursor.close()
        return render_template('PowerBoat/best.html',best=best)
