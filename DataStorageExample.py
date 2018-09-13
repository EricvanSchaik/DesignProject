import sqlite3


def create_table():
    conn = sqlite3.connect('example.db')
    c = conn.cursor()

    c.execute("CREATE TABLE data (Time real, Ax real, Ay real, Az real, Gx real, Gy real, Gz real, Mx real, My real, Mz real, T real)")

    c.execute("INSERT INTO data VALUES (0.006042,2056,-486,-2872,988,-1097,-839,-287,-141,-148,25560), (0.055389,2966,-838,-3098,619,-1387,-1204,-247,-159,-156,25587)")

    conn.commit()
    conn.close()


def read_data():
    conn = sqlite3.connect('example.db')
    c = conn.cursor()

    for row in c.execute('SELECT * FROM data'):
        print(row)


if __name__ == '__main__':
    #create_table()
    read_data()
