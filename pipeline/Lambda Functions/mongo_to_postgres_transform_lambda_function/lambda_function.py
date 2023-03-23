import json
import pymongo
from pymongo import MongoClient
import psycopg2
from datetime import datetime

import pymongo
import psycopg2

def lambda_handler(event, context):
    # Connect to MongoDB
    mongodb_uri = "***REMOVED***"
    mongo_client = pymongo.MongoClient(mongodb_uri)
    mongodb = mongo_client.group_db

    # Connect to PostgreSQL
    postgres_connection = "***REMOVED***"
    pg_conn = psycopg2.connect(postgres_connection)
    pg_cursor = pg_conn.cursor()

    # Load data from MongoDB collections
    hotels = list(mongodb.hotels.find())
    coordinates_hotel = list(mongodb.coordinates_hotel.find())
    train_stations = list(mongodb.coordinates_train.find())
    tweets = list(mongodb.tweets.find())
    uber_data = list(mongodb.uber.find())
    weather_data = list(mongodb.weather.find())
    routes_data = list(mongodb.routes.find())

    # Transform data
    transformed_hotel_data = transform_hotel_data(hotels, coordinates_hotel)
    transformed_train_station_data = transform_train_station_data(train_stations)
    transformed_tweet_data = transform_tweet_data(tweets)
    transformed_uber_data = transform_uber_data(uber_data, routes_data)
    transformed_routes_data_dict = transform_routes_data(routes_data, weather_data)
    transformed_weather_data = transform_weather_data(weather_data, transformed_routes_data_dict['location_ids'], postgres_connection)

    # Insert transformed data into PostgreSQL
    insert_hotel_data(transformed_hotel_data, postgres_connection)
    insert_train_station_data(transformed_train_station_data, postgres_connection)
    insert_tweet_data(transformed_tweet_data, postgres_connection)

    # Move insert_routes_data before insert_uber_data
    insert_routes_data(
        transformed_routes_data_dict['routes'],
        transformed_routes_data_dict['start_location'],
        transformed_routes_data_dict['end_location'],
        postgres_connection
        )

    insert_uber_data(transformed_uber_data, postgres_connection)
    insert_weather_data(transformed_weather_data, postgres_connection)


    # Commit changes and close PostgreSQL connection
    pg_conn.commit()
    pg_cursor.close()
    pg_conn.close()


# Transform data

def transform_hotel_data(hotels, coordinates_hotel):
    hotel_info = []
    hotel_location = []
    
    current_id = 1  # Initialize a counter for assigning unique IDs

    # Create a dictionary to map hotel names to their coordinates
    hotel_coordinates_map = {}
    for coord in coordinates_hotel:
        hotel_name = coord['name']
        hotel_coordinates_map[hotel_name] = (coord['latitude'], coord['longitude'])

    for hotel in hotels:
        # Assign a new unique integer ID to each hotel
        hotel_id = current_id
        current_id += 1

        # Extract 'name' and 'location' fields from the hotel document
        name = hotel.get('name')
        location = hotel.get('location')

        hotel_info.append({"id": hotel_id, "name": name, "neighbourhood": location})
        
        # Get the latitude and longitude from the hotel_coordinates_map
        lat, long = hotel_coordinates_map.get(name, (None, None))

        if lat is None or long is None:
            print(f"Missing latitude or longitude for hotel: {hotel_id}, name: {name}")

        hotel_location.append({"id": hotel_id, "hotel_id": hotel_id, "lat": lat, "long": long})

    return hotel_info, hotel_location


def transform_train_station_data(train_stations):
    train_station_data = []
    
    current_id = 1  # Initialize a counter for assigning unique IDs

    for station in train_stations:
        # Assign a new unique integer ID to each station
        station_id = current_id
        current_id += 1

        # Extract 'name', 'latitude', and 'longitude' fields from the station document
        name = station.get('name')
        lat = station.get('latitude')
        long = station.get('longitude')

        train_station_data.append({"id": station_id, "name": name, "lat": lat, "long": long})

    return train_station_data

