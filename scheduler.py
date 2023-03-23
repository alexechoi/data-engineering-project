import requests
import json
import datetime
import time
import threading

from get_hotels import get_hotels_booking
from geolocation_train import get_coordinates_from_file_trains
from geolocation_hotels import get_coordinates_from_file_hotels
from routes_V2 import create_route
from get_ride_price import get_ride_price
from twitter_API_function import search_tweets
from weather_api_func import get_weather_data

import logging

logging.basicConfig(filename='scheduler.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')



def scheduler():

    bearer_token = '***REMOVED***'
    API_key_weather = '***REMOVED***'
    API_key_hotel_train = '***REMOVED***'
    query = "uber London OR #uber #London"
    max_results = 20

    # Get updated hotel data
    get_hotels_booking('https://www.booking.com/searchresults.en-gb.html?ss=Westminster%2C+London%2C+United+Kingdom')
    get_coordinates_from_file_hotels('/home/ubuntu/output/hotels.json', API_key_hotel_train)
    # Get updated train coordinates
    get_coordinates_from_file_trains('/home/ubuntu/input/train_stations.json', API_key_hotel_train)
    #routes = create_route()
    # Call get_ride_price, get_weather_data, and search_tweets every 1 minute for 5 minutes
    minute_interval_seconds = 5*60
    num_minute_iterations = 131487192

    for i in range(num_minute_iterations):
        # Extract coordinates from updated routes
        #with open('/project/output/routes.json', 'r') as f:
            #route_data = json.load(f)

        #coordinates = []
        #for route_key, route_value in route_data.items():
            #start_lat = route_value['start_coordinate']['latitude']
            #start_long = route_value['start_coordinate']['longitude']
            #end_lat = route_value['end_coordinate']['latitude']
            #end_long = route_value['end_coordinate']['longitude']
            #coordinates.append((start_lat, start_long, end_lat, end_long))

        # Call get_ride_price, get_weather_data, and search_tweets for updated routes
        #for coords in coordinates:
            #origin_lat, origin_long, dest_lat, dest_long = coords
        get_ride_price("/home/ubuntu/output/routes.json")

        get_weather_data("/home/ubuntu/output/routes.json", API_key_weather)

        search_tweets(bearer_token, query, max_results)
        # At the end of the scheduler function, create a flag file
        with open("scheduler_done.flag", "w") as flag_file:
           flag_file.write("done")
        # Wait one minute before checking again
        time.sleep(minute_interval_seconds)


def start_scheduler():
    scheduler_thread = threading.Thread(target=scheduler)
    scheduler_thread.daemon = True
    scheduler_thread.start()

from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/scheduler', methods=['GET'])
def call_scheduler():
    try:
        start_scheduler()
        return jsonify(status='success', message='Scheduler started')
    except requests.exceptions.RequestException as e:
        logging.error(f"Network error communicating with endpoint: {e}")
        return jsonify(status='error', message=str(e))
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)

