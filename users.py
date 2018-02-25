import psycopg2 as dbapi2
from flask import render_template
from flask import redirect
from flask import url_for, session, flash

class Users:
    def __init__(self, dsn):
        self.dsn = dsn
        with dbapi2.connect(self.dsn) as connection:
            cursor = connection.cursor()

            query = """CREATE TABLE IF NOT EXISTS users(
                        id serial PRIMARY KEY,
                        username text UNIQUE NOT NULL,
                        password text NOT NULL,
                        type text NOT NULL)"""
            cursor.execute(query)

            query = """INSERT INTO users (username, password, type)
                        SELECT 'admin', '3333', 'Admin'
                        WHERE
                        NOT EXISTS (
                            SELECT username FROM users WHERE username = 'admin'
                        )"""
            cursor.execute(query)

            connection.commit()
        return

    def delete_user(self, id):
        with dbapi2.connect(self.dsn) as connection:
            cursor = connection.cursor()

            query = "DELETE FROM users WHERE id = %s"
            cursor.execute(query, (id,))

            connection.commit()
        return redirect(url_for('users'))

    def update_user(self, username, password, type, id):
        with dbapi2.connect(self.dsn) as connection:
            cursor = connection.cursor()

            query = """UPDATE users
                        SET username=%s,password=%s,type=%s
                        WHERE id = %s"""
            cursor.execute(query, (username, password, type, id))

            connection.commit()
        return redirect(url_for('users'))

    def add_user(self, username, password, type):
        with dbapi2.connect(self.dsn) as connection:
            cursor = connection.cursor()

            query = """SELECT username FROM users
                        WHERE username = %s"""
            cursor.execute(query, (username,))
            if cursor.fetchall():
                return False
            else:
                query = """INSERT INTO users (username, password, type)
                        VALUES (%s, %s, %s)"""
                cursor.execute(query, (username, password, type))

            connection.commit()
        return True

    def add_user_from_table(self, username, password, type):
        if self.add_user(username, password, type):
            flash("User added!")
            return redirect(url_for('users'))
        else:
            flash("There is already a user with that name! Use a different name")
            return redirect(url_for('users'))

    def sign_up(self, username, password):
        if self.add_user(username, password, 'User'):
            flash("Sign up successful! You can login as "+ username)
            return redirect(url_for('login'))
        else:
            flash("There is already a user with that name! Use a different name")
            return redirect(url_for('sign_up'))

    def login(self, username, password):
        with dbapi2.connect(self.dsn) as connection:
            cursor = connection.cursor()

            query = """SELECT id,type FROM users
                        WHERE username = %s and password = %s
                        """
            cursor.execute(query, (username, password))

            connection.commit()
            user = cursor.fetchone()
        if user:
            session['username'] = username
            flash("Login successful!")
            if(user[1] == 'Admin'):
                session['admin'] = True
                flash("You are an admin! You can modify users.")
                return redirect(url_for('users'))
            else:
                session['admin'] = False
                return redirect(url_for('home'))
        else:
            flash("User name or password is wrong!")
            return redirect(url_for('login'))

    def show_users(self):
        with dbapi2.connect(self.dsn) as connection:
            cursor = connection.cursor()

            query = "SELECT id, username, password, type FROM users"
            cursor.execute(query)
            users = cursor.fetchall()

        return render_template('user/users.html', users = sorted(users, key=lambda p: p[1]))

    def reset_table(self):
        with dbapi2.connect(self.dsn) as connection:
            cursor = connection.cursor()

            query = "DROP TABLE IF EXISTS users"
            cursor.execute(query)

            query = """CREATE TABLE users(
                        id serial PRIMARY KEY,
                        username text UNIQUE NOT NULL,
                        password text NOT NULL,
                        type text NOT NULL)"""
            cursor.execute(query)

            query = """INSERT INTO users (username, password, type)
                        VALUES ('admin', '3333', 'Admin')"""
            cursor.execute(query)

            connection.commit()
        return redirect(url_for('users'))