def transform_tweet_data(tweets):
    tweet_data = []
    tweet_metadata = []

    current_id = 1  # Initialize a counter for assigning unique IDs

    for tweet in tweets:
        # Assign a new unique integer ID to each tweet
        tweet_id = current_id
        current_id += 1

        # Extracting necessary fields from the tweet document
        text = tweet.get('text')

        tweet_data.append({"id": tweet_id, "text": text})

        # Assuming newest_id and oldest_id are fields in the tweets collection
        newest_id = tweet.get('newest_id')
        oldest_id = tweet.get('oldest_id')

        # Calculate result_count only if edit_history_tweet_ids is present
        edit_history_tweet_ids = tweet.get('edit_history_tweet_ids', [])
        result_count = len(edit_history_tweet_ids)

        tweet_metadata.append({"id": tweet_id, "newest_id": newest_id, "oldest_id": oldest_id, "result_count": result_count, "tweet_id": tweet_id})

    return tweet_data, tweet_metadata

from datetime import datetime
import re

def extract_median_price(price_range):
    """
    Extracts the median price from a price range string.
    """
    match = re.search(r'£([\d.]+)-([\d.]+)', price_range)
    if match:
        return (float(match.group(1)) + float(match.group(2))) / 2
    else:
        return None

def transform_uber_data(uber_data, routes_data):
    transformed_uber_ride_data = []
    transformed_uber_price_data = []
    route_id_map = {}

    for route in routes_data:
        start_coordinate = (route['start_coordinate']['latitude'], route['start_coordinate']['longitude'])
        end_coordinate = (route['end_coordinate']['latitude'], route['end_coordinate']['longitude'])
        route_id_map[(start_coordinate, end_coordinate)] = route['route_id']

    current_id = 1  # Initialize a counter for assigning unique IDs

    for uber in uber_data:
        origin_latitude = uber['origin_latitude']
        origin_longitude = uber['origin_longitude']
        destination_latitude = uber['destination_latitude']
        destination_longitude = uber['destination_longitude']

        start_coordinate = (origin_latitude, origin_longitude)
        end_coordinate = (destination_latitude, destination_longitude)

        route_id = route_id_map.get((start_coordinate, end_coordinate), None)

        if route_id is not None:
            ride_id = current_id
            current_id += 1

            transformed_uber_ride_data.append({
                'id': ride_id,
                'time_stamp': datetime.fromtimestamp(uber['timestamp']),  # Convert UNIX timestamp to datetime
                'route_id': route_id,
            })

            prices = uber['prices']
            # Fill in the missing values with None
            prices += [None] * (9 - len(prices))

            transformed_uber_price_data.append({
                'id': ride_id,
                'ride_id': ride_id,
                'x': prices[0],
                'green': prices[1],
                'assist': prices[2],
                'access': prices[3],
                'pet': prices[4],
                'comfort': prices[5],
                'xl': prices[6],
                'exec': prices[7],
                'lux': prices[8],
            })

    return transformed_uber_ride_data, transformed_uber_price_data




def transform_weather_data(weather_data, location_ids, postgres_connection):
    weather_location = []
    weather_main = []
    weather_conditions = []

    for weather in weather_data:
        print("Processing weather data:", weather)
        weather_id = weather['id']
        try:
            condition_id = weather['weather'][0]['id']
        except KeyError as e:
            print(f"KeyError: {e}")
            continue
        
        location_id = location_ids.get((weather['coord']['lat'], weather['coord']['lon']))

        if not location_id:
            # Insert a new train station if location_id is not found
            new_train_station = {
                'id': weather_id,
                'name': f"Train Station {weather_id}",
                'lat': weather['coord']['lat'],
                'long': weather['coord']['lon']
            }
            insert_train_station_data([new_train_station], postgres_connection)
            location_id = weather_id
            location_ids[(weather['coord']['lat'], weather['coord']['lon'])] = location_id

        print(f"Adding weather record for location_id: {location_id}")

        weather_location.append({
            'id': weather_id,
            'location_id': location_id,
            'main_id': condition_id,
            'condition_id': condition_id,
            'dt': datetime.utcfromtimestamp(weather['dt'])
        })

        weather_main.append({
            'id': condition_id,
            'main': weather['weather'][0]['main'],
            'desc': weather['weather'][0]['description']
        })

        weather_conditions.append({
            'id': condition_id,
            'temperature': weather['main']['temp'],
            'feels_like': weather['main']['feels_like'],
            'clouds': weather['clouds']['all']
        })

    print("Weather location records:", len(weather_location))
    print("Weather main records:", len(weather_main))
    print("Weather conditions records:", len(weather_conditions))

    return weather_location, weather_main, weather_conditions

