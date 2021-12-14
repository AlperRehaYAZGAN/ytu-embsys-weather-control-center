from flask import Flask,request,render_template
app = Flask(__name__)

#
#   SOCKET IO IMPLEMENTATION
#
from flask_socketio import SocketIO,send,emit
socketio = SocketIO(app)


import datetime as dt
import sqlite3 as sqlite3
import os


class EntrySqlite():

    dbpath = os.path.join(os.path.dirname(__file__), "data", "database.sq3")    
    def __init__(self):
        conn = sqlite3.connect(self.dbpath)
        conn.execute('CREATE TABLE IF NOT EXISTS entries ( lux integer, air integer, temp integer, humidity integer, water_level integer, created_at text )')
        print("Table created successfully")
        pass
    
    def save(self,lux,air,temp,humidity,water_level):
        isOk = False
        try:
            with sqlite3.connect(self.dbpath) as con:
                cur = con.cursor()
                cur.execute("INSERT INTO entries (lux,air,temp,humidity, water_level,created_at) VALUES (?,?,?,?,?,?)",(lux,air,temp, humidity, water_level,dt.datetime.now()) )
                con.commit()
                isOk = True
                pass
        except:
            con.rollback()
            pass
        finally:
            con.close()
            pass
        return isOk     
    
    def all(self):
        con = sqlite3.connect(self.dbpath)
        con.row_factory = sqlite3.Row
        
        cur = con.cursor()
        cur.execute("select * from entries;")
        rows = cur.fetchall()
        
        con.close()
        return rows
    pass

database = EntrySqlite()



@app.route('/')
def get_all():
    allEntries = database.all()    
    return render_template("index.html",rows = allEntries, msg = "Sisteme kayıtlı girdi(entry) kayıtlarını getirdi.")


@app.route('/save')
def save_sensor_values():
    air_quality = float(request.args.get('air',0))
    temperature = float(request.args.get('temp',0))
    lux = float(request.args.get('lux',0))
    humidity = float(request.args.get('humidity',0))
    water_level = float(request.args.get('wlevel',0))

    try:
        isOk = database.save(lux,air_quality,temperature,humidity,water_level,water_temp,0)
        if(air_quality == 0 and temperature == 0 and lux == 0):
            return "No sensor value ensured. Usage: http://SERVER/save?air=10&temp=10&lux=10&wlevel=10&humidity=20"
        else:
            return "Saved successfully"
    except:
        return "Error occured while inserting database"


@app.route('/history')
def get_db_all():
    allEntries = database.all()    
    return render_template("db.html",rows = allEntries, msg = "Sisteme kayıtlı girdi(entry) kayıtlarını getirdi.")


@app.route('/new')
def emit_new_values():
    air_quality = float(request.args.get('air',0))
    temperature = float(request.args.get('temp',0))
    lux = float(request.args.get('lux',0))
    humidity = float(request.args.get('humidity',0))
    water_level = float(request.args.get('wlevel',0))

    if(air_quality == 0 and lux == 0 and temperature == 0):
        return "No value ensured usage: http://SERVER/new?air=10&temp=10&lux=10&wlevel=10&humidity=20"
    
    new_values = {
        "air" : air_quality,
        "lux" : lux,
        "temp" : temperature,
        "humidity" : humidity,
        "wlevel" : water_level,
    }

    # send sensor values to dashboard
    try:
        socketio.emit('new-values', new_values)
    except:
        print("Sensor values could not send to admin dashboard")
        pass
    # save entries to database
    try:
        database.save(lux,air_quality,temperature,humidity,water_level)
        print("Kaydedildi")
        pass
    except:
        print("Hata meydana geldi.")
        pass
    return "0"



APP_BIND= os.getenv('APP_BIND', '0.0.0.0')
APP_PORT= os.getenv('APP_PORT', '5000')

# flask main function
if __name__ == '__main__':
    print("App initiliazing...")
    # run from dotenv
    app.run(app,host=APP_BIND,port=APP_PORT)
    print("App Server Port: " + APP_PORT)
    socketio.run(app)
    print("Socket Server Port: " + APP_PORT)
    print("App Initialization Finished")
    pass
