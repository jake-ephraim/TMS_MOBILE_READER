import sqlite3

def create_db(path):
    con = None
    try:
        con = sqlite3.connect(path + "TMS_database.db")
        cur = con.cursor()
        cur.executescript("""
        DROP TABLE IF EXISTS tmsTable;
        CREATE TABLE tmsTable(filename TEXT, open_count INT, timestamp TEXT, starred BOOL);
            """)
        con.commit()
    except sqlite3.Error:
        if con:
            print("Error! Rolling back changes")
            con.rollback()
    finally:
        if con:
            con.close()


def get_file_name():
    con = sqlite3.connect("TMS_database.db")
    data = con.cursor().execute("SELECT filename, timestamp FROM tmsTable").fetchall()
    return data


def get_starred_files():
    con = sqlite3.connect("TMS_database.db")
    data = con.cursor().execute("SELECT filename FROM tmsTable WHERE starred = 1").fetchall()
    return data


def sync_db(data):
    con = sqlite3.connect("TMS_database.db")
    cur = con.cursor()
    filename = ["%s" % x for x in cur.execute("SELECT filename FROM tmsTable").fetchall()]
    for i in data:
        if i not in filename:
            cur.execute("INSERT INTO tmsTable VALUES(?,?,?,?)", (i, 0, 0, 0))
    con.commit()
    filename = ["%s" % x for x in cur.execute("SELECT filename FROM tmsTable").fetchall()]
    for i in filename:
        if i not in data:
            cur.execute("DELETE FROM tmsTable WHERE filename = ?", (i,))
    con.commit()
    con.close()


# if __name__ == "__main__":
    # create_db('dev/')
