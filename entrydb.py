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
                is_raining INTEGER,
                gas_leak INTEGER,
                bmp_temp REAL,
                bmp_pressure REAL,
                bmp_altitude REAL,
                bmp_sealevel_pressure REAL,
                created_at DATETIME
            );
        """
        print("Creating table...")
        conn.execute(create_sql)
        print("Table created.")
        pass

    # get all entries from db
    def find(self, limit=1000, offset=0):
        con = sqlite3.connect(self.dbpath)
        con.row_factory = sqlite3.Row
        
        cur = con.cursor()
        cur.execute("SELECT * FROM entries ORDER BY created_at DESC LIMIT ? OFFSET ?", (limit, offset))
        rows = cur.fetchall()
        
        con.close()
        return rows
    pass
    
    # save entry to db
    def save(self,temp,humidity,lux,is_raining,gas_leak,bmp_temp,bmp_pressure,bmp_altitude,bmp_sealevel_pressure):
        try:
            with sqlite3.connect(self.dbpath) as con:
                cur = con.cursor()
                cur.execute("INSERT INTO entries (temp,humidity,lux,is_raining,gas_leak,bmp_temp,bmp_pressure,bmp_altitude,bmp_sealevel_pressure,created_at) VALUES (?,?,?,?,?,?,?,?,?,?,?)", (temp,humidity,lux,is_raining,gas_leak,bmp_temp,bmp_pressure,bmp_altitude,bmp_sealevel_pressure,dt.datetime.now()))
                con.commit()
                pass
        except:
            con.rollback()
            pass
        finally:
            con.close()
            pass

    pass



