Parts Implemented by Turker Unlu
================================

Divers
======
This section of the page is used for managing information about dive sporters.

.. figure:: images/divertable.png
      :scale: 30 %
      :alt: Screenshot of Divers Table

      Fig. 1.1: Screenshot of Divers Table

Information about divers is listed on the screen.
Data table consist of ID, name, age and country information of the sporter.
ID is unique sporter ID of a sporter.
Name and age are sporter's personal information.
Country is the country sporter represents.


Operations add, delete, update and find can be done from this section alone.


Competitions
============
This section of the page is used for managing information about diving competitions.

.. figure:: images/competitiontable.png
      :scale: 30 %
      :alt: Screenshot of Competition Table

      Fig. 1.2: Screenshot of Competition Table

Information about diving competitions is listed on the screen.
Data table consist of competition ID, winner sporter ID and the year which competition is done.
CompetitionID is the unique ID of a diving competition.
WinnerID is the ID of the sporter who won the competition.
Year is the date which the competition held.

Operations add, delete, update and find can be done from this section alone.
The sporter with the ID number winnerID must exist in order to add a new competition.

Records
=======
This section of the page is used for managing information about a sporter record at a specific competition.
For example sporter "DiverID" jumped from 5 meter at competition "CompetitionID"

.. figure:: images/recordtable.png
      :scale: 30 %
      :alt: Screenshot of Record Table

      Fig. 1.3: Screenshot of Record Table

Information about record is listed on the screen.
Data table consist of competitionID, DiverID and record.
CompetitionID is the unique ID of the competition.
DiverID is the unique ID of the sporter.
Record is the amount of height sporter dived from.



Operations add, delete, update and find can be done from this section alone.
The sporter with the ID number DiverID and competition with the CompetitionID must exist in order to add a new record.