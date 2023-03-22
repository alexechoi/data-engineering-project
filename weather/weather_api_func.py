import requests
import json
import os
import os.path
import pandas as pd
import time # time module for monitoring when it is checking etc

def get_weather_data(json_file_path, api_key):
    # Set up API endpoint URLs
    API_endpoint = "http://api.openweathermap.org"
    coord_API_endpoint = "http://api.openweathermap.org/data/2.5/weather?"
    units = "&units=metric"

    with open(json_file_path, 'r') as f:
        data = json.load(f)
        latitudes = []
        longitudes = []
        seen_coordinates = set()
        for route_data in data.values():
            start_coord = route_data['start_coordinate']
            coordinate_tuple = (start_coord['latitude'], start_coord['longitude'])
            if coordinate_tuple not in seen_coordinates:
                seen_coordinates.add(coordinate_tuple)
                latitudes.append(start_coord['latitude'])
                longitudes.append(start_coord['longitude'])
    # Set start time for monitoring duration
    start_time = time.time()
    # Create empty list for weather data
    weather_data = []

    # Loop through all unique start coordinates and request weather data for each pair
    for lat, long in zip(latitudes, longitudes):
        lat_long = f"lat={lat}&lon={long}"
        join_key = f"&appid={api_key}"
        current_coord_weather_url = coord_API_endpoint + lat_long + join_key + units

        request = requests.get(current_coord_weather_url)
        request_text = request.text
        JSON = json.loads(request_text)

        weather_data.append(JSON)

    # Save the JSON file
    try:
        with open('/home/ubuntu/output/weather.json', 'w') as f:
            json.dump(weather_data, f)
        print("Data appended to file successfully")
        
    except Exception as e:
        print("Error writing to file:", e)

    print('Weather APIs saved to weather.json')

