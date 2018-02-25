import psycopg2 as dbapi2
from flask import render_template
from flask import redirect
from flask import url_for

class Diver:
    def __init__(self, diverID, name, age, country):
        self.diverID = diverID
        self.name = name
        self.age = age
        self.country = country


class Competition:
    def __init__(self, competitionID, winnerID, year):
        self.competitionID = competitionID
        self.winnerID = winnerID
        self.year = year

class Record:
    def __init__(self, competitionID, diverID, record):
        self.competitionID = competitionID
        self.diverID = diverID
        self.record = record

def ValidateInput(data, table):
    if table == 1:
        int(data.diverID)
        int(data.age)
    elif table == 2:
        int(data.competitionID)
        int(data.winnerID)
        int(data.year)
    elif table == 3:
        int(data.competitionID)
        int(data.diverID)
        int(data.record)


class DiverStore:
    def __init__(self, dbf):
        self.dbf = dbf

    def add_diver(self, data, table):
        try:
            ValidateInput(data, table)
        except ValueError:
            return render_template('Diving/InvalidValue.html', divers=divers)

        with dbapi2.connect(self.dbf) as connection:
            cursor = connection.cursor()
            query = ""

            if table == 1:
                query = """INSERT INTO DIVER (DIVERID, NAME, AGE, COUNTRY)
                            VALUES ('%s', '%s', '%s', '%s')""" % (data.diverID, data.name, data.age, data.country)
            elif table == 2:
                query = """INSERT INTO COMPETITION (COMPETITIONID, WinnerID, YEAR)
                            VALUES ('%s', '%s', '%s')""" % (data.competitionID, data.winnerID, data.year)
            elif table == 3:
                query = """INSERT INTO RECORD (COMPETITIONID, DIVERID, Record)
                            VALUES ('%s', '%s', '%s')""" % (data.competitionID, data.diverID, data.record)

            cursor.execute(query)
            connection.commit()
            return redirect(url_for('diving'))


    def delete_diver(self, id, table):
        with dbapi2.connect(self.dbf) as connection:
            cursor = connection.cursor()
            query = ""

            if table == 1:
                query = "DELETE FROM DIVER WHERE (DIVERID = '%s')" %(id)
            elif table == 2:
                query = "DELETE FROM COMPETITION WHERE (COMPETITIONID = '%s')" %(id)
            elif table == 3:
                ids = id.split('-')
                query = "DELETE FROM RECORD WHERE ((COMPETITIONID = '%s') AND (DIVERID = '%s'))" %(ids[0], ids[1])

            cursor.execute(query)
            connection.commit()
            return redirect(url_for('diving'))


    def update_diver(self, data, id, table):
        try:
            ValidateInput(data, table)
        except ValueError:
            return render_template('Diving/InvalidValue.html', divers=divers)

        with dbapi2.connect(self.dbf) as connection:
            cursor = connection.cursor()
            query = ""

            if table == 1:
                query = """UPDATE DIVER
                            SET DIVERID='%s', NAME='%s', AGE='%s', COUNTRY='%s'
                            WHERE (DIVERID = '%s')""" % (data.diverID, data.name, data.age, data.country, id)
            elif table == 2:
                query = """UPDATE COMPETITION
                            SET COMPETITIONID='%s', WinnerID='%s', YEAR='%s'
                            WHERE (COMPETITIONID = '%s')""" % (data.competitionID, data.winnerID, data.year, id)
            elif table == 3:
                ids = id.split('-')
                query = """UPDATE DIVER
                            SET COMPETITIONID='%s', DIVERID='%s', RECORD='%s'
                            WHERE ((COMPETITIONID = '%s') AND (DIVERID = '%s'))""" % (data.competitionID, data.diverID, data.record, ids[0], ids[1])

            cursor.execute(query)
            connection.commit()
            return redirect(url_for('diving'))


    def find_diver(self, data, table):
        with dbapi2.connect(self.dbf) as connection:
            cursor = connection.cursor()
            query = ""

            if table == 1:
                if data.diverID == '':
                    data.diverID = '-1'
                if data.age == '':
                    data.age = '-1'

                data.name = data.name.upper()
                data.country = data.country.upper()
                query = """SELECT DIVERID, NAME, AGE, COUNTRY FROM DIVER
                            WHERE (
                            (('%s' = '-1') OR (DIVERID = '%s'))
                            AND( ('%s' = '' ) OR (UPPER(NAME) LIKE '%s') )
                            AND( ('%s' = '-1') OR (AGE = '%s') )
                            AND( ('%s' = '' ) OR (UPPER(COUNTRY) = '%s') )
                            )"""% (data.diverID, data.diverID, data.name, data.name+'%', data.age, data.age, data.country, data.country)
                cursor.execute(query)
                divers = cursor.fetchall()
                return render_template('Diving/searchdiver.html', divers=divers)

            elif table == 2:
                if data.competitionID == '':
                    data.competitionID = '-1'
                if data.winnerID == '':
                    data.winnerID == '-1'
                if data.year == '':
                    data.year == '-1'
                query = """SELECT * FROM COMPETITION
                            WHERE (
                            (('%s' = '-1') OR (COMPETITIONID = '%s'))
                            AND( ('%s' = '-1') OR (WinnerID = '%s') )
                            AND( ('%s' = '-1') OR (YEAR = '%s') )
                            )"""% (data.competitionID, data.competitionID, data.winnerID, data.winnerID, data.year, data.year)
                cursor.execute(query)
                competitions = cursor.fetchall()
                return render_template('Diving/searchcompetition.html', competitions=competitions)

            elif table == 3:
                if data.competitionID == '':
                    data.competitionID = '-1'
                if data.diverID == '':
                    data.diverID = '-1'
                if data.record == '':
                    data.record = '-1'
                query = """SELECT * FROM RECORD
                            WHERE (
                            (('%s' = '-1') OR (COMPETITIONID = '%s'))
                            AND( ('%s' = '-1') OR (DIVERID = '%s') )
                            AND( ('%s' = '-1') OR (RECORD = '%s') )
                            )"""% (data.competitionID, data.competitionID, data.diverID, data.diverID, data.record, data.record)
                cursor.execute(query)
                records = cursor.fetchall()
                return render_template('Diving/searchrecord.html', records=records)

    def create_tables(self):
        with dbapi2.connect(self.dbf) as connection:
            cursor = connection.cursor()
            query = """CREATE TABLE IF NOT EXISTS DIVER (
                        DIVERID INTEGER PRIMARY KEY NOT NULL,
                        NAME text,
                        AGE INTEGER,
                        COUNTRY text)"""
            cursor.execute(query)
