from api_calls.geocoder.app import geocode_address
from api_calls.priceline.search import search_location_ids, search_hotels

def search(address:str, checkIn:str, checkOut:str, limit:int, page:int=1) -> list:
    """
    Takes a freeform addressand check in and checkout date to find matching hotels.
    Params:
    address (str): physical address or location. Can be any form of geographicaly category but being specific is better to reduce the amount of results returned. 
    checkIn (str): check in time formatted "yyyy-mm-dd"
    checkOut (str): check out time formatted "yyyy-mm-dd"
    limit (int): number of records to limit per page.
    page (int): index of page to return, 1-indexed. Defaults to first page. 
    """

    # get the geo coordinates for the address
    lat, lon = geocode_address(address)
    print(f"Coordinates: {lat}, {lon}")

    # find location ids near set of coordinates
    location_ids = search_location_ids(lat, lon)

    # get the location_id that matches exactly to the lat lon coordinates
    try:
        matched_location_id = location_ids["data"]["exactMatch"]["matchedCity"]["cityID"]
        # use location id to search for hotels
        hotels = search_hotels(locationId=matched_location_id, checkIn=checkIn, checkOut=checkOut, limit=limit, page=page)
    except: 
        print("No exactly-matching city ID available")
        hotels=None

    return hotels

if __name__=='__main__':
    print(search("Eureka Montana", "2025-04-12", "2025-04-14", limit=2))