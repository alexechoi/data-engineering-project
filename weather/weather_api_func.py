import requests
import json
import os
import schedule # pip install schedule
import pandas as pd
import time # time module for monitoring when it is checking etc



def get_weather_data(json_file_path, api_key, duration_days, save_file_path):
    # Set up API endpoint URLs
    API_endpoint = "http://api.openweathermap.org"
    coord_API_endpoint = "http://api.openweathermap.org/data/2.5/weather?"
    units = "&units=metric"

    # Read in latitude and longitude data from JSON file
    with open(json_file_path, 'r') as f:
        data = json.load(f)
        latitudes = []
        longitudes = []
        for route_data in data.values():
            start_coord = route_data['start_coordinate']
            latitudes.append(start_coord['latitude'])
            longitudes.append(start_coord['longitude'])

    # Set start time for monitoring duration
    start_time = time.time()

    # Create empty JSON file
    data = []
    with open(save_file_path, 'w') as f:
        json.dump(data, f)
    print("Empty JSON File Created Successfully")

    # Function to request and save weather data for a given latitude and longitude pair
    def request_data_and_save(lat, long):
        lat_long = f"lat={lat}&lon={long}"
        join_key = f"&appid={api_key}"
        current_coord_weather_url = coord_API_endpoint + lat_long + join_key + units

        request = requests.get(current_coord_weather_url)
        request_text = request.text
        JSON = json.loads(request_text)

        filterJSON = {
            'longitude': str(JSON['coord']['lon']),
            'latitude': str(JSON['coord']['lat']),
            'weather_id': str(JSON['weather'][0]['id']),
            'weather_main': str(JSON['weather'][0]['main']),
            'weather_desc': str(JSON['weather'][0]['description']),
            'temperature': str(JSON['main']['temp']),
            'feels_like': str(JSON['main']['feels_like']),
            'clouds': str(JSON['clouds']['all']),
            'dt': str(JSON['dt']),
            'id': str(JSON['id'])
        }

        print(filterJSON)

        data.append(filterJSON)

        # Save the JSON file
        with open(save_file_path, 'w') as f:
            json.dump(data, f, indent=4)

        time.sleep(1 * 60)  # Sleep for 2 minutes between requests

    # Loop through all start coordinates and call the request_data_and_save() function for each pair
    for lat, long in zip(latitudes, longitudes):
        request_data_and_save(lat, long)

    # Monitor duration and break out of loop if necessary
    while time.time() - start_time < duration_days * 24 * 60 * 60:
        time.sleep(1)

    print("Finished collecting weather data")

    

get_weather_data('/home/ubuntu/output/routes.json', 'c074b46ec5bfcb0091f23a91b46c79a2', 1, save_file_path='/home/ubuntu/output/weather.json')
    
    
    
    

