import requests
import json

def get_coordinates_from_file(json_file_path, api_key):
    """
    Retrieves latitude and longitude coordinates for each location in a JSON file, and writes the results to a new JSON file.
    """
    def get_coordinates(location, api_key):
        """
        Returns the latitude and longitude coordinates of a location based on its name.
        """
        url = 'https://maps.googleapis.com/maps/api/geocode/json'
        params = {'address': location, 'key': api_key}
        response = requests.get(url, params=params)
        response_data = response.json()
        if response_data['status'] == 'OK':
            latitude = response_data['results'][0]['geometry']['location']['lat']
            longitude = response_data['results'][0]['geometry']['location']['lng']
            return latitude, longitude
        else:
            print('Could not find coordinates for', location)
            return None

    with open(json_file_path, 'r') as f:
        data = json.load(f)

    coordinates = {}
    for event in data:
        location = f"{event['venue_name']} {event['venue_address']}"
        coords = get_coordinates(location, api_key)
        if coords is not None:
            coordinates[event['name']] = {'latitude': coords[0], 'longitude': coords[1]}

    with open('coordinates.json', 'w') as f:
        json.dump(coordinates, f)

    print('Coordinates saved to coordinates.json')



api_key='***REMOVED***'

events = '/project/Events/events.json'

get_coordinates_from_file(events, api_key)