#
            query = """CREATE TABLE IF NOT EXISTS COMPETITION (
                        COMPETITIONID INTEGER PRIMARY KEY NOT NULL,
                        WinnerID INTEGER REFERENCES DIVER(DIVERID) ON DELETE RESTRICT ON UPDATE CASCADE,
                        YEAR INTEGER)"""
            cursor.execute(query)

            query = """CREATE TABLE IF NOT EXISTS RECORD (
                        COMPETITIONID INTEGER REFERENCES COMPETITION(COMPETITIONID) ON DELETE RESTRICT ON UPDATE CASCADE,
                        DIVERID INTEGER REFERENCES DIVER(DIVERID) ON DELETE RESTRICT ON UPDATE CASCADE,
                        RECORD INTEGER DEFAULT NULL,
                        PRIMARY KEY(COMPETITIONID, DIVERID))"""
            cursor.execute(query)

            connection.commit()

    def firstrun(self):
        self.create_tables()
        with dbapi2.connect(self.dbf) as connection:
            cursor = connection.cursor()

            #  get all divers
            query = "SELECT * FROM DIVER ORDER BY DIVERID"
            cursor.execute(query)
            divers = cursor.fetchall()

            #  get all competitions
            query = "SELECT * FROM COMPETITION ORDER BY COMPETITIONID"
            cursor.execute(query)
            competitions = cursor.fetchall()

            #  get all records
            query = "SELECT * FROM RECORD ORDER BY COMPETITIONID"
            cursor.execute(query)
            records = cursor.fetchall()

            #return render_template('diving.html', diverall=diverall, competitionall=competitionall, recordall=recordall)
            return render_template('Diving/diving.html', divers=divers, competitions=competitions, records=records)



    def recreate(self):
        with dbapi2.connect(self.dbf) as connection:
            cursor = connection.cursor()


            query = "DROP TABLE IF EXISTS RECORD"
            cursor.execute(query)
            query = "DROP TABLE IF EXISTS COMPETITION"
            cursor.execute(query)
            query = "DROP TABLE IF EXISTS DIVER"
            cursor.execute(query)

            connection.commit()

            self.create_tables()

            query = """INSERT INTO DIVER (DIVERID, NAME, AGE, COUNTRY)
                        VALUES
                        (1, 'Peng Bo', 34, 'CN'),
                        (2, 'Alexander Dobroskok', 33, 'RU'),
                        (3, 'Alexandre Despatie', 30, 'CA'),
                        (4, 'Ken Terauchi', 35, 'JP'),
                        (5, 'Troy Dumais', 35, 'US'),
                        (6, 'Dmitri Sautin', 41, 'RU'),
                        (7, 'Wang Tianling', 30, 'CN'),
                        (8, 'He Cong', 28, 'CN'),
                        (9, 'Zhou Luxin', 27, 'CN'),
                        (10, 'Lin Yue', 24, 'CN'),
                        (11, 'Tom Daley', 21, 'UK'),
                        (12, 'Qui Bo', 22, 'CN'),
                        (13, 'Chen Roulin', 23, 'CN'),
                        (14, 'Hu Yadan', 19, 'CN'),
                        (15, 'Paola Espinosa', 30, 'MX'),
                        (20, 'Gleb Galperin', 30, 'RU')"""
            cursor.execute(query)

            query = """INSERT INTO COMPETITION (COMPETITIONID, WinnerID, YEAR)
                        VALUES
                        (1, 6, 2001),
                        (2, 2, 2003),
                        (3, 3, 2005),
                        (4, 20, 2007),
                        (5, 11, 2009),
                        (6, 13, 2011)
                        """
            cursor.execute(query)

            query = """INSERT INTO RECORD (COMPETITIONID, DIVERID, RECORD)
                        VALUES
                        (1, 6, 3),
                        (2, 2, 3),
                        (3, 3, 3),
                        (4, 20, 10),
                        (5, 11, 10),
                        (6, 13, 10)"""
            cursor.execute(query)
            connection.commit()