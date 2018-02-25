Parts Implemented by Ercan Alp Serteli
======================================

I have implemented three database tables: competitors, teams and users. The first two tables are regarding the Underwater Photography and they are managed by the *UWP* class. The users table is managed by the *Users* class.

Here, I will explain everything technical that is related to these entities including SQL code, Python code and HTML code.

UWP Class
---------

The *UWP* class includes all the methods that are needed to manage the *competitor* and *team* tables

init Method
^^^^^^^^^^^
   .. code-block:: python

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

This is the method that gets called when the UWP object is created. It gets the dsn by a parameter and saves it in its field for later use. Then it attempts to create the role type and the two tables if they do not exist. These SQL statements do nothing if the database has been initialized properly. They are there in case the application might be needed to run in a new database or some of the tables are dropped for some reason.

show_page_comp Method
^^^^^^^^^^^^^^^^^^^^^
   .. code-block:: python

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

This method is called when a HTTP GET is requested for the competitors page. It gets the data that is needed to construct the competitor list from the database and renders the page with that data as the parameter. It sorts the list by the first names before using it.
In the first select statement, we get the data of all competitors by joining the competitor and team tables over team_id. This way, we can display the countries that each competitor belongs to as well as their other attributes.
The second select statement is used to get all the countries from the team table so that they can be shown in a dropdown menu when adding or updating rows.
The last select statement gets the roles that are used in the competitor table for a dropdown menu again. I just noticed that this is a very bad way of doing this. It should get them from the type instead of the table. However it is too late to fix this now.

show_page_team Method
^^^^^^^^^^^^^^^^^^^^^

   .. code-block:: python

      def show_page_team(self):
        with dbapi2.connect(self.dsn) as connection:
            cursor = connection.cursor()

            query = """SELECT team.id, country, COUNT(competitor.id)
                        FROM team LEFT JOIN competitor  ON team_id = team.id
                        GROUP BY team.id"""

            cursor.execute(query)
            teams = cursor.fetchall()

        return render_template('uwp/uwp_teams.html', teams = teams)

This method is for showing the teams page. It gets the team data and the number of competitors in each team by joining the team and competitor tables. Left join is used because we want to get all the teams in the list whether they have any members or not.

add_competitor Method
^^^^^^^^^^^^^^^^^^^^^

   .. code-block:: python

      query = """INSERT INTO competitor (name, surname, role, team_id)
                     SELECT %s, %s, %s, team.id
                     FROM team WHERE team.country = %s
                     """
      cursor.execute(query, (name, surname, role, country))

   .. note:: From now on, in most methods only a relevant part of the method is pasted

This method is used to insert a row into the competitor table. The team_id needed is selected from team using the country.

delete_competitor Method
^^^^^^^^^^^^^^^^^^^^^^^^

   .. code-block:: python

      query = "DELETE FROM competitor WHERE id = %s"
      cursor.execute(query, (id,))

This is a very simple method as it only gets an id and deletes the row with that id from the table.

update_competitor Method
^^^^^^^^^^^^^^^^^^^^^^^^

   .. code-block:: python

      query = """UPDATE competitor
               SET name=%s,surname=%s,role=%s,team_id=subquery.id
               FROM (SELECT team.id FROM team WHERE team.country = %s)
               AS subquery
               WHERE competitor.id = %s"""
      cursor.execute(query, (name, surname, role, country, id))

This method updates a row in the competitor table with the new data. It uses the name, surname and role inputs directly while it gets the team_id using a subquery that uses the country input.

add_team Method
^^^^^^^^^^^^^^^

   .. code-block:: python

      query = """INSERT INTO team (country)
               VALUES (%s)"""
      cursor.execute(query, (country,))

Self explanatory method that adds a new row to the team table.

update_team Method
^^^^^^^^^^^^^^^^^^

   .. code-block:: python

      query = """UPDATE team
                  SET country = %s
                  WHERE id = %s"""
      cursor.execute(query, (country, id))

Self explanatory method that updates new row in the team table.

delete_team Method
^^^^^^^^^^^^^^^^^^

   .. code-block:: python

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

This method is used for deleting a row from the team table. However, it has to check if there are any members of the team before attempting to delete it. So, it gets the number of members in a team in the same way show_page_team does. Then checks if the number is 0. If it is, then it is deleted. Otherwise, it pops a flash message and reloads the page.

reset_table Method
^^^^^^^^^^^^^^^^^^

   .. code-block:: python

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

This method drops the team and competitor tables, creates them again and fills them with default data.

Users Class
-----------

This class has all the methods that are needed for managing the users table.

init Method
^^^^^^^^^^^

   .. code-block:: python

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

The init method saves the dsn in a field and attempts to create the users table if it does not exists. Then it tries to insert an admin account into it if one does not exist.

delete_user Method
^^^^^^^^^^^^^^^^^^

   .. code-block:: python

      query = "DELETE FROM users WHERE id = %s"
      cursor.execute(query, (id,))

This is a self explanatory method that deletes a row from the users table by an id.

