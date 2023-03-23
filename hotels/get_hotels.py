import requests
from bs4 import BeautifulSoup
import json
import os

def get_hotels_booking(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}

    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    data = []
    counter = 0  # Initialize counter for the number of hotels scraped

    property_blocks = soup.find_all('div', {'data-testid': 'property-card'})

    for block in property_blocks:
        if counter == 20:
            break  # Exit the loop if 20 hotels have been scraped

        # Extract the hotel name
        hotel_name_div = block.find('a', {'data-testid': 'title-link'})
        if hotel_name_div is not None:
            hotel_name = hotel_name_div.text.strip().replace('Opens in new window', '')

        # Extract the hotel location
        hotel_location_div = block.find('div', {'data-testid': 'location'})
        if hotel_location_div is not None:
            hotel_location = hotel_location_div.find('span', {'class': 'f4bd0794db'}).text.strip()

        # Store the extracted data in a dictionary
        hotel_data = {
            'name': hotel_name,
            'location': hotel_location,
        }

        # Append the dictionary to the data list
        data.append(hotel_data)
        counter += 1  # Increment the counter for each hotel scraped


    # Write the data to a JSON file
 # Check if the hotels.json file exists. If not, create an empty file.
    if not os.path.exists('/home/ubuntu/output/hotels.json'):
        with open('/home/ubuntu/output/hotels.json', 'w') as f:
            json.dump([], f)

    with open('/home/ubuntu/output/hotels.json', 'w') as f:
        json.dump(data, f)

    print("Hotels saved as hotels.json in output folder")
