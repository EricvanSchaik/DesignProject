import sqlite3
from functools import reduce


class DeviceOffset:

    sql_queryDate = "SELECT Offset FROM offsets WHERE Camera = ? AND Sensor = ? AND Date = ?"
    sql_queryNoDate = "SELECT Offset FROM offsets WHERE Camera = ? AND Sensor = ?"
    sql_insertOffset = "INSERT INTO offsets(Camera, Sensor, Offset, Date) VALUES (?, ?, ?, ?)"
    sql_updateOffset = "UPDATE Offsets SET Offset = ? WHERE Camera = ? AND Sensor = ? AND Date = ?"

    def __init__(self):
        self.conn = sqlite3.connect('database.db')

    def create_table(self):
        c = self.conn.cursor()

        c.execute("CREATE TABLE offsets (Camera TEXT, Sensor TEXT, Offset REAL, Date TEXT)")

        self.conn.commit()
        self.conn.close()

    def getOffset(self, camID, sensID, date):
        c = self.conn.cursor()
        c.execute(self.sql_queryDate, (camID, sensID, date))
        results = [x[0] for x in c.fetchall()]

        # if there is a known offset, return it
        if len(results) != 0:
            return results[0]

        # otherwise check again without date and return the average or 0 if no offset is known at all
        c.execute(self.sql_queryNoDate, (camID, sensID))
        results = [x[0] for x in c.fetchall()]

        if len(results) == 0:
            # Camera-Sensor combination unknown; add to table with offset 0
            c.execute(self.sql_insertOffset, (camID, sensID, 0, date))
            self.conn.commit()
            return 0

        # Camera-Sensor combination unknown; add to table with average offset
        avg = reduce(lambda x, y: x + y, results) / len(results)
        c.execute(self.sql_insertOffset, (camID, sensID, avg, date))
        self.conn.commit()
        return avg

    def setOffset(self, camID, sensID, offset, date):
        c = self.conn.cursor()
        c.execute(self.sql_updateOffset, (offset, camID, sensID, date))
        self.conn.commit()


if __name__ == '__main__':
    d = DeviceOffset()
    c = d.conn.cursor()
    # print(c.execute("SELECT * FROM offsets").fetchall())
    # c.execute(d.insertOffset, ("camera1", "sensor1", 10, "2018-09-20"))
    # c.execute(d.insertOffset, ("camera1", "sensor1", 20, "2018-09-20"))
    # d.conn.commit()
    print(d.getOffset("camera1", "sensor2", "2018-09-19"))
    # print(c.execute("SELECT Offset FROM offsets WHERE Offset = 0").fetchall())
