import requests
import json
import time
import pandas as pd
import sys
import itertools
import threading
import datetime

# define variables

# This is the start location
origin_latitude = 51.5030
origin_longitude = 0.0032

# This is the end location
destination_latitude = 51.4974948
destination_longitude = -0.1356583

# Function to retreieve the price
def get_ride_price(origin_latitude, origin_longitude, destination_latitude, destination_longitude):
    url = "https://www.uber.com/api/loadFEEstimates?localeCode=en"

    payload = json.dumps({
      "origin": {
        "latitude": origin_latitude,
        "longitude": origin_longitude
      },
      "destination": {
        "latitude": destination_latitude,
        "longitude": destination_longitude
      },
      "locale": "en"
    })
    headers = {
      'content-type': 'application/json',
      'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36',
      'x-csrf-token': 'x'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    result = [[x['vehicleViewDisplayName'], x['fareString']] for x in response.json()['data']['prices']]
    return result

# Spinner function
def spinner_thread():
    while True:
        for char in itertools.cycle('|/-\\'):
            sys.stdout.write(f'\rProcess working... {char}')
            sys.stdout.flush()
            time.sleep(0.1)
            sys.stdout.write('\r')

# Initilize the start time
start_time = time.time()
df = pd.DataFrame(columns=['timestamp', 'start_latitude', 'start_longitude', 'end_latitude', 'end_longitude'] + [service for service, price in get_ride_price(origin_latitude, origin_longitude, destination_latitude, destination_longitude)])

# Loop the program for as many times as necessary
while True:
    # Call the function
    ride_prices = get_ride_price(origin_latitude, origin_longitude, destination_latitude, destination_longitude)
    
    print(ride_prices)
    
    ride_data = {
        'timestamp': [datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")],
        'start_latitude': origin_latitude,
        'start_longitude': origin_longitude,
        'end_latitude': destination_latitude,
        'end_longitude': destination_longitude
    }
    
    for service, price in ride_prices:
        ride_data[service] = [price]

    df = pd.concat([df, pd.DataFrame(ride_data)], ignore_index=True)
    
    # Save the data to a CSV file after each iteration - incase of a timeout
    df.to_csv('ride_prices.csv', index=False)

    if time.time() - start_time >= 24 * 60 * 60: # Change the 10 to change the number of hours (10 = 10 hours)
        break

    thread = threading.Thread(target=spinner_thread)
    thread.start()

    # wait for a given number of minutes
    # Change the 5 to the given number of minutes (5 = 5 minutes)
    time.sleep(0.5 * 60)

#display data at the end
print(df)
