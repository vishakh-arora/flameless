#! /usr/bin/python

from flask import Flask, render_template, send_from_directory, jsonify, request
import requests, json
from flameless_text import generate_email
import NeuralNetwork as neural
import numpy as np
from dateutil import parser

app = Flask(__name__, static_url_path='/static')

#@app.route('/')
#def index():
#    print("Test Received")
#    return 'test',200 # response to your request.

# Formats the data like this: 34.28, -118.43, 'Location=San Fernando Smoke Level=653 Temp=56 C',
def constructLocation(content):
    data = content["payload_fields"]
    TEMPC = float(data["temperature_1"])
    TEMP = '%.1f'%(TEMPC * (9/5) + 32.0)
    HUMID = str(data["relative_humidity_2"])
    SMOKE = str(data["analog_out_3"])

    location = content['metadata']
    lat = str(location['latitude'])
    long = str(location['longitude'])
    date = parser.parse(location['time'])
    # Make weekday 1 indexed
    weekday = float(date.strftime('%w')) + 1
    month = float(date.month)
    response = requests.get("https://api.tomtom.com/search/2/reverseGeocode/"+lat+"%2C"+long+".json?key=4mXdXKAv0CQKru0SpInttSAw2CVOliMz")
    responseData = json.loads(response.text)
    city = responseData['addresses'][0]['address']['freeformAddress'].replace(",","")

    speedData = requests.get("https://api.openweathermap.org/data/2.5/weather?lat="+lat+"&lon="+long+"&appid=37e350cbd0d4c12e3438f9a194a20693")
    data_wind = json.loads(speedData.text)

    # convert m/s --> mph
    windSpeed = float(data_wind["wind"]["speed"]) * 2.23694
    windSpeedkmh = float(data_wind["wind"]["speed"]) * 3.6
    windString = '%.1f'%(windSpeed)

    elevationData = requests.get("https://maps.googleapis.com/maps/api/elevation/json?locations="+str(lat)+","+str(long)+"&key=AIzaSyATYK4iyl4JnU4oH6hqewTXLxFzB420ESg")
    eleResponse = json.loads(elevationData.text)
    elevation = float(eleResponse['results'][0]['elevation'])

    inputs = [[]]
    inputs[0].append(float(lat))
    inputs[0].append(float(long))
    inputs[0].append(elevation)
    inputs[0].append(month)
    inputs[0].append(weekday)
    inputs[0].append(TEMPC)
    inputs[0].append(float(HUMID))
    inputs[0].append(windSpeedkmh)
    print("INPUTS:", str(inputs))
    burnedArea = getPrediction(inputs)
    print("PREDICTED BURN AREA:",str(burnedArea))
    generate_email(lat, long, TEMP, city, windString)
    csv = lat + ", " + long + ", " + "\'Location: " + city + " Smoke Level: " + SMOKE + " ppm Temp: " + TEMP + "°F Wind: " + windString + " mph\',"
    print(csv)
    return csv

def getPrediction(inputs):
    return nn.predict(np.array(inputs))

@app.route('/flameless', methods=['POST'])
def result():
    print("Received")
    content = request.json # should display 'bar'

    markers = open("marker_locations.txt","a")
    csv = constructLocation(content)
    markers.write(csv)
    markers.close()

    return '',200 # response to your request.

############## BEGIN WEBSITE ROUTES HERE ##############

@app.route('/js/<path:path>')
def send_js(path):
    return send_from_directory('static/js', path)

@app.route('/css/<path:path>')
def send_css(path):
    return send_from_directory('static/css', path)

@app.route('/img/<path:path>')
def send_img(path):
    return send_from_directory('static/img', path)

@app.route('/assets/<path:path>')
def send_assets(path):
    return send_from_directory('static/assets', path)

@app.route('/sdk/<path:path>')
def send_sdk(path):

    return send_from_directory('static/sdk', path)

@app.route('/DVHacks_website/<path:path>')
def send_website(path):

    return send_from_directory('static/DVHacks_website', path)

@app.route('/mark')
def mark():
  #print("hello")
  return app.send_static_file('markers-clustering.html')

@app.route('/data/destination')
def destination():
        return jsonify(lat=37.7,lon=-122)

@app.route('/data/locations')
def locations():
    fin = open("marker_locations.txt","r")
    ret = fin.read()[:-1]
    fin.close()
    return ret

@app.route('/data/center')
def center():
    center = [37.7,-122]
    return jsonify(center)

@app.route('/route')
def route():
    return render_template('routing-from-my-location.html',lat=request.args.get('lat'),lon=request.args.get('lon'))

@app.route('/')
def home():
  return app.send_static_file('index.html'),200

@app.route('/about')
def about():
  return app.send_static_file('about.html')

@app.route('/histogram/laps')
def lap_histogram():
  return app.send_static_file('lap_histogram.html')

@app.route('/scatter/lap-duration')
def lap_duration_scatter():
  return app.send_static_file('scatter.html')

@app.route('/')
def reports():
  return app.send_static_file('reports.html')

############## END WEBSITE ROUTES HERE ##############

nn = neural.NeuralNetwork()
nn.load(['model.json', 'model.h5'])

if __name__ == '__main__':
  app.run(host="0.0.0.0",port=8000,debug=True)
