from flask import Flask , redirect , url_for ,render_template , request, jsonify
import pgeocode
import json  
from utils import *
from flask_mysqldb import MySQL
from geopy.geocoders import Nominatim
geocoder = Nominatim(user_agent = 'geoapiExercise')
data = pgeocode.Nominatim('In')

app = Flask(__name__)
app.config["DEBUG"] = True

#connecting with database
app.config['MYSQL_HOST'] = 'localhost' 
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'oreo0008'
app.config['MYSQL_DB'] = 'practice'

mysql = MySQL(app)



@app.route("/")
def home():
    return render_template('datainput.html')

@app.route("/" , methods=['POST','GET'])
def address():
    if request.method == "POST":
        pincode = request.form["pincode"]
        return redirect(url_for("getAddressByPinCode",pin=pincode))
    else:
        return render_template('datainput.html')

@app.route("/axis" , methods=['POST','GET'])
def axis():
    if request.method == "POST":
        latitude = request.form["latitude"]
        longitude = request.form["longitude"]

        return redirect(url_for("getAddressByAxis",latitude=latitude,longitude=longitude))
    else:
        return render_template('datainput.html')

@app.route("/<latitude>/<longitude>")
def getAddressByAxis(latitude,longitude):
    location = geocoder.reverse((latitude, longitude))
    addingToDatabase(location.raw['address']['postcode'])
    return jsonify(deleteNone(axisDetailedAddress(location.raw['address'])))

@app.route("/<pin>")
def getAddressByPinCode(pin):
    location=(data.query_postal_code(str(pin)))
    
    addingToDatabase(pin)
    return jsonify(deleteNone(pincodeDetailedAddress(location)))

def addingToDatabase(pin):
    location=(data.query_postal_code(str(pin)))
    pincodeDetailedAddress(location)
    #convert Nan to null or 0
    #address=((json.dumps(addre).replace("NaN" ,  "test",)))
    #json.loads(address)
    #dict_clean(address)

    cur = mysql.connection.cursor()
    #check if pincode exist or not
    row = cur.execute("SELECT * FROM practice.pinapi WHERE pincode = (%s)",(pin,))
    if(row==0):
        cur.execute("INSERT INTO practice.pinapi (pincode,area,tehsil,district,state) VALUES (%s ,%s,%s,%s,%s)" ,(pin,address['area'],address['tehsil'],address['district'],address['state']))
    
    #Saving the Actions performed on the DB
    mysql.connection.commit()

    #Closing the cursor
    cur.close()

if __name__ == '__main__':
   app.run()
