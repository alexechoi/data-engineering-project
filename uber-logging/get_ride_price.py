import json
import requests

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
