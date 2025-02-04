import requests
from requests.structures import CaseInsensitiveDict
import os

def geocode_address(address:str) -> tuple:
    """
    Gets the lat and long coordinates for a given address.

    Params:
    address (str): free form address such as a street address, city name, postal code, etc.

    Returns:
    - a tuple of the lat and long coordinates
    """

    # format street address for url
    address_formatted = address.replace(" ", "%20")

    # endpoint
    url = f"https://api.geoapify.com/v1/geocode/search?text={address_formatted}&apiKey={os.environ["GEOAPIFY_KEY"]}"

    headers = CaseInsensitiveDict()
    headers["Accept"] = "application/json"

    resp = requests.get(url, headers=headers)
    print(f"Response from Geoapify geocoder:\n{resp.status_code}")

    d = resp.json()

    lat = d["features"][0]["properties"]["lat"]
    lon = d["features"][0]["properties"]["lon"]

    return lat, lon