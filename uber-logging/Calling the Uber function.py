#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import json
import subprocess
from datetime import datetime
from get_ride_price import get_ride_price
from time import sleep, time

# Load routes from JSON file
with open("/routes.json") as f:
    routes = json.load(f)

# Set the start time
start_time = time()

# Run the following for each route every 5 minutes until 24 hours have passed
while time() - start_time < 86400:
    for route, data in routes.items():
        start_lat = data['start_coordinate']['latitude']
        start_long = data['start_coordinate']['longitude']
        end_lat = data['end_coordinate']['latitude']
        end_long = data['end_coordinate']['longitude']
        
        # Run the function to get the ride price
        ride_price = get_ride_price(start_lat, start_long, end_lat, end_long)
    
    # Wait for 5 minutes before running again
    sleep(300)