update_user Method
^^^^^^^^^^^^^^^^^^

   .. code-block:: python

      query = """UPDATE users
                  SET username=%s,password=%s,type=%s
                  WHERE id = %s"""
      cursor.execute(query, (username, password, type, id))

This is a self explanatory method that updates a row in the users table with the given data.

add_user Method
^^^^^^^^^^^^^^^

   .. code-block:: python

      query = """SELECT username FROM users
                  WHERE username = %s"""
      cursor.execute(query, (username,))
      if cursor.fetchall():
          return False
      else:
          query = """INSERT INTO users (username, password, type)
                  VALUES (%s, %s, %s)"""
          cursor.execute(query, (username, password, type))

This is the method that adds rows into the users table. However, first it checks if there is a row with that username and if there is, it returns false because the username must be unique. If there is no match, the user is added. This is a lower level method that is called through higher level methods.

add_user_from_table Method
^^^^^^^^^^^^^^^^^^^^^^^^^^

   .. code-block:: python

      def add_user_from_table(self, username, password, type):
        if self.add_user(username, password, type):
            flash("User added!")
            return redirect(url_for('users'))
        else:
            flash("There is already a user with that name! Use a different name")
            return redirect(url_for('users'))

This method is used to try and add a user from the users page by an admin. It calls the add_user method explained above.

sign_up Method
^^^^^^^^^^^^^^

   .. code-block:: python

     if self.add_user(username, password, 'User'):
         flash("Sign up successful! You can login as "+ username)
         return redirect(url_for('login'))
     else:
         flash("There is already a user with that name! Use a different name")
         return redirect(url_for('sign_up'))

This method is used to try and add a user from the sign up page. It calls the add_user method.

login Method
^^^^^^^^^^^^

   .. code-block:: python

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

This method handles the logging in functionality. It executes a select statement and checks if anything returned. If so, it assigns the username to the 'username' key of the session and checks if the user type is admin. If it is, then the 'admin' key of the session is assigned true. These are the values that are used to determine which user can do/see what.

If nothing is returned from the select, a flash message is shown to the user.

show_users Method
^^^^^^^^^^^^^^^^^

   .. code-block:: python

      def show_users(self):
        with dbapi2.connect(self.dsn) as connection:
            cursor = connection.cursor()

            query = "SELECT id, username, password, type FROM users"
            cursor.execute(query)
            users = cursor.fetchall()

        return render_template('user/users.html', users = sorted(users, key=lambda p: p[1]))

This is simply the method that is called when an admin wants to open the users page. All users are selected and sorted according to their usernames.

reset_table Method
^^^^^^^^^^^^^^^^^^

   .. code-block:: python

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

This method drops the users table and creates it again. Then it adds the default admin user to the table.

Methods in server.py
--------------------

server.py is the main part of our application. It is the file where the methods that flask calls when it gets a request, are in. These methods create instances of a class and call its methods according to the type of the request.

uwp_comp Method
^^^^^^^^^^^^^^^

   .. code-block:: python

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

This method handles the competitor page requests. If the HTTP method is GET, it calls show_page_comp(). If it is POST, then it determines the kind (add/update/delete/reset), gets the required inputs from the form fields and does some input checking before calling the appropriate function. In add, it checks if the name and surname boxes are not empty, in delete it checks if any one of the rows is selected and in update it checks both of those conditions.

uwp_team Method
^^^^^^^^^^^^^^^

   .. code-block:: python

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

This method handles the team page requests. It works almost identically to the uwp_comp method, so check it out for any explanations.

users method
^^^^^^^^^^^^

   .. code-block:: python

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

This method handles the users page requests. First thing it does is check if the user is an admin. If it is, then the method works similarly to the uwp_comp method. Otherwise, the user is redirected to the home_page.

logout Method
^^^^^^^^^^^^^

    .. code-block:: python

      @app.route('/logout', methods=['GET'])
      def logout():
          flash("Logged out!")
          session.pop('username', None)
          session.pop('admin', None)
          return redirect(url_for('home'))

This method simply logs the user out.

login Method
^^^^^^^^^^^^

    .. code-block:: python

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

This is the method that handles the login page requests. If the request is GET, it justs renders the html template. Otherwise it is a POST, so it gets the username and password and calls the login method of Users class.

sign_up Method
^^^^^^^^^^^^^^

    .. code-block:: python

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

This is the method that handles the sign up page requests. It is similar to the login method but it checks if the username or password boxes are empty before calling the sign_up method of Users.

HTML Templates
--------------

These are the files that are rendered to create what the user sees in their browser. They are templates because they have parameters which we can fill up in run time.

