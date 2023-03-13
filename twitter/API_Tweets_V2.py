{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": 1,
   "id": "88d3ad21",
   "metadata": {},
   "outputs": [],
   "source": [
    "import requests\n",
    "import json\n",
    "from datetime import datetime, timedelta\n",
    "\n",
    "def search_twitter(bearer_token, query, max_results, start_time, end_time):\n",
    "    # Prepare the headers to pass the authentication to Twitter's api\n",
    "    headers = {\n",
    "        'Authorization': 'Bearer {}'.format(bearer_token),\n",
    "    }\n",
    "\n",
    "    params = (\n",
    "        ('query', query),\n",
    "        ('max_results', str(int(max_results))),\n",
    "        ('start_time', start_time),\n",
    "        ('end_time', end_time),\n",
    "    )\n",
    "\n",
    "    # Does the request to get the most recent tweets\n",
    "    response = requests.get('https://api.twitter.com/2/tweets/search/recent', headers=headers, params=params)\n",
    "\n",
    "    # Validates that the query was successful\n",
    "    if response.status_code == 200:\n",
    "        print(\"URL of query:\", response.url)\n",
    "\n",
    "        # Let's convert the query result to a dictionary that we can save as a json file\n",
    "        try:\n",
    "            tweets =  json.loads(response.text)\n",
    "        except json.JSONDecodeError as e:\n",
    "            print(\"Error decoding JSON:\", e)\n",
    "            tweets = {}\n",
    "\n",
    "        # Save the json file\n",
    "        with open(\"twitterQuery.json\", \"w+\") as json_file:\n",
    "            json_string = json.dumps(tweets, sort_keys=True, indent=4)\n",
    "            json_file.write(json_string)\n",
    "\n",
    "    else:\n",
    "        print(\"Request failed with status code\", response.status_code)\n",
    "        print(\"Response text:\", response.text)\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 5,
   "id": "28104008",
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "URL of query: https://api.twitter.com/2/tweets/search/recent?query=uber+London+OR+%23uber+%23London&max_results=20&start_time=2023-03-7T00%3A00%3A00Z&end_time=2023-03-12T00%3A00%3A00Z\n"
     ]
    }
   ],
   "source": [
    "bearer_token = '***REMOVED***'\n",
    "\n",
    "query = \"uber London OR #uber #London\"\n",
    "max_results = 20\n",
    "\n",
    "start_time = '2023-03-7T00:00:00Z'\n",
    "end_time = '2023-03-12T00:00:00Z'\n",
    "\n",
    "search_twitter(bearer_token, query, max_results, start_time, end_time)\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "84cde339",
   "metadata": {},
   "outputs": [],
   "source": []
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.8.8"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 5
}
