Parts Implemented by Cemal Türkoğlu
===================================

The parts that I have implemented are the *Power Boat Racing* pages and functionalities related to users.


Power Boat Racing
-----------------
The power boat racing pages can be reached by clicking this button in the home page.

   .. image:: images/cemal/visit.png
      :scale: 80 %

Power boat racing pages locates under /drivers route. In the main page you can see some complex statistics
and all tables. There are 5 table: Drivers,Teams,Boats,League15,OldRaces. In table operation you can make
add,delete,update and resetting table


Adding
^^^^^^

To add a new driver, you need to enter a name,team and boat using the textboxes.Also click the *Add* button.

   .. image:: images/cemal/add.png
      :scale: 100 %
      :alt: Adding demonstration


As a result, the new driver you entered will be added to the database and the new list will be shown to you.




Deleting
^^^^^^^^

To delete a driver, click the circle to its left in the list. Then press the *Delete* button.

   .. image:: images/cemal/delete.png
      :scale: 100 %
      :alt: Deleting demonstration

   .. note:: If you try to break referencial integrity , it will not be allowed.

Then, the entry will be removed from the database and the resulting list will be displayed.

Updating
^^^^^^^^

To update the information of a competitor, select the comptitor in the same manner as deleting (by clicking the circle to its left) and then enter the information as you would in adding. After that, click the *Update* button and watch it happen.

   .. image:: images/cemal/update.png
      :scale: 100 %
      :alt: Updating demonstration

Information in the entry will be updated and shown back.

   .. note:: Again breaking referencial integrity is not allowed

Resetting the Table
^^^^^^^^^^^^^^^^^^^

Clicking the *Reset Table* button reverts any changes done to both the competitors and the teams table and fills them with default values. Not much has to be said about this function.

Tables
^^^^^^

All tables are listed in main page.Also from the left menu one of the table can be selected to display.
   Drivers

   .. image:: images/cemal/add.png
      :scale: 100 %
      :alt: The driver table

   Teams

   .. image:: images/cemal/teams.png
      :scale: 100 %
      :alt: The teams table

   Boats

   .. image:: images/cemal/boats.png
      :scale: 100 %
      :alt: The boats table

   League

   .. image:: images/cemal/league.png
      :scale: 100 %
      :alt: The league table

   OldRaces

   .. image:: images/cemal/oldraces.png
      :scale: 100 %
      :alt: The oldraces table
