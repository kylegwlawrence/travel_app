#The Geocoder API accepts both structured and free-form addresses as an input and returns JSON, GeoJSON, and XML objects as a response. In addition, you can specify location filters and preferred geographical areas to make the address search more accurate and focused

import requests
from requests.structures import CaseInsensitiveDict
import json

def geocode_address(address) -> list:
    """
    Accepts a free form typed street address and returns two variables, lat and lon
    """

    address_formatted = address.replace(" ", "%20")

    # read api key
    with open("api_calls/geocoder/key.json", "r") as f:
        apiKey=json.load(f)["apiKey"]

    url = f"https://api.geoapify.com/v1/geocode/search?text={address_formatted}&apiKey={apiKey}"

    headers = CaseInsensitiveDict()
    headers["Accept"] = "application/json"

    resp = requests.get(url, headers=headers)
    print(resp.status_code)

    d = resp.json()

    lat = d["features"][0]["properties"]["lat"]
    lon = d["features"][0]["properties"]["lon"]

    return lat, lon
    
if __name__=="__main__":
    print(geocode_address("mixcalco 371 jose Vicente Villada, 57710 Cdad. nezahualcoyotl mexico city, mexico"))
