import json
import requests
import os

def get_coordinates_from_file_trains(json_file_path, api_key):
    """
    Retrieves latitude and longitude coordinates for each location in a JSON file, and writes the results to a new JSON file.
    """
    import json

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

# Create an empty JSON file if it doesn't exist
    if not os.path.exists(json_file_path):
        with open(json_file_path, 'w') as f:
            json.dump({'name': []}, f)

    with open(json_file_path, 'r') as f:
        data = json.load(f)

    locations = data["name"]
    coordinates = {}
    for location in locations:
        coords = get_coordinates(location, api_key)
        if coords is not None:
            coordinates[location] = {'latitude': coords[0], 'longitude': coords[1]}

    with open('/home/ubuntu/output/coordinates_train.json', 'w') as f:
        json.dump(coordinates, f)

    print('Coordinates saved to coordinates_train.json')


