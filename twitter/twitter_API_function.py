import requests
import json
import datetime

def search_tweets(bearer_token, query, max_results):
    # Prepare the headers to pass the authentication to Twitter's api
    headers = {
        'Authorization': 'Bearer {}'.format(bearer_token),
    }

    # Set start_time to 1 day before the current time and end_time to the current time
    now = datetime.datetime.now(datetime.timezone.utc)
    start_time = (now - datetime.timedelta(days=1)).strftime('%Y-%m-%dT%H:%M:%SZ')
    end_time = now.strftime('%Y-%m-%dT%H:%M:%SZ')

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
        try:
            tweets = json.loads(response.text)
        except json.JSONDecodeError as e:
            print("Error decoding JSON:", e)
            tweets = {}

        # Save the json file
        with open("/home/ubuntu/output/twitter.json", "w+") as json_file:
            json_string = json.dumps(tweets, sort_keys=True, indent=4)
            json_file.write(json_string)

    else:
        print("Request failed with status code", response.status_code)
        print("Response text:", response.text)

# Call the function with the desired variables as arguments
bearer_token = '***REMOVED***'
query = "uber London OR #uber #London"
max_results = 20
search_tweets(bearer_token, query, max_results)


