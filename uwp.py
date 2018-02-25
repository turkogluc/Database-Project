import psycopg2 as dbapi2
from flask import render_template
from flask import redirect
from flask import url_for
from flask import flash

class UWP:
    def __init__(self, dsn):
        self.dsn = dsn
        with dbapi2.connect(self.dsn) as connection:
            cursor = connection.cursor()
            query =  """DO $$
                        BEGIN
                            IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'role') THEN
                                CREATE TYPE role AS ENUM ('Photographer', 'Assistant', 'Captain');
                            END IF;
                        END$$"""
            cursor.execute(query)

            query = """CREATE TABLE IF NOT EXISTS team (
                        id serial PRIMARY KEY,
                        country text NOT NULL)"""
            cursor.execute(query)

            query = """CREATE TABLE IF NOT EXISTS competitor (
                        id serial PRIMARY KEY,
                        name text NOT NULL,
                        surname text NOT NULL,
                        role role NOT NULL,
                        team_id integer REFERENCES team (id))"""
            cursor.execute(query)
        return

    def show_page_comp(self):
        with dbapi2.connect(self.dsn) as connection:
            cursor = connection.cursor()

            query = """SELECT competitor.id, name, surname, country, role FROM competitor, team
                        WHERE (team_id = team.id)"""
            cursor.execute(query)
            competitors = cursor.fetchall()

            query = "SELECT country FROM team"
            cursor.execute(query)
            countries = []
            for row in cursor:
                countries.append(row[0])
            query = "SELECT DISTINCT role FROM competitor"
            cursor.execute(query)
            roles = []
            for row in cursor:
                roles.append(row[0])

        return render_template('uwp/uwp_comp.html', competitors = sorted(competitors, key=lambda p: p[1]),
                               countries = countries, roles = roles)

    def show_page_team(self):
        with dbapi2.connect(self.dsn) as connection:
            cursor = connection.cursor()

            query = """SELECT team.id, country, COUNT(competitor.id)
                        FROM team LEFT JOIN competitor  ON team_id = team.id
                        GROUP BY team.id"""

            cursor.execute(query)
            teams = cursor.fetchall()

        return render_template('uwp/uwp_teams.html', teams = teams)

    def add_competitor(self, name, surname, country, role):
        with dbapi2.connect(self.dsn) as connection:
            cursor = connection.cursor()

            query = """INSERT INTO competitor (name, surname, role, team_id)
                        SELECT %s, %s, %s, team.id
                        FROM team WHERE team.country = %s
                        """
            cursor.execute(query, (name, surname, role, country))

            connection.commit()
        return redirect(url_for('uwp_comp'))

    def delete_competitor(self, id):
        with dbapi2.connect(self.dsn) as connection:
            cursor = connection.cursor()

            query = "DELETE FROM competitor WHERE id = %s"
            cursor.execute(query, (id,))

            connection.commit()
        return redirect(url_for('uwp_comp'))

    def update_competitor(self, name, surname, country, role, id):
        with dbapi2.connect(self.dsn) as connection:
            cursor = connection.cursor()

            query = """UPDATE competitor
                        SET name=%s,surname=%s,role=%s,team_id=subquery.id
                        FROM (SELECT team.id FROM team WHERE team.country = %s)
                        AS subquery
                        WHERE competitor.id = %s"""
            cursor.execute(query, (name, surname, role, country, id))

            connection.commit()
        return redirect(url_for('uwp_comp'))

    def add_team(self, country):
        with dbapi2.connect(self.dsn) as connection:
            cursor = connection.cursor()

            query = """INSERT INTO team (country)
                        VALUES (%s)"""
            cursor.execute(query, (country,))

            connection.commit()
        return redirect(url_for('uwp_team'))

    def update_team(self, country, id):
        with dbapi2.connect(self.dsn) as connection:
            cursor = connection.cursor()

            query = """UPDATE team
                        SET country = %s
                        WHERE id = %s"""
            cursor.execute(query, (country, id))

            connection.commit()
        return redirect(url_for('uwp_team'))

    def delete_team(self, id):
        with dbapi2.connect(self.dsn) as connection:
            cursor = connection.cursor()

            query = """SELECT team.id, country, COUNT(competitor.id)
                        FROM team LEFT JOIN competitor  ON team_id = team.id
                        WHERE team.id = %s GROUP BY team.id
                        """
            cursor.execute(query, (id,))
            id, country, members = cursor.fetchone()

            if members != 0:
                flash("You cannot delete a team that has members in the competitor list!")
            else:
                query = "DELETE FROM team WHERE id = %s"
                cursor.execute(query, (id,))

            connection.commit()
        return redirect(url_for('uwp_team'))

    def reset_table(self):
        with dbapi2.connect(self.dsn) as connection:
            cursor = connection.cursor()

            query = """DROP TABLE IF EXISTS competitor;
                        DROP TABLE IF EXISTS team;
                        DROP TYPE IF EXISTS role;"""
            cursor.execute(query)

            query = "CREATE TYPE role AS ENUM ('Photographer', 'Assistant', 'Captain')"
            cursor.execute(query)

            query = """CREATE TABLE team (
                        id serial PRIMARY KEY,
                        country text NOT NULL)"""
            cursor.execute(query)

            query = """CREATE TABLE competitor (
                        id serial PRIMARY KEY,
                        name text NOT NULL,
                        surname text NOT NULL,
                        role role NOT NULL,
                        team_id integer REFERENCES team (id))"""
            cursor.execute(query)

            query = """INSERT INTO team (country)
                        VALUES
                        ('Turkey'),
                        ('Italy')
                        """
            cursor.execute(query)

            query = """INSERT INTO competitor (name, surname, role, team_id)
                        VALUES
                        ('Ahmet', 'KARPUZSEVER', 'Photographer', 1),
                        ('Orhan', 'AYTUR', 'Captain', 1),
                        ('Melek', 'KOYUKANAT', 'Photographer', 1),
                        ('Leyla', 'LALECI', 'Assistant', 1),
                        ('Ivo', 'MONALDO', 'Photographer', 2),
                        ('Rosita', 'BUCCHO', 'Assistant', 2),
                        ('Callan', 'ROBERTSON', 'Assistant', 2),
                        ('Katarina', 'LONCAR', 'Captain', 2),
                        ('Fastred', 'RUMBLE', 'Photographer', 2)
                        """
            cursor.execute(query)

            connection.commit()
        return redirect(url_for('uwp_comp'))
