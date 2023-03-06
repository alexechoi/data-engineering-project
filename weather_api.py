import requests
import json
import os
import schedule # pip install schedule
import pandas as pd
import time # time module for monitoring when it is checking etc
import csv

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

# make the csv
with open('weather-output.csv', 'w') as creating_new_csv_file: 
   pass 
print("Empty CSV Created Successfully")

# headers for the csv
headers = [
        'longitude',
        'latitude',
        'weather_id',
        'weather_main',
        'weather_desc',
        'weather_icon',
        'base',
        'temperature',
        'feels_like',
        'temp_min',
        'temp_max',
        'pressure',
        'humidity',
        'visibility',
        'wind_speed',
        'wind_deg',
        'clouds',
        'dt',
        'sys_type',
        'sys_id',
        'sys_country',
        'sys_sunrise',
        'sys_sunset',
        'timezone',
        'id',
        'city',
        'cod'
    ]

# add headers to csv
with open('weather-output.csv', 'w', newline='') as file:
    writer = csv.DictWriter(file, fieldnames=headers)
    writer.writeheader()
    print("Headers added to CSV")

def request_data_and_save(excel_file: str = "weather.xlsx"):
    request = requests.get(current_coord_weather_url)
    request_text = request.text
    JSON = json.loads(request_text)

    filterJSON = {
        'longitude': str(JSON['coord']['lon']), 
        'latitude': str(JSON['coord']['lat']),
        'weather_id': str(JSON['weather'][0]['id']),
        'weather_main': str(JSON['weather'][0]['main']),
        'weather_desc': str(JSON['weather'][0]['description']),
        'weather_icon': str(JSON['weather'][0]['icon']),
        'base': str(JSON['base']),
        'temperature': str(JSON['main']['temp']),
        'feels_like': str(JSON['main']['feels_like']),
        'temp_min': str(JSON['main']['temp_min']),
        'temp_max': str(JSON['main']['temp_max']),
        'pressure': str(JSON['main']['pressure']),
        'humidity': str(JSON['main']['humidity']),
        'visibility': str(JSON['visibility']),
        'wind_speed': str(JSON['wind']['speed']),
        'wind_deg': str(JSON['wind']['deg']),
        'clouds': str(JSON['clouds']['all']),
        'dt': str(JSON['dt']),
        'sys_type': str(JSON['sys']['type']),
        'sys_id': str(JSON['sys']['id']),
        'sys_country': str(JSON['sys']['country']),
        'sys_sunrise': str(JSON['sys']['sunrise']),
        'sys_sunset': str(JSON['sys']['sunset']),
        'timezone': str(JSON['timezone']),
        'id': str(JSON['id']),
        'city': str(JSON['name']),
        'cod': str(JSON['cod'])
    }
    
    print(filterJSON)
    
    dct = {k:[v] for k,v in filterJSON.items()}
    
    # save the csv
    with open('weather-output.csv', 'a', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=dct.keys())
        writer.writerow(dct)
    
while True:
    request_data_and_save()
    
    if time.time() - start_time >= 3 * 24 * 60 * 60: # Change the 10 to change the number of hours (10 = 10 hours)
        break
    
    time.sleep(2 * 60) # 2 is number of minutes