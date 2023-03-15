import requests
import json

def get_coordinates_from_file(json_file_path, api_key):
    """
    Retrieves latitude and longitude coordinates for each location in a JSON file, and writes the results to a new JSON file.
    """
    def get_coordinates(name, api_key):
        """
        Returns the latitude and longitude coordinates of a location based on its name.
        """
        url = 'https://maps.googleapis.com/maps/api/geocode/json'
        params = {'address': name, 'key': api_key}
        response = requests.get(url, params=params)
        response_data = response.json()
        if response_data['status'] == 'OK':
            latitude = response_data['results'][0]['geometry']['location']['lat']
            longitude = response_data['results'][0]['geometry']['location']['lng']
            return latitude, longitude
        else:
            print('Could not find coordinates for', name)
            return None

    with open(json_file_path, 'r') as f:
        data = json.load(f)

    locations = data['name']
    coordinates = {}
    for location in locations:
        coords = get_coordinates(location, api_key)
        if coords is not None:
            coordinates[location] = {'latitude': coords[0], 'longitude': coords[1]}

    with open('/home/ubuntu/output/coordinates_train.json', 'w') as f:
        json.dump(coordinates, f)

    print('Coordinates saved to coordinates_train.json')





api_key='***REMOVED***'
train_stations = '/home/ubuntu/input/train_stations.json'

get_coordinates_from_file(train_stations, api_key)