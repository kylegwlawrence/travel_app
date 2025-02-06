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

    # use env variable for key
    apiKey = os.environ["GEOAPIFY_KEY"]

    # endpoint
    url = f"https://api.geoapify.com/v1/geocode/search?text={address_formatted}&apiKey={apiKey}"

    headers = CaseInsensitiveDict()
    headers["Accept"] = "application/json"

    resp = requests.get(url, headers=headers)

    # log to console if we get a non-200 response
    if resp.status_code!=200:
        print(resp.json())

    d = resp.json()

    lat = d["features"][0]["properties"]["lat"]
    lon = d["features"][0]["properties"]["lon"]

    return lat, lon

if __name__=="__main__":
    address = "1709 F Street Bellingham WA"
    lat, long = geocode_address(address)

    print(lat, long)