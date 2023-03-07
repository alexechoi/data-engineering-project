
import requests
import json

def get_coordinates(location):
    """
    Returns the latitude and longitude coordinates of a location based on its name.
    """
    url = 'https://maps.googleapis.com/maps/api/geocode/json'
    params = {'address': location, 'key': '***REMOVED***'}
    response = requests.get(url, params=params)
    response_data = response.json()
    if response_data['status'] == 'OK':
        latitude = response_data['results'][0]['geometry']['location']['lat']
        longitude = response_data['results'][0]['geometry']['location']['lng']
        return latitude, longitude
    else:
        print('Could not find coordinates for', location)
        return None

with open('hotels.json', 'r') as f:
    data = json.load(f)

coordinates = {}
for hotel in data:
    location = hotel['location']
    coords = get_coordinates(location)
    if coords is not None:
        coordinates[hotel['name']] = {'latitude': coords[0], 'longitude': coords[1]}

with open('coordinates.json', 'w') as f:
    json.dump(coordinates, f)

print('Coordinates saved to coordinates.json')