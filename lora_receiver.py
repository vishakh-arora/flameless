#! /usr/bin/python

from flask import Flask, render_template, send_from_directory, jsonify, request

app = Flask(__name__, static_url_path='/static')

#@app.route('/')
#def index():
#    print("Test Received")
#    return 'test',200 # response to your request.

# Formats the data like this: 34.28, -118.43, 'Location=San Fernando Smoke Level=653 Temp=56 C',
def constructLocation(content):
    data = content["payload_fields"]
    TEMP = str(float(data["temperature_1"]) * (9/5) + 32.0)
    HUMID = data["relative_humidity_2"]
    SMOKE = data["analog_out_3"]

    location = content['metadata']
    lat = location['latitude']
    long = location['longitude']

    response = requests.get("https://api.tomtom.com/search/2/reverseGeocode/"+lat+"%2C"+long+".json?key=4mXdXKAv0CQKru0SpInttSAw2CVOliMz")
    responseData = json.loads(response.text)
    city = responseData['addresses'][0]['address']['freeformAddress']

    speedData = requests.get("https://api.openweathermap.org/data/2.5/weather?lat="+lat+"&lon="+long+"&appid=37e350cbd0d4c12e3438f9a194a20693")
    data_wind = json.loads(speedData.text)

    # convert m/s --> mph
    windSpeed = str(float(data_wind["wind"]["speed"]) * 2.23694)

    csv = lat + "," + long + "," + "\'Location: " + city + ", Smoke Level: " + SMOKE + " ppm Temp: " + TEMP + "°C Wind: " + windSpeed + " mph\',"
    print(csv)
    return csv

@app.route('/flameless', methods=['POST'])
def result():
    print("Received")
    content = request.json # should display 'bar'

    csv = constructLocation(content)
    markers = open("marker_locations.txt","a")
    #markers.write(csv)

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
    ret = fin.read()
    fin.close()
    return ret

@app.route('/data/center')
def center():
        center = [37.7,-122]
        return jsonify(center)

@app.route('/route')
def route():
        #print(request.args.get('lat'),request.args.get('lon'))
        return render_template('routing-from-my-location.html',lat=request.args.get('lat'),lon=request.args.get('lon'))

@app.route('/')
def home():
  return app.send_static_file('index.html')

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

if __name__ == '__main__':
  app.run(host="0.0.0.0",port=8000,debug=True)


#if __name__ == "__main__":
#    app.run(host='0.0.0.0', port=8000)
