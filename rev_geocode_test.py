import requests, json

response = requests.get("https://api.tomtom.com/search/2/reverseGeocode/40.9048839%2C-121.9599613.json?key=4mXdXKAv0CQKru0SpInttSAw2CVOliMz")
data = json.loads(response.text)
city = data['addresses'][0]['address']['freeformAddress']
#print(city)


speedData = requests.get("https://api.openweathermap.org/data/2.5/weather?lat=37.7159&lon=-121.9101&appid=37e350cbd0d4c12e3438f9a194a20693")
data_wind = json.loads(speedData.text)
print(data_wind)
windSpeed = data_wind["wind"]["speed"]
print(windSpeed)
