import os
import datetime as dt
import sqlite3 as sqlite3


class EntryDB():

    # DB Absolute Path
    dbpath = os.path.join(os.getcwd(), "data", "database.sq3")    

    def __init__(self):
        # connect to db
        conn = sqlite3.connect(self.dbpath)
        # create table
        create_sql = """
            CREATE TABLE IF NOT EXISTS entries (
                temp REAL,
                humidity REAL,
                lux REAL,
                pressure REAL,
                is_raining INTEGER,
                created_at DATETIME
            );
        """
        conn.execute(create_sql)
        pass

    # get all entries from db
    def find(self, limit=10, offset=0):
        con = sqlite3.connect(self.dbpath)
        con.row_factory = sqlite3.Row
        
        cur = con.cursor()
        cur.execute("SELECT * FROM entries ORDER BY created_at DESC LIMIT ? OFFSET ?", (limit, offset))
        rows = cur.fetchall()
        
        con.close()
        return rows
    pass
    
    # save entry to db
    def save(self,temp,humidity,lux,pressure,is_raining):
        try:
            with sqlite3.connect(self.dbpath) as con:
                cur = con.cursor()
                cur.execute("INSERT INTO entries (temp, humidity, lux, pressure, is_raining, created_at) VALUES (?,?,?,?,?,?)", (temp,humidity,lux,pressure,is_raining,dt.datetime.now()))
                con.commit()
                pass
        except:
            con.rollback()
            pass
        finally:
            con.close()
            pass

    pass



