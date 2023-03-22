import json
import os
import requests
import time

def get_ride_price(json_file_path):
    url = "https://www.uber.com/api/loadFEEstimates?localeCode=en"
    
    with open(json_file_path, 'r') as f:
        data = json.load(f)
        for route_data in data.values():
            origin_latitude = route_data['start_coordinate']['latitude']
            origin_longitude = route_data['start_coordinate']['longitude']
            destination_latitude = route_data['end_coordinate']['latitude']
            destination_longitude = route_data['end_coordinate']['longitude']


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

    # Add timestamp, latitude, and longitude to result
    timestamp = int(time.time())
    readable_timestamp = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(timestamp))
    result_with_timestamp = {
        "timestamp": timestamp, 
        "readable_timestamp": readable_timestamp, 
        "origin_latitude": origin_latitude,
        "origin_longitude": origin_longitude,
        "destination_latitude": destination_latitude,
        "destination_longitude": destination_longitude,
        "prices": result
    } 

    # Print current working directory
    print("Current working directory:", os.getcwd())
    
    # Append result with timestamp to file
    output_dir = "/home/ubuntu/output/"
    os.makedirs(output_dir, exist_ok=True)
    file_path = os.path.join(output_dir, "uber.json")
    print("Output file path:", os.path.abspath(file_path))
    if os.path.exists(file_path) and os.path.getsize(file_path) > 0:
        with open(file_path, "r") as f:
            data = json.load(f)
    else:
        data = []
    data.append(result_with_timestamp)
    with open(file_path, "w+") as f:
        json.dump(data, f)
    print('Ride prices saved to uber.json')
    
    return result_with_timestamp