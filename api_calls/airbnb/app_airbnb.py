from search import search_airbnb_listings_lat_long, search_airbnb_listing_details
from extract import parse_airbnb_id, parse_airbnb_details
import pandas as pd
import json

def get_airbnbs(lat, lng, bedrooms, maxGuestCapacity, range="500", offset="0") -> pd.DataFrame:
    """
    Runs api call to airbnb to get airbnb ids and their proximity in meters to the lat lng coordinates.
    """
    # call the api and get a reponse
    response = search_airbnb_listings_lat_long(lat, lng, bedrooms, maxGuestCapacity, range, offset)

    # keep only data you need
    airbnbs=parse_airbnb_id(response)

    return airbnbs

def get_details(id)-> pd.DataFrame:
    """
    Grab data from the api and output selected fields as a dataframe
    """
    # call the api and get a repsonse
    response=search_airbnb_listing_details(id)

    # keep data
    airbnb_details=parse_airbnb_details(response)

    return airbnb_details

if __name__=="__main__":
    id = "619966061834034729"
    print(get_details(id))