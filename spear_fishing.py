import psycopg2 as dbapi2
from flask import render_template
from flask import redirect
from flask import url_for

class Spear_fishing:

    def __init__(self, key):
        self.key = key
        return

    def show_spearfishing_page(self):
        with dbapi2.connect(self.key) as connection:
            cursor = connection.cursor()

            query = """ CREATE TABLE IF NOT EXISTS spear_fisher (
                        fisher_id serial PRIMARY KEY,
                        fisher_name text NOT NULL,
                        fisher_surname text NOT NULL,
                        team_id integer NOT NULL,
                        team_name text NOT NULL,
                        degree integer NOT NULL,
                        point integer NOT NULL
                        )"""
            cursor.execute(query)

            query = """ CREATE TABLE IF NOT EXISTS point (
                        id serial PRIMARY key,
                        fisher_id integer NOT NULL,
                        fisher_name text NOT NULL,
                        fish_name text NOT NULL,
                        gram integer NOT NULL
                        )"""
            cursor.execute(query)

            query = """ CREATE TABLE IF NOT EXISTS team (
                        team_id serial PRIMARY key,
                        team_name text NOT NULL,
                        team_degree integer NOT NULL,
                        team_point integer NOT NULL
                        )"""
            cursor.execute(query)

            query = "SELECT * FROM spear_fisher"
            cursor.execute(query)
            fishers = cursor.fetchall()

            query = "SELECT * FROM point"
            cursor.execute(query)
            point = cursor.fetchall()

            query = "SELECT * FROM team"
            cursor.execute(query)
            team = cursor.fetchall()

            query = """ SELECT spear_fisher.fisher_name,fisher_surname,fish_name,gram,team.team_name,team_point
                        FROM spear_fisher,point,team
                              WHERE(spear_fisher.fisher_id=point.fisher_id AND
                                    spear_fisher.team_name = team.team_name AND
                                    (gram>=1500))

             """

            cursor.execute(query)
            min_fish = cursor.fetchall()

            query = """(WITH score_leader AS (SELECT ROW_NUMBER() OVER (ORDER BY gram1*point DESC) AS order,
                         fisher_name,fisher_surname,team_name FROM
                         (SELECT fisher_id,SUM(gram) AS gram1 FROM point
                            GROUP BY fisher_id) AS table1,spear_fisher
                              WHERE(spear_fisher.fisher_id=table1.fisher_id)
                              ORDER BY gram1*point DESC)
                        SELECT fisher_name,fisher_surname,team_name from score_leader
                    WHERE("order" <=5))
                        INTERSECT
                       (WITH team_leader AS (SELECT ROW_NUMBER() OVER (ORDER BY point DESC) AS order,
                         fisher_name,fisher_surname,team.team_name FROM team,spear_fisher
                              WHERE(spear_fisher.team_id=team.team_id)
                              ORDER BY point DESC)
                        SELECT fisher_name,fisher_surname,team_name from team_leader
                    WHERE("order" <=5))"""


            cursor.execute(query)
            leader = cursor.fetchall()

            query = """ SELECT spear_fisher.fisher_name,fisher_surname,team_id,gram FROM spear_fisher,point
                              WHERE(spear_fisher.fisher_id=point.fisher_id)"""



            cursor.execute(query)
            max_gram = cursor.fetchall()

        return render_template('SpearFishing/Spear_Store.html',fishers=fishers,point=point,team = team,
                               max_gram=max_gram,min_fish=min_fish)




    def init_table(self):
        with dbapi2.connect(self.key) as connection:
            cursor = connection.cursor()

            query = """DROP TABLE IF EXISTS spear_fisher CASCADE"""
            cursor.execute(query)
            query = """DROP TABLE IF EXISTS point CASCADE"""
            cursor.execute(query)
            query = """DROP TABLE IF EXISTS team CASCADE """
            cursor.execute(query)

            query = """ CREATE TABLE IF NOT EXISTS spear_fisher (
                        fisher_id serial PRIMARY KEY,
                        fisher_name text,
                        fisher_surname text NOT NULL,
                        team_id integer NOT NULL,
                        team_name text NOT NULL,
                        degree integer NOT NULL,
                        point integer NOT NULL
                        )"""
            cursor.execute(query)

            query = """ CREATE TABLE IF NOT EXISTS point (
                        id serial PRIMARY key,
                        fisher_id integer NOT NULL,
                        fisher_name text NOT NULL,
                        fish_name text NOT NULL,
                        gram integer NOT NULL
                        )"""
            cursor.execute(query)

            query = """ CREATE TABLE IF NOT EXISTS team (
                        team_id serial PRIMARY key,
                        team_name text UNIQUE NOT NULL,
                        team_degree integer NOT NULL,
                        team_point integer NOT NULL
                        )"""
            cursor.execute(query)

            query = """INSERT INTO spear_fisher(fisher_name,fisher_surname,team_id,team_name,degree,point)
                        VALUES
                        ('A','A','1','U','1','1000'),
                        ('B','B','2','V','2','2000'),
                        ('C','C','3','X','3','3000'),
                        ('D','D','4','Y','4','4000'),
                        ('E','E','5','Z','5','5000')
                        """
            cursor.execute(query)


            query = """INSERT INTO point(fisher_id,fisher_name,fish_name,gram)
                        VALUES
                        ('1','A','A','1300'),
                        ('1','A','D','1600'),
                        ('1','A','C','1400'),
                        ('2','B','B','1400'),
                        ('3','C','C','1500'),
                        ('4','D','D','1600'),
                        ('2','B','D','1400'),
                        ('3','C','B','1500'),
                        ('4','D','A','1500'),
                        ('2','B','C','1400'),
                        ('3','C','A','1200'),
                        ('4','D','B','1300')
                        """
            cursor.execute(query)

            query = """INSERT INTO team(team_name,team_degree,team_point)
                        VALUES
                        ('U','1','55000'),
                        ('V','2','56000'),
                        ('X','3','57000'),
                        ('Y','4','58000'),
                        ('Z','5','59000')

                        """
            cursor.execute(query)



            connection.commit()
        return redirect(url_for('spear_fishing'))

    def add_fisher(self, fisher_name,fisher_surname,team_id,team_name,degree,point):
        with dbapi2.connect(self.key) as connection:
            cursor = connection.cursor()

            query = """INSERT INTO spear_fisher(fisher_name,fisher_surname,team_id,team_name,degree,point)
                        VALUES
                        ('%s', '%s', '%s', '%s', '%s','%s')""" % (fisher_name,fisher_surname,team_id,team_name,degree,point)
            cursor.execute(query)

            connection.commit()
        return redirect(url_for('spear_fishing'))

    def delete_fisher(self, id):
        with dbapi2.connect(self.key) as connection:
            cursor = connection.cursor()

            query = "DELETE FROM spear_fisher WHERE fisher_id = '%s'" % (id)
            cursor.execute(query)

            connection.commit()
        return redirect(url_for('spear_fishing'))
    def Upd_Fisher(self):
        with dbapi2.connect(self.key) as connection:
            cursor = connection.cursor()

            query = """ CREATE TABLE IF NOT EXISTS spear_fisher (
                        fisher_id serial PRIMARY KEY,
                        fisher_name text NOT NULL,
                        fisher_surname text NOT NULL,
                        team_id integer NOT NULL,
                        team_name text NOT NULL,
                        degree integer NOT NULL,
                        point integer NOT NULL
                        )"""
            cursor.execute(query)

            query = """ CREATE TABLE IF NOT EXISTS point (
                        id serial PRIMARY key,
                        fisher_id integer NOT NULL,
                        fisher_name text,
                        fish_name text NOT NULL,
                        gram integer NOT NULL
                        )"""
            cursor.execute(query)

            query = """ CREATE TABLE IF NOT EXISTS team (
                        team_id serial PRIMARY key,
                        team_name text NOT NULL,
                        team_degree integer NOT NULL,
                        team_point integer NOT NULL
                        )"""
            cursor.execute(query)

            query = "SELECT * FROM spear_fisher"
            cursor.execute(query)
            fishers = cursor.fetchall()

            return render_template('SpearFishing/update_fisher.html',fishers = fishers)

    def update_fisher(self, Name, Surname, Team_id,Team_name,Degree,Point,fisher_id):
        with dbapi2.connect(self.key) as connection:
            cursor = connection.cursor()

            query = """UPDATE spear_fisher
                        SET fisher_name='%s',fisher_surname='%s',team_id='%s',team_name='%s',degree='%s',point = '%s'
                        WHERE fisher_id = '%s'""" % (Name, Surname, Team_id,Team_name,Degree,Point,fisher_id)
            cursor.execute(query)

            connection.commit()
        return redirect(url_for('spear_fishing'))


    def add_point(self, Fisher_id,Fisher_name,Fish_name,Gram):
        with dbapi2.connect(self.key) as connection:
            cursor = connection.cursor()

            query = """INSERT INTO point(fisher_id,fisher_name,fish_name,gram)
                        VALUES
                        ('%s', '%s', '%s', '%s')""" % (Fisher_id,Fisher_name,Fish_name,Gram)
            cursor.execute(query)

            connection.commit()
        return redirect(url_for('spear_fishing'))

    def delete_point(self, id):
        with dbapi2.connect(self.key) as connection:
            cursor = connection.cursor()

            query = "DELETE FROM point WHERE id = '%s'" % (id)
            cursor.execute(query)

            connection.commit()
        return redirect(url_for('spear_fishing'))
    def Upd_Point(self):
        with dbapi2.connect(self.key) as connection:
            cursor = connection.cursor()
            query = "SELECT * FROM point"
            cursor.execute(query)
            point = cursor.fetchall()

        return render_template('SpearFishing/update_point.html',point=point)

    def update_point(self, Fisher_id, Fisher_name,Fish_name,Gram, ID):
        with dbapi2.connect(self.key) as connection:
            cursor = connection.cursor()

            query = """UPDATE point
                        SET fisher_id='%s',fisher_name='%s', fish_name='%s', gram='%s'
                        WHERE id = '%s'""" % (Fisher_id,Fisher_name,Fisher_name,Gram, ID)
            cursor.execute(query)

            connection.commit()
        return redirect(url_for('spear_fishing'))

    def add_team(self, team_name,degree,point):
        with dbapi2.connect(self.key) as connection:
            cursor = connection.cursor()

            query = """INSERT INTO team(team_name,team_degree,team_point)
                        VALUES
                        ('%s', '%s', '%s')""" % (team_name,degree,point)
            cursor.execute(query)

            connection.commit()
        return redirect(url_for('spear_fishing'))

    def delete_team(self, id):
        with dbapi2.connect(self.key) as connection:
            cursor = connection.cursor()

            query = "DELETE FROM team WHERE team_id = '%s'" % (id)
            cursor.execute(query)

            connection.commit()
        return redirect(url_for('spear_fishing'))

    def Upd_Team(self):
        with dbapi2.connect(self.key) as connection:
            cursor = connection.cursor()
            query = "SELECT * FROM team"
            cursor.execute(query)
            team = cursor.fetchall()

        return render_template('SpearFishing/update_team.html',team = team)

    def update_team(self, team_name,degree,point, ID):
        with dbapi2.connect(self.key) as connection:
            cursor = connection.cursor()

            query = """UPDATE team
                        SET team_name='%s',team_degree='%s', team_point='%s'
                        WHERE team_id = '%s'""" % (team_name,degree,point, ID)
            cursor.execute(query)

            connection.commit()
        return redirect(url_for('spear_fishing'))