uwp_comp.html
^^^^^^^^^^^^^

    .. code-block:: html

      {% block body %}
      <h1> Competitor List </h1>
      <form action="{{ url_for('uwp_comp') }}" method="post">
         <table>
            <tr>
               <th> </th>
               <th>Name</th>
               <th>Surname</th>
               <th>Country</th>
               <th>Role</th>
            </tr>
            {% for id, name, surname, country, role in competitors %}
               <tr>
                  <td> <input type="radio" name="select"value="{{id}}" /> </td>
                  <td> {{name}} </td>
                  <td> {{surname}} </td>
                  <td> {{country}} </td>
                  <td> {{role}} </td>
                </tr>
            {% endfor %}
            <tr>
               <td> </td>
               <td> <input type="text" name="Name" value="" placeholder="Name" /> </td>
               <td> <input type="text" name="Surname" value="" placeholder="Surname"/> </td>
               <td> <select name="Country">
                  {% for country in countries %}
                    <option value="{{country}}">{{country}}</option>
                  {% endfor %}
                  </select>
               </td>
               <td> <select name="Role">
                   {% for role in roles %}
                    <option value="{{role}}">{{role}}</option>
                  {% endfor %}
                  </select>
               </td>
             </tr>
         </table>
         <input type="submit" name="Add"value="Add" />
         <input type="submit" name="Delete"value="Delete" />
         <input type="submit" name="Update"value="Update" />
         <input type="submit" name="Reset"value="Reset Table" />
      </form>

      <footer>Ercan Alp Serteli</footer>
      {% endblock %}

This is the main body of the template for the underwater photography competitors page. There is a table that is filled with the values from *competitors*. Also the values of country and role selections are taken from parameters. Name and surname data is taken using text boxes and add, update, delete, reset table operations are determined by checking which submit has been pressed.

uwp_teams.html
^^^^^^^^^^^^^^

    .. code-block:: html

      {% block body %}
      <h1> Team List </h1>
      <form action="{{ url_for('uwp_team') }}" method="post">
         <table>
            <tr>
               <th> </th>
               <th>Country</th>
               <th>Number of members</th>
            </tr>
            {% for id, country, num_mem in teams %}
               <tr>
                  <td> <input type="radio" name="select"value="{{id}}" /> </td>
                  <td> {{country}} </td>
                  <td> {{num_mem}} </td>
                </tr>
            {% endfor %}
            <tr>
               <td> </td>
               <td> <input type="text" name="Country" value="" placeholder="Country"/>   </td>
             </tr>
         </table>
         <input type="submit" name="Add"value="Add" />
         <input type="submit" name="Delete"value="Delete" />
         <input type="submit" name="Update"value="Update" />
      </form>

      <footer>Ercan Alp Serteli</footer>
      {% endblock %}

This is the template for the underwater photography teams page. It works very similarly to the uwp_comp page

login.html
^^^^^^^^^^

    .. code-block:: html

      <h1>Login</h1>
      <p> To login as an example admin account: User name = admin, Password = 3333 </p>
      <div class="jumbotron">
      <form class="form-login" action="{{ url_for('login') }}" method="post">
          <label for="username" class="sr-only">Username</label>
          <input type="username" name="username" id="username" class="form-control" placeholder="User Name">
          <label for="password" class="sr-only">Password</label>
          <input type="password" name="password" id="password" class="form-control" placeholder="Password">
          <input type="submit" name="Login" value="Login" />
      </form>
      </div>

This is the template for the login page. Bootstrap classes are used for styling. A simple form with two text boxes and a submit button.

signup.html
^^^^^^^^^^^

    .. code-block:: html

      <h1>Sign Up</h1>
      <div class="jumbotron">
      <form class="form-signup" action="{{ url_for('sign_up') }}" method="post">
          <label for="username" class="sr-only">Username</label>
          <input type="username" name="username" id="username" class="form-control" placeholder="User Name">
          <label for="password" class="sr-only">Password</label>
          <input type="password" name="password" id="password" class="form-control" placeholder="Password">
          <input type="submit" name="SignUp" value="Sign Up" />
      </form>
      </div>

This is the template for the signup page. Almost identical to the login page.

users.html
^^^^^^^^^^

    .. code-block:: html

      <h1> User List </h1>
      <form action="{{ url_for('users') }}" method="post">
         <table>
            <tr>
               <th> </th>
               <th>User Name</th>
               <th>Password</th>
               <th>Type</th>
            </tr>
            {% for id, username, password, type in users %}
               <tr>
                  <td> <input type="radio" name="select"value="{{id}}" /> </td>
                  <td> {{username}} </td>
                  <td> {{password}} </td>
                  <td> {{type}} </td>
                </tr>
            {% endfor %}
            <tr>
               <td> </td>

               <td><input type="text" name="UserName" value="" placeholder="User Name" /></td>
               <td> <input type="text" name="Password" value="" placeholder="Password"/> </td>
               <td> <input type="text" name="UserType" value="" placeholder="User Type"/> </td>
             </tr>
         </table>
         <input type="submit" name="Add"value="Add" />
         <input type="submit" name="Delete"value="Delete" />
         <input type="submit" name="Update"value="Update" />
         <input type="submit" name="Reset"value="Reset Table" />
      </form>

This is the template for the users page. This is the template for the underwater photography teams page. It works very similarly to the uwp_comp and uwp_team pages