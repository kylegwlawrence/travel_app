import requests
import json
from datetime import datetime

def search_airbnb_listings_lat_long(lat, lng, bedrooms, maxGuestCapacity, range="500", offset="0") -> None:
    """
    Takes search filters and writes the api response to a json file.
    Params:
    lat (str): cartesian latitude coordinate
    lng (str): cartesian longitude coordinate
    range (str): range in meters from latitude and longitude point to define search area
    bedrooms (str): number of bedrooms
    maxGuestCapacity (str): Max guest the listing can accomodate
    offset (str): index to start from
    """

    # api url
    url = "https://airbnb-listings.p.rapidapi.com/v2/listingsByLatLng"

    # search filters
    querystring = {"lat":lat,"lng":lng,"range":range,"offset":offset,"bedrooms":bedrooms,"maxGuestCapacity":maxGuestCapacity}

    # load api key
    with open('key.json', 'r') as f:
        headers = json.load(f)

    # store a response from the request
    response = requests.get(url, headers=headers, params=querystring).json()

    # json file name
    date_time = datetime.now().strftime("%d-%m-%Y_%H:%M:%S")
    file_name=date_time+"_search_listings"

    # write response to json
    with open(f"jsons/search_listings/{file_name}.json", "w") as outfile:
        json.dump(response, outfile)


def search_airbnb_listing_details(id) -> dict:
    """
    Pass in an airbnb id to get its details.
    """
    url = "https://airbnb-listings.p.rapidapi.com/v2/listing"

    querystring = {"id":id}

    # write to a json file
    with open('key.json', 'r') as f:
        headers = json.load(f)

    response = requests.get(url, headers=headers, params=querystring)

    return response.json()

if __name__=='__main__':
   # args={"id":"619966061834034729"}
    #print(search_airbnb_listing_details(**args))

    # test the alt long search

    # load test args
    with open('test_args.json', 'r') as f:
        args = json.load(f)

    print(search_airbnb_listings_lat_long(**args))