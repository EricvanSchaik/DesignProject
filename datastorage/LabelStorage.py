import sqlite3

sql_new_label = "INSERT INTO labelType(Name, Color, Description) VALUES (?,?,?)"
sql_del_label_type = "DELETE FROM labelType WHERE Name = ?"
sql_del_label_data_all = "DELETE FROM labelData WHERE Label_name = ?"
sql_del_label_data = "DELETE FROM labelData WHERE Start_time = ? AND Sensor_id = ?"
sql_add_label = "INSERT INTO labelData(Start_time, Label_name, Sensor_id) VALUES (?,?,?)"
sql_upd_name_type = "UPDATE labelType SET Name = ? WHERE Name = ?"
sql_upd_name_data = "UPDATE labelData SET Label_name = ? WHERE Label_name = ?"
sql_upd_color = "UPDATE labelType SET Color = ? WHERE Name = ?"
sql_upd_desc = "UPDATE labelType SET Description = ? WHERE Name = ?"
sql_change_label = "UPDATE labelData SET Label_name = ? WHERE Start_time = ?"


class LabelStorage:

    def __init__(self):
        # TODO: different location for different user projects?
        self.conn = sqlite3.connect('database.db')
        self.cur = self.conn.cursor()

    """Method for creating the necessary label tables in the database."""
    def create_tables(self):
        c = self.conn.cursor()
        c.execute("CREATE TABLE labelType (Name TEXT PRIMARY KEY, Color INTEGER, Description TEXT)")
        c.execute("CREATE TABLE labelData (Start_time REAL, Label_name TEXT, Sensor_id TEXT, "
                  "PRIMARY KEY(Start_time, Sensor_id))")
        self.conn.commit()

    """Creates a new label type given its name, color and description."""
    def new_label(self, name, color, desc):
        try:
            self.cur.execute(sql_new_label, (name, color, desc))
            self.conn.commit()
        except sqlite3.Error as e:
            # TODO: label name exists, give error message
            pass

    """Deletes a label type with the given name as well as all its usages."""
    def delete_label_type(self, name):
        self.cur.execute(sql_del_label_type, name)
        self.cur.execute(sql_del_label_data_all, name)
        self.conn.commit()

    """"Adds a label to the data of a sensor given the timestamp in the data, the name of the label that is used and the
        name of the sensor."""
    def add_label(self, time, name, sensor):
        try:
            self.cur.execute(sql_add_label, (time, name, sensor))
            self.conn.commit()
        except sqlite3.Error as e:
            # TODO: label at this time exists, give error message
            pass

    """Deletes a label linked to data, given its timestamp and sensor"""
    def delete_label(self, time, sens_id):
        self.cur.execute(sql_del_label_data, (time, sens_id))
        self.conn.commit()

    """Updates the name of an existing label type. This also updates the name of all the labels that were made using the 
       old name, linked to any data."""
    def update_label_name(self, old_name, new_name):
        self.cur.execute(sql_upd_name_type, (new_name, old_name))
        self.cur.execute(sql_upd_name_data, (new_name, old_name))
        self.conn.commit()

    """Updates the color of an existing label type."""
    def update_label_color(self, name, color):
        self.cur.execute(sql_upd_color, (color, name))
        self.conn.commit()

    """Updates the description of an existing label type."""
    def update_label_description(self, name, desc):
        self.cur.execute(sql_upd_desc, (desc, name))
        self.conn.commit()

    """Changes the label type of a label at a given timestamp in the data of a given sensor."""
    def change_label(self, time, name):
        self.cur.execute(sql_change_label, (name, time))
        self.conn.commit()

    """Returns all the labels for a given sensor."""
    def get_all_labels(self, sensor_id):
        # TODO
        pass


if __name__ == '__main__':
    l = LabelStorage()
    l.add_label(0, "label1", "sensor1")
    l.conn.commit()
