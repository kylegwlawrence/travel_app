from app.api_calls.geocoder.search import geocode_address
from api_calls.priceline.search import search_location_ids, search_hotels
import pandas as pd

def search(address:str, checkIn:str, checkOut:str, limit:int, page:int=1) -> list:
    """
    Takes a freeform addressand check in and checkout date to find matching hotels.
    
    Params:
    address (str): physical address or location. Can be any form of geographicaly category but being specific is better to reduce the amount of results returned. 
    checkIn (str): check in time formatted "yyyy-mm-dd"
    checkOut (str): check out time formatted "yyyy-mm-dd"
    limit (int): number of records to limit per page.
    page (int): index of page to return, 1-indexed. Defaults to first page. 

    Returns: 
    - list of dictionaries
    - empty list if there are no exactly matching cities for the given address
    """

    # get the geo coordinates for the address
    lat, lon = geocode_address(address)

    # find location ids near set of coordinates
    location_ids = search_location_ids(lat, lon)

    # try to get the location_id that matches exactly to the lat lon coordinates
    try:
        matched_location_id = location_ids["data"]["exactMatch"]["matchedCity"]["cityID"]
        # use location id to search for hotels
        hotels = search_hotels(locationId=matched_location_id, checkIn=checkIn, checkOut=checkOut, limit=limit, page=page)
    
    # return None if there is an error finding the exactly matching city
    except: 
        print(f"No exactly-matching city ID available for {address}")
        hotels=[]

    return hotels

if __name__=='__main__':
    d = search("820 15 ave SW calgary ab", "2025-05-11", "2025-05-14", limit=10)
    df = pd.DataFrame(d)
    df.to_csv("test_priceline.csv", index=False)