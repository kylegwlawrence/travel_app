#The Geocoder API accepts both structured and free-form addresses as an input and returns JSON, GeoJSON, and XML objects as a response. In addition, you can specify location filters and preferred geographical areas to make the address search more accurate and focused

import requests
from requests.structures import CaseInsensitiveDict
import json

def geocode(address, fileout="output.json"):
    """
    Accepts a free form typed street address, calls a geocoding api and writes the results to disk
    """

    address_formatted = address.replace(" ", "%20")

    # read api key
    with open("key.json", "r") as f:
        apiKey=json.load(f)["apiKey"]

    url = f"https://api.geoapify.com/v1/geocode/search?text={address_formatted}&apiKey={apiKey}"

    headers = CaseInsensitiveDict()
    headers["Accept"] = "application/json"

    resp = requests.get(url, headers=headers)
    print(resp.status_code)

    # write response to json
    with open(fileout, "w") as f:
        json.dump(resp.json(), f)

def get_coordinates(file_path:str) -> list:
    """Reads the coordinates out of the api results on disk and returns them in a list as latitude, longitude"""
    with open(file_path, "r") as f:
        d=json.load(f)
    
    lat = d["features"][0]["properties"]["lat"]
    lon = d["features"][0]["properties"]["lon"]

    return [lat, lon]
    
if __name__=="__main__":
    fileout="output.json"
    geocode("mixcalco 371 jose Vicente Villada, 57710 Cdad. nezahualcoyotl mexico city, mexico", fileout=fileout)

    c = get_coordinates(fileout)

    print(c)