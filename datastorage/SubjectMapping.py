import sqlite3

sql_add_subject = "INSERT INTO subject_map (Name) VALUES (?)"
sql_change_sensor = "UPDATE subject_map SET Sensor = ? WHERE Name = ?"
sql_change_start_date = "UPDATE subject_map SET Start_date = ? WHERE Name = ?"
sql_change_end_date = "UPDATE subject_map SET End_date = ? WHERE Name = ?"


class SubjectManager:

    def __init__(self):
        self._conn = sqlite3.connect('database.db')
        self._cur = self._conn.cursor()

    def create_table(self):
        """Method for creating the necessary subject mapping table."""
        self._cur.execute("CREATE TABLE subject_map (Name TEXT, Sensor TEXT, Start_date TEXT, End_date TEXT)")
        self._conn.commit()

    def add_subject(self, name):
        """
        Adds a new subject.

        :param name: The name of the new subject
        """
        self._cur.execute(sql_add_subject, [name])
        self._conn.commit()

    def change_sensor(self, name, sens_id):
        """
        Changes the sensor mapped to a subject.

        :param name: The name of the subject to map this sensor to
        :param sens_id: The sensor ID of the sensor
        """
        self._cur.execute(sql_change_sensor, (sens_id, name))
        self._conn.commit()

    def change_start_date(self, name, date):
        """
        Changes the start date for a subject.

        :param name: The name of the subject
        :param date: The start date
        """
        self._cur.execute(sql_change_start_date, (date, name))
        self._conn.commit()

    def change_end_date(self, name, date):
        """
        Changes the end date for a subject.

        :param name: The name of the subject
        :param date: The end date
        """
        self._cur.execute(sql_change_end_date, (date, name))
        self._conn.commit()

    # TODO: allow user to add and manipulate own columns

