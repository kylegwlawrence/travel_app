from api_calls.geocoder.search import geocode_address
from api_calls.priceline.search import search_location_ids, search_hotels
import pandas as pd

def search(coordinates:tuple, checkIn:str, checkOut:str, limit:int, page:int=1) -> list:
    """
    Takes a freeform addressand check in and checkout date to find matching hotels.
    
    Params:
    coordinates (tuple): search area as (lat, long)
    checkIn (str): check in time formatted "yyyy-mm-dd"
    checkOut (str): check out time formatted "yyyy-mm-dd"
    limit (int): number of records to limit per page.
    page (int): index of page to return, 1-indexed. Defaults to first page. 

    Returns: 
    - list of dictionaries
    - empty list if there are no exactly matching cities for the given address
    """

    # find location ids near set of coordinates
    location_ids = search_location_ids(coordinates[0], coordinates[1])

    # try to get the location_id that matches exactly to the lat lon coordinates
    try:
        matched_location_id = location_ids["data"]["exactMatch"]["matchedCity"]["cityID"]
        # use location id to search for hotels
        hotels = search_hotels(locationId=matched_location_id, checkIn=checkIn, checkOut=checkOut, limit=limit, page=page)
    
    # return None if there is an error finding the exactly matching city
    except: 
        print(f"No exactly-matching city ID available for {coordinates}")
        hotels = None

    return hotels