import sqlite3

sql_add_camera = "INSERT INTO cameras(Name, SN) VALUES (?,?)"
sql_delete_camera = "DELETE FROM cameras WHERE Name = ?"


class CameraInfo:

    def __init__(self):
        self.conn = sqlite3.connect('database.db')
        self.cur = self.conn.cursor()

    """Creates the necessary cameras table in the database"""
    def create_table(self):
        self.cur.execute("CREATE TABLE cameras (Name TEXT PRIMARY KEY, SN TEXT)")
        self.conn.commit()

    """Adds a camera to the table with the given name and serial number"""
    def add_camera(self, name, sn):
        self.cur.execute(sql_add_camera, (name, sn))
        self.conn.commit()

    """Deletes the camera with the given name from the table"""
    def delete_camera(self, name):
        self.cur.execute(sql_delete_camera, [name])
        self.conn.commit()


if __name__ == '__main__':
    c = CameraInfo()
    # c.add_camera("camera1", "SN1182746")
    c.delete_camera("camera1")
