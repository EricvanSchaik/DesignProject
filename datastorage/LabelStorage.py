import sqlite3


class LabelStorage:

    sql_new_label = "INSERT INTO labelInfo(Name, Color, Description) VALUES (?,?,?)"
    sql_add_label = "INSERT INTO labelData(Start_time, Label_name, Sensor_id) VALUES (?,?,?)"

    def __init__(self):
        self.conn = sqlite3.connect('database.db')

    def create_table(self):
        c = self.conn.cursor()
        c.execute("CREATE TABLE labelInfo (Name TEXT PRIMARY KEY, Color INTEGER, Description TEXT)")
        c.execute("CREATE TABLE labelData (Start_time REAL PRIMARY KEY, Label_name TEXT, Sensor_id TEXT)")
        self.conn.commit()
        self.conn.close()

    def new_label(self, name, color, desc):
        try:
            c = self.conn.cursor()
            c.execute(self.sql_new_label, (name, color, desc))
            self.conn.commit()
        except sqlite3.Error as e:
            # TODO: label name exists, give error message
            pass

    def add_label(self, time, name, sensor):
        try:
            c = self.conn.cursor()
            c.execute(self.sql_add_label, (time, name, sensor))
            self.conn.commit()
        except sqlite3.Error as e:
            # TODO: label at this time exists, give error message
            pass

    # TODO: return all labels for a certain sensor (for GUI), update label color/name


if __name__ == '__main__':
    l = LabelStorage()
    l.new_label("label1", 0, "test label")
    l.conn.commit()
