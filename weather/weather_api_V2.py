import requests
import json
import os
import schedule # pip install schedule
import pandas as pd
import time # time module for monitoring when it is checking etc

API_endpoint = "http://api.openweathermap.org"
lat = 51.509865
long = -0.118092
lat_long = "lat=" + str(lat)+ "&lon=" + str(long)
join_1 = "&appid="
API_key = "c074b46ec5bfcb0091f23a91b46c79a2"
current_weather_lat_lon = "/data/2.5/weather?"+ "lat=" + str(round(lat,2))+ "&lon=" + str(round(long,2))

coord_API_endpoint = "http://api.openweathermap.org/data/2.5/weather?"
lat_long = "lat=" + str(lat)+ "&lon=" + str(long)
excludes = '&exclude=daily,minutely,current,alerts'
join_key = "&appid=" + "c074b46ec5bfcb0091f23a91b46c79a2"
units = "&units=metric"

current_coord_weather_url= coord_API_endpoint + lat_long + join_key + units

start_time = time.time() # start time gets the time that we are gonna start the while loop

# make the JSON file
data = []
with open('weather-output.json', 'w') as f:
    json.dump(data, f)
print("Empty JSON File Created Successfully")

def request_data_and_save():
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
    
    # save the JSON file
    with open('weather-output.json', 'w') as f:
        json.dump(data, f, indent=4)
    
while True:
    request_data_and_save()
    
    if time.time() - start_time >= 3 * 24 * 60 * 60: # Change the 3 to change the number of days (3 = 

        break
    
    time.sleep(2 * 60) # 2 is number of minutes