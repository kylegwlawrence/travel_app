from search import search_airbnb_listings_lat_long
import pandas as pd

def get_airbnbs(payload:dict) -> list:
    """
    Runs api call to airbnb to get listings for a given lat and long
    """
    airbnbs = search_airbnb_listings_lat_long(**payload)

    return airbnbs

if __name__=="__main__":
    payload={
        "lat":"45.5"
        , "lng":"-73.5"
        , "range":"500"
        , "offset":"0"
        , "bedrooms":"1"
        , "maxGuestCapacity":"4"
    }
    airbnbs=get_airbnbs(payload)
    print(airbnbs)