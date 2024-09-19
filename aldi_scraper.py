from geopy.geocoders import Nominatim
from bs4 import BeautifulSoup
import requests
import json
import time

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36"
}
geolocator = Nominatim(user_agent="aldi_scraper")

# Geocoding (address to coordinates)
location = geolocator.geocode("1300 Fairmount Ave, Philadelphia")
print(location.latitude)

def get_product_links(query, location, page_number=1):
    location_data = [location.latitude, location.longitude]
    search_url = f"https://new.aldi.us/results?q={query}&latitude={location_data[0]}&longitude={location_data[1]}"
    print(search_url)
    response = requests.get(search_url, headers=HEADERS)
    
    # Sleep for 5 seconds to allow the page to load
    time.sleep(5)
    
    soup = BeautifulSoup(response.text, "html.parser")
    
    # print(soup.prettify)
    
    links = soup.find_all("div", class_="product-tile")
    print(links)
    product_links = []
    
    for link in links:
        link_href = link['href']
        if "/product" in link_href:
            if "https" in link_href:
                full_url = link_href
            else:
                full_url = "https://new.aldi.us" + link_href
            
            product_links.append(full_url)
            
    return product_links

def main():
    x = 0
    
    print(get_product_links("chicken", location))

if __name__ == "__main__":
    main()
    
