#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import json
from datetime import datetime, timedelta
from crontab import CronTab

# Load routes from JSON file
with open("/routes.json") as f:
    routes = json.load(f)

# Iterate over routes
for route, data in routes.items():
    start_lat = data['start_coordinate']['latitude']
    start_long = data['start_coordinate']['longitude']
    end_lat = data['end_coordinate']['latitude']
    end_long = data['end_coordinate']['longitude']

    # Create cron job for each route that runs every 5min
    cron_tab = CronTab()
    job = cron_tab.new(command=f'/project/Uber/get_ride_price.py {start_lat} {start_long} {end_lat} {end_long}')
    job.setall('*/5 * * * *') 
    cron_tab.write()

