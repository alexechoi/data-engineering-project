import requests
import json
from datetime import datetime, timedelta

bearer_token = '***REMOVED***'

query = "uber London OR #uber #London"
max_results = 20

# Set the time interval to the last hour
#end_time = datetime.utcnow().replace(second=0, microsecond=0).isoformat() + 'Z'
#start_time = (datetime.utcnow() - timedelta(hours=1)).replace(second=0, microsecond=0).isoformat() + 'Z'

start_time = '2023-03-1T00:00:00Z'
end_time = '2023-03-4T00:00:00Z'

# Prepare the headers to pass the authentication to Twitter's api
headers = {
    'Authorization': 'Bearer {}'.format(bearer_token),
}

params = (
    ('query', query),
    ('max_results', str(int(max_results))),
    ('start_time', start_time),
    ('end_time', end_time),
)

# Does the request to get the most recent tweets
response = requests.get('https://api.twitter.com/2/tweets/search/recent', headers=headers, params=params)

# Validates that the query was successful
if response.status_code == 200:
    print("URL of query:", response.url)
    
    # Let's convert the query result to a dictionary that we can save as a json file
    tweets =  json.loads(response.text)
    
    # Save the json file
    with open("twitterQuery.json", "w+") as json_file:
        json_string = json.dumps(tweets, sort_keys=True, indent=4)
        json_file.write(json_string)
        
if response.status_code == 200:
    print("URL of query:", response.url)
    
    # Let's convert the query result to a dictionary that we can save as a json file
    try:
        tweets =  json.loads(response.text)
    except json.JSONDecodeError as e:
        print("Error decoding JSON:", e)
        tweets = {}
    
    # Save the json file
    with open("twitterQuery.json", "w+") as json_file:
        json_string = json.dumps(tweets, sort_keys=True, indent=4)
        json_file.write(json_string)
else:
    print("Request failed with status code", response.status_code)
    print("Response text:", response.text)
