Parts Implemented by Ercan Alp Serteli
======================================

The parts that I have implemented are the *Underwater Photography* pages and functionalities related to users.


Underwater Photography
----------------------
The underwater photography pages can be reached by clicking this button in the home page.

   .. image:: images/ercan/visit_button.PNG
      :scale: 80 %
      :alt: Visit Underwater Photography Button

Or from this menu item in the navigation bar from any other page.

   .. image:: images/ercan/navbar_button.PNG
      :scale: 100 %
      :alt: Underwater Photography navigation bar item

Now that you clicked one of them, you are in the *Competitors* page of Underwater Photography.

   .. image:: images/ercan/competitor_page.PNG
      :scale: 100 %
      :alt: Underwater Photography competitors page

From the *Categories* menu you see on the left, it is possible to navigate between the two pages of Underwater Photography: *Competitors* and *Teams*

What you see in the middle is a representation of the underlying Competitors database table. It lists the information of the existing competitors in the table and allows anyone to modify the table via adding, updating or deleting entries or via resetting the table to its default state.

The entries are sorted according to the alphabetical order of their first names.

Adding
^^^^^^

To add a new competitor, you need to enter a name and a surname using the textboxes. Then you need to select a country and a role using the dropdown menus and click the *Add* button.

   .. image:: images/ercan/add.PNG
      :scale: 100 %
      :alt: Adding demonstration

   .. note:: To add a competitor from a team of some non-existing country, you first need to add the team from the *Teams* page. On the other hand, the team roles are fixed. They cannot be changed and a new role cannot be added.

As a result, the new competitor you entered will be added to the database and the new list will be shown to you.

   .. image:: images/ercan/add_newlist.PNG
      :scale: 100 %
      :alt: New list after the adding operation

   .. note:: If you leave the name or the surname boxes empty, it will not be added and the page will show you a warning message

Deleting
^^^^^^^^

To delete a competitor, click the circle to its left in the list. Then press the *Delete* button.

   .. image:: images/ercan/delete.PNG
      :scale: 100 %
      :alt: Deleting demonstration

Then, the entry will be removed from the database and the resulting list will be displayed.

Updating
^^^^^^^^

To update the information of a competitor, select the comptitor in the same manner as deleting (by clicking the circle to its left) and then enter the information as you would in adding. After that, click the *Update* button and watch it happen.

   .. image:: images/ercan/update.PNG
      :scale: 100 %
      :alt: Updating demonstration

Information in the entry will be updated and shown back.

   .. image:: images/ercan/update_newlist.PNG
      :scale: 100 %
      :alt: New list after the updating operation

Resetting the Table
^^^^^^^^^^^^^^^^^^^

Clicking the *Reset Table* button reverts any changes done to both the competitors and the teams table and fills them with default values. Not much has to be said about this function.

Teams Page
^^^^^^^^^^

When you click the *Teams* button in the left menu, you will end up in this page.

   .. image:: images/ercan/teams.PNG
      :scale: 100 %
      :alt: The teams page

What you see is the same structure as the Competitors page, but with a smaller table. That is the teams list. Teams only have a *Country* field and an ID, since competitions are held with national teams. In fact, the competitors list you have seen before is taking its country information from this table.

All the operations as in the Competitors page are possible here as well, and they all work the same.

   .. note:: If you try to delete a team that has members in the competitors list, you cannot do it. To do this, delete the members from the Competitors page first.

User Operations
---------------

The website supports basic user functionalities such as signing up, logging in, logging out. Modifying the information of users is also possible for admin type accounts.

Signing up
^^^^^^^^^^

You can move to the sign up page by clicking the *Sign Up* button from the navigation bar.

   .. image:: images/ercan/sign_up_button.PNG
      :scale: 80 %
      :alt: The sign up button

In the sign up page, enter a username and a password and press the *Sign Up* button. This will enable you to login using those credentials. You will be redirected to the Login page, since you will probably want to login after signing up.

   .. image:: images/ercan/sign_up_page.PNG
      :scale: 100 %
      :alt: The sign up page

   .. note:: If you try to sign up with a blank username or password, the page will warn you. Also a different warning message will be shown if you enter an username that already exists in the system.

   .. warning:: Do not use a real password to sign up because it is not secure, at all. Literally anyone can see your information if they want to.

Logging in
^^^^^^^^^^

You can get to the login page by clicking the *Login* button from the navigation bar.

   .. image:: images/ercan/login_button.PNG
      :scale: 80 %
      :alt: The login button

You can also get redirected here by signing up.

You will be given a default admin account's credentials in case you want to try out being an admin. You can login using that or your own credentials.

   .. note:: Any user who signs up is a *User* type user. To change a user's type, you have to be logged in as an *Admin* type user.

   .. image:: images/ercan/login_page.PNG
      :scale: 100 %
      :alt: The login page

   .. note:: If you try to login using wrong information, the page will show you a message and let you try again.

Logging out
^^^^^^^^^^^

Once you are logged in, a new item appears in the navigation bar while the sign up and login items disappear. This new button lets you log out from the system.

   .. image:: images/ercan/logout_button.PNG
      :scale: 80 %
      :alt: The log out button

Once you click it, you will no longer be logged in.

Users Page
^^^^^^^^^^

If you login as an admin, you will be directed to the *Users* page. You can also go there using the navigation bar item that only shows up if you are an admin.

   .. image:: images/ercan/users_button.PNG
      :scale: 80 %
      :alt: The button to get to the users page

In the users page, you will see the list of users. You can add, delete or update users or you can reset the users table. The operations are identical to the ones in the Underwater Photography pages.

   .. image:: images/ercan/users_page.PNG
      :scale: 80 %
      :alt: The button to get to the users page