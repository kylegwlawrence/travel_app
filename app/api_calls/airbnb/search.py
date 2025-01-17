import requests
import json
from datetime import datetime

def listings_near_lat_long(lat:int, lon:int, maxGuestCapacity:int=6, range:int=500, offset:int=0) -> list:
    """
    Takes search filters and returns airbnb data matching the search criteria.
    Params:
    lat (int): cartesian latitude coordinate
    lng (int): cartesian longitude coordinate
    range (int): range in meters from latitude and longitude point to define search area
    bedrooms (int): number of bedrooms
    maxGuestCapacity (int): Max guest the listing can accomodate
    offset (int): index to start from

    Returns a list of airbnb ids matching the search criteria.
    """

    # api url
    url = "https://airbnb-listings.p.rapidapi.com/v2/listingsByLatLng"

    querystring = {"lat":str(lat),"lng":str(lon),"range":str(range),"offset":str(offset),"maxGuestCapacity":str(maxGuestCapacity)}

    # load api key
    with open('api_calls/airbnb/key.json', 'r') as f:
        headers = json.load(f)

    response = requests.get(url, headers=headers, params=querystring).json()

    # print if there is no data available.
    if response["results"] == None:
        print("No data available.")

    airbnb_ids=[]
    for airbnb in response["results"]:
        airbnb_ids.append(
            {
                "airbnb_id":airbnb["airbnb_id"]
                , "distance":airbnb["distance"]
            }
        )

    return airbnb_ids

def listing_details(id) -> dict:
    """
    Pass in an airbnb id and write the response to json.
    """

    # api url
    url = "https://airbnb-listings.p.rapidapi.com/v2/listing"

    # search filters
    querystring = {"id":id}

    # load api key
    with open('api_calls/airbnb/key.json', 'r') as f:
        headers = json.load(f)

    response = requests.get(url, headers=headers, params=querystring)

    details_dict = response.json()["results"][0]
    airbnb_details = {
            "airbnb_id":details_dict["airbnb_id"]
            , "city":details_dict["city"]
            , "listingTitle": details_dict["listingTitle"]
            , "reviewCount":details_dict["reviewCount"]
            , "starRating":details_dict["starRating"]
            , "maxGuestCapacity":details_dict["maxGuestCapacity"]
            , "bedrooms":details_dict["bedrooms"]
            , "beds":details_dict["beds"]
            , "bathrooms":details_dict["bathrooms"]
            , "bathroomShared":details_dict["bathroomShared"]
            , "propertyType":details_dict["propertyType"]
            , "listingLat":details_dict["listingLat"]
            , "listingLng":details_dict["listingLng"]
            , "cancel_policy":details_dict["cancel_policy"]
            , "min_nights":details_dict["min_nights"]
            , "max_nights":details_dict["max_nights"]
            , "check_in_time":details_dict["check_in_time"]
            , "check_out_time":details_dict["check_out_time"]
            , "listingstatus":details_dict["listingstatus"]
        }

    return airbnb_details