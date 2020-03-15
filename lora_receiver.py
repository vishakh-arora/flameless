from flask import Flask,request
app = Flask(__name__)

@app.route('/')
def index():
    print("Test Received")
    return 'test',200 # response to your request.

@app.route('/flameless', methods=['POST'])
def result():
    print("Received")
    content = request.json # should display 'bar'
    location = content['metadata']
    latitude = location['latitude']
    longitude = location['longitude']

    print(latitude)
    print(longitude)
#    print(content['payload_fields'])
    return '',200 # response to your request.

#@app.route("/flameless")
#def hello():
#    return "Hello World!"

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000)
