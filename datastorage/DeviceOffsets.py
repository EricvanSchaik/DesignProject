import sqlite3
from functools import reduce

sql_queryDate = "SELECT Offset FROM offsets WHERE Camera = ? AND Sensor = ? AND Date = ?"
sql_queryNoDate = "SELECT Offset FROM offsets WHERE Camera = ? AND Sensor = ?"
sql_insertOffset = "INSERT INTO offsets(Camera, Sensor, Offset, Date) VALUES (?, ?, ?, ?)"
sql_updateOffset = "UPDATE Offsets SET Offset = ? WHERE Camera = ? AND Sensor = ? AND Date = ?"


class DeviceOffset:

    def __init__(self):
        self.conn = sqlite3.connect('database.db')
        self.cur = self.conn.cursor()

    """Method for creating the necessary offset table in the database"""
    def create_table(self):
        self.cur.execute("CREATE TABLE offsets (Camera TEXT, Sensor TEXT, Offset REAL, Date TEXT,"
                         "PRIMARY KEY (Camera, Sensor, Date))")
        self.conn.commit()
    """Returns the offset between a given camera and sensor on a given date.
       If there is no known offset for the given date, this returns the average of the offsets of previous dates.
       If no offset is known at all between the given camera and sensor, this returns a default offset of 0."""
    def get_offset(self, cam_id, sens_id, date):
        c = self.cur
        c.execute(sql_queryDate, (cam_id, sens_id, date))
        results = [x[0] for x in c.fetchall()]

        # if there is a known offset, return it
        if len(results) != 0:
            return results[0]

        # otherwise check again without date and return the average or 0 if no offset is known at all
        c.execute(sql_queryNoDate, (cam_id, sens_id))
        results = [x[0] for x in c.fetchall()]

        if len(results) == 0:
            # Camera-Sensor combination unknown; add to table with offset 0
            c.execute(sql_insertOffset, (cam_id, sens_id, 0, date))
            self.conn.commit()
            return 0

        # Camera-Sensor combination unknown; add to table with average offset
        avg = reduce(lambda x, y: x + y, results) / len(results)
        c.execute(sql_insertOffset, (cam_id, sens_id, avg, date))
        self.conn.commit()
        return avg

    """Changes the offset between a given camera and sensor to the given value on the given date."""
    def set_offset(self, cam_id, sens_id, offset, date):
        self.cur.execute(sql_updateOffset, (offset, cam_id, sens_id, date))
        self.conn.commit()


if __name__ == '__main__':
    d = DeviceOffset()
    c = d.cur
    # print(c.execute("SELECT * FROM offsets").fetchall())
    # c.execute(d.sql_insertOffset, ("camera1", "sensor1", 10, "2018-09-20"))
    # c.execute(d.sql_insertOffset, ("camera1", "sensor1", 20, "2018-09-19"))
    # d.conn.commit()
    print(d.get_offset("camera1", "sensor1", "2018-09-21"))
    # print(c.execute("SELECT Offset FROM offsets WHERE Offset = 0").fetchall())
