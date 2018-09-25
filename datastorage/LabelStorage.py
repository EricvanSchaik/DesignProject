import sqlite3
from typing import List, Tuple

sql_new_label = "INSERT INTO labelType(Name, Color, Description) VALUES (?,?,?)"
sql_del_label_type = "DELETE FROM labelType WHERE Name = ?"
sql_del_label_data_all = "DELETE FROM labelData WHERE Label_name = ?"
sql_del_label_data = "DELETE FROM labelData WHERE Start_time = ? AND Sensor_id = ?"
sql_add_label = "INSERT INTO labelData(Start_time, Label_name, Sensor_id) VALUES (?,?,?)"
sql_upd_name_type = "UPDATE labelType SET Name = ? WHERE Name = ?"
sql_upd_name_data = "UPDATE labelData SET Label_name = ? WHERE Label_name = ?"
sql_upd_color = "UPDATE labelType SET Color = ? WHERE Name = ?"
sql_upd_desc = "UPDATE labelType SET Description = ? WHERE Name = ?"
sql_change_label = "UPDATE labelData SET Label_name = ? WHERE Start_time = ? AND Sensor_id = ?"
sql_get_labels = "SELECT Start_time, Label_name FROM labelData WHERE Sensor_id = ?"


class LabelManager:

    def __init__(self, project_name: str):
        """
        :param project_name: The name of the current project
        """
        self._conn = sqlite3.connect('projects/' + project_name + '/project_data.db')
        self._cur = self._conn.cursor()

    def create_tables(self) -> None:
        """Method for creating the necessary label tables in the database."""
        c = self._conn.cursor()
        c.execute("CREATE TABLE labelType (Name TEXT PRIMARY KEY, Color INTEGER, Description TEXT)")
        c.execute("CREATE TABLE labelData (Start_time REAL, Label_name TEXT, Sensor_id TEXT, "
                  "PRIMARY KEY(Start_time, Sensor_id), FOREIGN KEY (Label_name) REFERENCES labelType(Name))")
        self._conn.commit()

    def add_label_type(self, name: str, color: int, desc: str) -> None:
        """
        Creates a new label type.

        :param name: The name of the new label type
        :param color: The color of the new label represented as an integer
        :param desc: The description of the label
        """
        try:
            self._cur.execute(sql_new_label, (name, color, desc))
            self._conn.commit()
        except sqlite3.Error as e:
            # TODO: label name exists, give error message
            pass

    def delete_label_type(self, name: str) -> None:
        """
        Deletes a label type.

        :param name: The name of the label type
        """
        self._cur.execute(sql_del_label_data_all, [name])
        self._cur.execute(sql_del_label_type, [name])
        self._conn.commit()

    def add_label(self, time: float, name: str, sensor: str) -> None:
        """
        Adds a label to the data of a sensor.

        :param time: The timestamp in the sensor-data at which the label starts
        :param name: The name of the label type that is used
        :param sensor: The sensor ID belonging to the data
        """
        try:
            self._cur.execute(sql_add_label, (time, name, sensor))
            self._conn.commit()
        except sqlite3.Error as e:
            # TODO: label at this time exists, give error message
            pass

    def delete_label(self, time: float, sens_id: str) -> None:
        """
        Deletes a label linked to data.

        :param time: The timestamp at which the label starts
        :param sens_id: The sensor ID for which the label is made
        """
        self._cur.execute(sql_del_label_data, (time, sens_id))
        self._conn.commit()

    def update_label_name(self, old_name: str, new_name: str) -> None:
        """
        Updates the name of an existing label type. This also updates the name of all the labels that were made using
        the old name.

        :param old_name: The name of the label type that has to be changed
        :param new_name: The name that the label type should get
        """
        self._cur.execute(sql_upd_name_data, (new_name, old_name))
        self._cur.execute(sql_upd_name_type, (new_name, old_name))
        self._conn.commit()

    def update_label_color(self, name: str, color: int) -> None:
        """
        Updates the color of an existing label type.

        :param name: The name of the label type
        :param color: The new color that the label type should get, represented as an integer
        """
        self._cur.execute(sql_upd_color, (color, name))
        self._conn.commit()

    def update_label_description(self, name: str, desc: str) -> None:
        """
        Updates the description of an existing label type.

        :param name: The name of the label type
        :param desc: The new description that the label type should get
        """
        self._cur.execute(sql_upd_desc, (desc, name))
        self._conn.commit()

    def change_label(self, time: float, name: str, sens_id: str) -> None:
        """
        Changes the label type of a data-label.

        :param time: The timestamp of the label
        :param name: The name of the label type into which the label should be changed
        :param sens_id: The sensor ID belonging to this label
        """
        self._cur.execute(sql_change_label, (name, time, sens_id))
        self._conn.commit()

    def get_all_labels(self, sensor_id: str) -> List[Tuple[float, str]]:
        """
        Returns all the labels for a given sensor.

        :param sensor_id: The sensor ID of the sensor for which the labels need to be returned
        :return: List of all labels belonging to the sensor
        """
        self._cur.execute(sql_get_labels, [sensor_id])
        return self._cur.fetchall()