def transform_routes_data(routes_data, weather_data):
    routes = []
    start_location = []
    end_location = []
    location_ids = {}
    hotel_ids = {}

    current_location_id = 1
    current_hotel_id = 1

    for route in routes_data:
        route_id = route['route_id']
        start_lat = route['start_coordinate']['latitude']
        start_long = route['start_coordinate']['longitude']
        end_lat = route['end_coordinate']['latitude']
        end_long = route['end_coordinate']['longitude']

        start_coordinates = (start_lat, start_long)
        end_coordinates = (end_lat, end_long)

        # Generate unique IDs for start and end locations
        if start_coordinates not in location_ids:
            location_id = current_location_id
            current_location_id += 1
            start_location.append({'id': location_id, 'name': 'Train Station', 'lat': start_lat, 'long': start_long})
            location_ids[start_coordinates] = location_id
        else:
            location_id = location_ids[start_coordinates]

        if end_coordinates not in location_ids:
            location_id = current_location_id
            current_location_id += 1
            
            if end_coordinates not in hotel_ids:
                hotel_ids[end_coordinates] = current_hotel_id
                current_hotel_id += 1
            end_location.append({'id': location_id, 'hotel_id': hotel_ids[end_coordinates], 'lat': end_lat, 'long': end_long})
            location_ids[end_coordinates] = location_id
        else:
            location_id = location_ids[end_coordinates]

        routes.append({
            'id': int(route_id),
            'start_location_id': location_ids[start_coordinates],
            'end_location_id': location_ids[end_coordinates]
        })
        print(f"Adding route with id: {route_id}, start_location_id: {location_ids[start_coordinates]}, end_location_id: {location_ids[end_coordinates]}")

    # Add missing weather locations to location_ids
    for weather in weather_data:
        weather_lat = weather.get('latitude')
        weather_long = weather.get('longitude')
        if weather_lat is not None and weather_long is not None:
            weather_coordinates = (weather_lat, weather_long)
            if weather_coordinates not in location_ids:
                location_id = current_location_id
                current_location_id += 1
                start_location.append({'id': location_id, 'name': 'Station', 'lat': weather_lat, 'long': weather_long})
                location_ids[weather_coordinates] = location_id

    return {
        'routes': routes,
        'start_location': start_location,
        'end_location': end_location,
        'location_ids': location_ids
    }



# Insert Data
import psycopg2

def insert_hotel_data(data, postgres_connection):
    hotel_info, hotel_location = data

    with psycopg2.connect(postgres_connection) as conn:
        with conn.cursor() as cur:
            for record in hotel_info:
                cur.execute("""
                    INSERT INTO hotel_info (id, name, neighbourhood)
                    VALUES (%s, %s, %s)
                    ON CONFLICT (id) DO NOTHING;
                """, (record['id'], record['name'], record['neighbourhood']))
            conn.commit()

            for record in hotel_location:
                print(f"Inserting hotel location: {record}")  # Add print statement to check the values being inserted

                # Check if the hotel_id exists in the hotel_info table
                cur.execute("""
                    SELECT COUNT(*) FROM hotel_info WHERE id = %s;
                """, (record['hotel_id'],))
                count = cur.fetchone()[0]
                if count == 0:
                    # Insert the hotel info record if it does not exist
                    cur.execute("""
                        INSERT INTO hotel_info (id, name, neighbourhood)
                        VALUES (%s, %s, %s)
                        ON CONFLICT (id) DO NOTHING;
                    """, (record['hotel_id'], "Unknown", "Unknown"))
                    conn.commit()

                cur.execute("""
                    INSERT INTO hotel_location (id, hotel_id, lat, long)
                    VALUES (%s, %s, %s, %s)
                    ON CONFLICT (id) DO NOTHING;
                """, (record['id'], record['hotel_id'], record['lat'], record['long']))
            conn.commit()


def insert_train_station_data(data, postgres_connection):
    with psycopg2.connect(postgres_connection) as conn:
        with conn.cursor() as cur:
            for record in data:
                cur.execute("""
                    INSERT INTO train_stations (id, name, lat, long)
                    VALUES (%s, %s, %s, %s)
                    ON CONFLICT (id) DO NOTHING;
                """, (record['id'], record['name'], record['lat'], record['long']))
            conn.commit()

