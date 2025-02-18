import requests
from requests.structures import CaseInsensitiveDict
import os
import json

def geocode_address(address:str) -> tuple:
    """
    Gets the lat and long coordinates for a given address.
    Params:
    address (str): free form address such as a street address, city name, postal code, etc.
    Returns:
    - (tuple): the lat and long coordinates
    """

    apiKey = os.environ["GEOAPIFY_KEY"]
    url = f"https://api.geoapify.com/v1/geocode/search?text={address.replace(" ", "%20")}&apiKey={apiKey}"
    headers = CaseInsensitiveDict()
    headers["Accept"] = "application/json"

    response = requests.get(url, headers=headers)

    if response.status_code!=200:
        print(response.json())
        raise

    d = response.json()

    lat = d["features"][0]["properties"]["lat"]
    lon = d["features"][0]["properties"]["lon"]

    return lat, lon

def geocode_multiple_addresses(addresses:list):
    """Coordiantes for a list of addresses"""
    geocoded_addresses = []
    for address in addresses:
        geocoded_addresses.append(geocode_address(address))

    return geocoded_addresses

if __name__=="__main__":
    address = "1709 F Street Bellingham WA"
    lat, long = geocode_address(address)

    print(lat, long)