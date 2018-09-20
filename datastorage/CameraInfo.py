import sqlite3

sql_add_camera = "INSERT INTO cameras(Name) VALUES (?)"
sql_delete_camera = "DELETE FROM cameras WHERE Name = ?"


class CameraInfo:

    def __init__(self):
        self._conn = sqlite3.connect('database.db')
        self._cur = self._conn.cursor()

    def create_table(self):
        """Creates the necessary cameras table in the database."""
        self._cur.execute("CREATE TABLE cameras (Name TEXT PRIMARY KEY)")
        self._conn.commit()

    def add_camera(self, name):
        """
        Adds a camera to the table.

        :param name: The name of the new camera
        """
        self._cur.execute(sql_add_camera, [name])
        self._conn.commit()

    def delete_camera(self, name):
        """
        Deletes a camera from the table.

        :param name: The name of the camera
        """
        self._cur.execute(sql_delete_camera, [name])
        self._conn.commit()


if __name__ == '__main__':
    c = CameraInfo()
    c.create_table()
    c.add_camera("camera1")
    # c.delete_camera("camera1")