def insert_tweet_data(data, connection_string):
    tweet_info, tweet_metadata = data

    with psycopg2.connect(connection_string) as conn:
        with conn.cursor() as cur:
            for record in tweet_info:
                cur.execute("""
                    INSERT INTO tweets (id, text)
                    VALUES (%s, %s)
                    ON CONFLICT (id) DO NOTHING;
                """, (record['id'], record['text']))
            conn.commit()

            for record in tweet_metadata:
                cur.execute("""
                    INSERT INTO tweet_metadata (id, newest_id, oldest_id, result_count, tweet_id)
                    VALUES (%s, %s, %s, %s, %s)
                    ON CONFLICT (id) DO NOTHING;
                """, (record['id'], record['newest_id'], record['oldest_id'], record['result_count'], record['tweet_id']))
            conn.commit()

def insert_uber_data(data, postgres_connection):
    uber_ride_data, uber_price_data = data

    with psycopg2.connect(postgres_connection) as conn:
        with conn.cursor() as cur:
            for record in uber_ride_data:
                cur.execute("""
                    INSERT INTO uber_ride (id, time_stamp, route_id)
                    VALUES (%s, %s, %s)
                    ON CONFLICT (id) DO NOTHING;
                """, (record['id'], record['time_stamp'], record['route_id']))
                print(f"Inserted uber ride with id: {record['id']}, route_id: {record['route_id']}")
            conn.commit()

            for record in uber_price_data:
                cur.execute("""
                    INSERT INTO uber_price (id, ride_id, x, green, assist, access, pet, comfort, xl, exec, lux)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    ON CONFLICT (id) DO NOTHING;
                """, (record['id'], record['ride_id'], record['x'], record['green'], record['assist'], record['access'], record['pet'], record['comfort'], record['xl'], record['exec'], record['lux']))
            conn.commit()






def insert_weather_data(data, postgres_connection):
    weather_location, weather_main, weather_conditions = data

    with psycopg2.connect(postgres_connection) as conn:
        with conn.cursor() as cur:
            # Insert weather_conditions and weather_main records first
            for record in weather_conditions:
                cur.execute("""
                    INSERT INTO weather_conditions (id, temperature, feels_like, clouds)
                    VALUES (%s, %s, %s, %s)
                    ON CONFLICT (id) DO NOTHING;
                """, (record['id'], record['temperature'], record['feels_like'], record['clouds']))
                print(f"Inserted weather_conditions with id: {record['id']}")

            for record in weather_main:
                cur.execute("""
                    INSERT INTO weather_main (id, main, "desc")
                    VALUES (%s, %s, %s)
                    ON CONFLICT (id) DO NOTHING;
                """, (record['id'], record['main'], record['desc']))
                print(f"Inserted weather_main with id: {record['id']}")
            conn.commit()

            # Insert weather_location records after weather_conditions and weather_main
            for record in weather_location:
                cur.execute("""
                    INSERT INTO weather_location (id, location_id, main_id, condition_id, dt)
                    VALUES (%s, %s, %s, %s, %s)
                    ON CONFLICT (id) DO NOTHING;
                """, (record['id'], record['location_id'], record['main_id'], record['condition_id'], record['dt']))
                print(f"Inserted weather_location with id: {record['id']}")
            conn.commit()



def insert_routes_data(routes, start_location, end_location, postgres_connection):
    with psycopg2.connect(postgres_connection) as conn:
        with conn.cursor() as cur:
            for record in routes:
                cur.execute("""
                    INSERT INTO routes (id, start_location_id, end_location_id)
                    VALUES (%s, %s, %s)
                    ON CONFLICT (id) DO NOTHING;
                """, (record['id'], record['start_location_id'], record['end_location_id']))
                print(f"Inserted route with id: {record['id']}, start_location_id: {record['start_location_id']}, end_location_id: {record['end_location_id']}")
            conn.commit()

            for record in start_location:
                cur.execute("""
                    INSERT INTO train_stations (id, name, lat, long)
                    VALUES (%s, %s, %s, %s)
                    ON CONFLICT (id) DO NOTHING;
                """, (record['id'], record['name'], record['lat'], record['long']))
            conn.commit()

            for record in end_location:
                cur.execute("""
                    INSERT INTO hotel_location (id, hotel_id, lat, long)
                    VALUES (%s, %s, %s, %s)
                    ON CONFLICT (id) DO NOTHING;
                """, (record['id'], record['hotel_id'], record['lat'], record['long']))
            conn.commit()

