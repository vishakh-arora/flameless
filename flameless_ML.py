import numpy as np
import requests, json, sys
import keras_test

months = ['fill', 'jan', 'feb', 'mar', 'apr', 'may', 'jun', 'jul', 'aug', 'sep', 'oct', 'nov', 'dec']
weekdays = ['fill', 'sun', 'mon', 'tue', 'wed', 'thu', 'fri', 'sat']
topLeft = (42.001417, -7.218365)
bottomRight = (41.730503, -6.580759)
x_coord_diff = (bottomRight[0] - topLeft[0]) / 9.0
y_coord_diff = (bottomRight[1] - topLeft[1]) / 9.0

# Gets the elevation(topography) of a latitude and longitude pair using Google's Elevation API
def getElevation(lat, long):
    elevationData = requests.get("https://maps.googleapis.com/maps/api/elevation/json?locations="+str(lat)+","+str(long)+"&key=AIzaSyATYK4iyl4JnU4oH6hqewTXLxFzB420ESg")
    eleResponse = json.loads(elevationData.text)
    elevation = float(eleResponse['results'][0]['elevation'])
    return elevation

# Converts spatial coordinate of Montesinho park to latitude, longitude
def getLatLong(x, y):
    lat = 41.994823 + x_coord_diff * float(x)
    long = -7.191875 + y_coord_diff * float(y)
    return (lat, long)

with open('/home/vishakh/flameless/flameless_fires_processed.csv') as f:
    input = [i.split(",") for i in f.read().strip().split('\n')[1:]]
    x = [i[:-1] for i in input]
    y = np.array([float(i[-1]) for i in input])

# Prep data for ML: [latitude, longitude, elevation, month, day, temp, humid, windSpeed]
for i in range(len(x)):
    for j in range(len(x[i])):
        try:
            x[i][j] = float(x[i][j])
        except:
            try:
                x[i][j] = months.index(x[i][j]) # Convert month names to numbers
            except:
                x[i][j] = weekdays.index(x[i][j]) # Convert weekday names to numbers
    x[i][0], x[i][1] = getLatLong(x[i][0], x[i][1])
    x[i].insert(2, getElevation(x[i][0], x[i][1]))

x = np.array(x)
rng = np.random.RandomState(113)
indices = np.arange(len(x))
rng.shuffle(indices)
x = x[indices]
y = y[indices]

test_split = 0.2
train_data = np.array(x[:int(len(x) * (1 - test_split))])
train_targets = np.array(y[:int(len(x) * (1 - test_split))])
test_data = np.array(x[int(len(x) * (1 - test_split)):])
test_targets = np.array(y[int(len(x) * (1 - test_split)):])

mean = train_data.mean(axis=0)
train_data -= mean
std = train_data.std(axis=0)
train_data /= std

test_data -= mean
test_data /= std

keras_test.runModel(train_data, train_targets, test_data, test_targets)
