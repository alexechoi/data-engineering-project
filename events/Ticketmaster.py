import subprocess
subprocess.check_call(['pip', 'install', 'requests'])

import requests
import json
from datetime import datetime, timedelta

def get_events(api_key, city, output_file='events.json'):
    url = "https://app.ticketmaster.com/discovery/v2/events"
    date_from = datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ") # current datetime in UTC
    date_to = (datetime.now() + timedelta(days=7)).strftime("%Y-%m-%dT%H:%M:%SZ") # datetime 7 days from now in UTC

    params = {
        "apikey": api_key,
        "city": city,
        "startDateTime": date_from,
        "endDateTime": date_to,
        "size": 200 # increase page size to get more events per page
    }

    output = []
    while True:
        response = requests.get(url, params=params)
        if response.status_code == 200:
            json_data = response.json()
            events = json_data['_embedded']['events']
            for event in events:
                event_data = {
                    "name": event['name'],
                    "date": event['dates']['start']['localDate'],
                    "time": event['dates']['start']['localTime'],
                    "venue_name": event['_embedded']['venues'][0]['name'],
                    "venue_address": event['_embedded']['venues'][0]['address']['line1']
                }
                output.append(event_data)
                # Do other things with the event data.
            # check if there are more pages
            if 'page' in json_data and 'next' in json_data['page']:
                # set the params to the next page
                params = json_data['page']['next']
            else:
                break
        else:
            print("Error:", response.status_code)
            break

    # write output to JSON file
    with open(output_file, 'w') as outfile:
        json.dump(output, outfile)

    # return the output
    return output

# example usage
api_key = "***REMOVED***"
city = "London"
events = get_events(api_key, city, output_file='events.json')

