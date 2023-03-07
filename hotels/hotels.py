import json
import requests
from bs4 import BeautifulSoup

url = 'https://www.booking.com/searchresults.en-gb.html?ss=London%2C+Greater+London%2C+United+Kingdom'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
}

for page in range(1, 4): # Loop through the first three pages
    params = {
        'page': page,
    }
    response = requests.get(url, headers=headers, params=params)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    property_blocks = soup.find_all('div', {'data-testid': 'property-card'})
    for block in property_blocks:
        # Extract the hotel name
        hotel_name_div = block.find('a', {'data-testid': 'title-link'})
        if hotel_name_div is not None:
            hotel_name = hotel_name_div.text.strip().replace('Opens in new window', '')
            print(hotel_name)

        # Extract the hotel location
        hotel_location_div = block.find('div', {'data-testid': 'location'})
        if hotel_location_div is not None:
            hotel_location = hotel_location_div.find('span', {'class': 'f4bd0794db'}).text.strip()
            print(hotel_location)

        # Extract the number of reviews
        review_div = block.find('div', {'class': 'f919b8b3d5'})
        if review_div is not None:
            review_count = review_div.find('span', {'class': 'cb5ebe3ffb'}).text.strip()
            print(review_count)

        # Add hotel name and location to hotels list
        hotels.append({'name': hotel_name, 'location': hotel_location})
        
# Convert hotels list to JSON format
json_data = json.dumps(hotels, indent=4)

# Print JSON data
print(json_data)