import time
import pandas as pd
import itertools
import threading
import datetime
from get_ride_price import get_ride_price
from spinner_thread import spinner_thread

# define variables

# This is the start location
origin_latitude = 51.5030
origin_longitude = 0.0032

# This is the end location
destination_latitude = 51.4974948
destination_longitude = -0.1356583

# Initilize the start time
start_time = time.time()
df = pd.DataFrame(columns=['timestamp', 'start_latitude', 'start_longitude', 'end_latitude', 'end_longitude'] + [service for service, price in get_ride_price(origin_latitude, origin_longitude, destination_latitude, destination_longitude)])

# Loop the program for as many times as necessary
while True:
    # Call the function
    try:
        ride_prices = get_ride_price(origin_latitude, origin_longitude, destination_latitude, destination_longitude)
    except Exception as e:
        print(f'Request failed: {e}')
        
        # timeout for 60 seconds to stop mass requests
        time.sleep(1 * 60)
        continue
    
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

    if time.time() - start_time >= 3 * 24 * 60 * 60: # Change the 10 to change the number of hours (10 = 10 hours)
        break

    thread = threading.Thread(target=spinner_thread)
    thread.start()

    # wait for a given number of minutes
    # Change the 5 to the given number of minutes (5 = 5 minutes)
    time.sleep(5 * 60)

#display data at the end
print(df)
