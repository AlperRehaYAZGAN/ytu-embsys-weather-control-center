#
#   YTU Embedded Systems Mini Meteorology App 
#

#
#   Docs: https://docs.python.org/3/library/webbrowser.html
#

#
#   APP Dependencies
#
import os


#
#   Flask Implementation
#
from flask import Flask,request,render_template
app = Flask(__name__)


#
#   Flask Socket.io Implementation
#
from flask_socketio import SocketIO,send,emit
socketio = SocketIO(app)

#
#   entryDB Implementation
#
from entrydb import EntryDB
entryDB = EntryDB()





#   HTML ENDPOINT
#   GET / - Home Page -> Render 'home' Template
#
@app.route('/')
def home():
    return render_template('home.html')


#   HTML ENDPOINT
#   GET /monitor - About Page -> Render 'about' Template
#
@app.route('/monitor')
def monitor():
    return render_template('monitor.html')


#   HTML ENDPOINT
#   GET /entries - Entries Page -> Render 'entries' Template
#
@app.route('/history', methods=['GET'])
def get_db_history():
    allEntries = entryDB.find()    
    return render_template("db.html",rows = allEntries, msg = "Sisteme kayıtlı girdi(entry) kayıtlarını getirdi.")


#   API ENDPOINT
#   GET /save - Save Entry to DB
#
@app.route('/save')
def save_sensor_values():
    # sensor values temp,humidity,pressure,lux,is_raining,gas_leak
    temp = float(request.args.get('temp',0))
    humidity = float(request.args.get('humidity',0))
    pressure = float(request.args.get('pressure',0))
    lux = float(request.args.get('lux',0))
    is_raining = int(request.args.get('is_raining',0))
    gas_leak = int(request.args.get('gas_leak',0))
    # bmp values
    bmp_temp = float(request.args.get('bmp_temp',0))
    bmp_pressure = float(request.args.get('bmp_pressure',0))
    bmp_altitude = float(request.args.get('bmp_altitude',0))
    bmp_sealevel_pressure = float(request.args.get('bmp_sealevel_pressure',0))

    resp = {
        'status': True,
        'msg': '',
    }

    # check all values not default
    if not(temp != 0 and humidity != 0):
        resp['status'] = False
        resp['msg'] = "Lütfen tüm değerleri giriniz. Example: /save?temp=23.5&humidity=45.6&pressure=12.3&lux=12.3&is_raining=1&gas_leak=1"
        return resp

    # save to db
    try:
        entryDB.save(temp,humidity,lux,pressure,is_raining,gas_leak)
        pass
    except:
        print("Error saving to db.")
        pass

    # emit new values to all clients
    try:
        emit('new_values', {
            'temp': temp,
            'humidity': humidity,
            'pressure': pressure,
            'lux': lux,
            'is_raining': is_raining,
            'gas_leak': gas_leak,
            'bmp_temp': bmp_temp,
            'bmp_pressure': bmp_pressure,
            'bmp_altitude': bmp_altitude,
            'bmp_sealevel_pressure': bmp_sealevel_pressure
        })
        pass
    except:
        print("Error while emitting new values.")
        pass

    # return success
    resp['status'] = 'success'
    resp['msg'] = "Girdi kaydedildi."
    return resp




#
#   Flask App Run
#
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
