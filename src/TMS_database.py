import sqlite3


class TmsDatabase:
    def __init__(self, path):
        self.path = path
        """creates a database in the specified path
        :param path: the database path
        """
        con = None
        try:
            con = sqlite3.connect(path + "TMS_database.db")
            cur = con.cursor()
            cur.execute("""
            CREATE TABLE IF NOT EXISTS tmsTable(filename TEXT, open_count INT, timestamp TEXT, starred BOOL)
                """)
            con.commit()
        except sqlite3.Error:
            if con:
                print("Error! Rolling back changes")
                con.rollback()
        finally:
            if con:
                con.close()

    def get_file_name(self):
        """
        :return: a list of all filename and its timestamp
        """
        con = sqlite3.connect(self.path + "TMS_database.db")
        data = con.cursor().execute("SELECT filename, timestamp FROM tmsTable").fetchall()
        con.close()
        return data

    def get_starred_files(self):
        """
        :return: a list of all filenames that are starred
        """
        con = sqlite3.connect(self.path + "TMS_database.db")
        data = con.cursor().execute("SELECT filename FROM tmsTable WHERE starred = 1").fetchall()
        con.close()
        return data

    def set_timestamp(self, filename, current_time):
        """ updates the timestamp of the filename to the current time
        """
        con = sqlite3.connect(self.path + "TMS_database.db")
        con.cursor().execute(f"UPDATE tmsTable SET timestamp = {current_time} WHERE filename = {filename}")
        con.commit()
        con.close()

    def sync_db(self, filenames):
        """
        Inserts a filename into database that is not in database file and removes a filename
        from database file that is not in filenames
        :param filenames: a list of filenames
        """
        con = sqlite3.connect(self.path + "TMS_database.db")
        cur = con.cursor()
        filename = ["%s" % x for x in cur.execute("SELECT filename FROM tmsTable").fetchall()]
        for i in filenames:
            if i not in filename:
                cur.execute("INSERT INTO tmsTable VALUES(?,?,?,?)", (i, 0, 0, 0))
        con.commit()
        filename = ["%s" % x for x in cur.execute("SELECT filename FROM tmsTable").fetchall()]
        for i in filename:
            if i not in filenames:
                cur.execute("DELETE FROM tmsTable WHERE filename = ?", (i,))
        con.commit()
        con.close()

    def insert_files(self, filenames):
        """
        Inserts a list of filenames into database
        :param filenames: a list of filenames
        """
        con = sqlite3.connect(self.path + "TMS_database.db")
        for i in filenames:
            con.cursor().execute("INSERT INTO tmsTable VALUES(?,?,?,?)", (i, 0, 0, 0))
        con.commit()
        con.close()

    def remove_file(self, filename):
        """
        :param filename:
        """
        con = sqlite3.connect(self.path+"TMS_database.db")
        con.cursor().execute(f"DELETE FROM tmsTable WHERE filename = ?", (filename,))
        con.commit()
        con.close()


# if __name__ == "__main__":
#     val = TmsDatabase("dev/")

