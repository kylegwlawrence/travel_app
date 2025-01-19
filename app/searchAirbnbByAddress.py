from api_calls.geocoder.app import geocode_address
from api_calls.airbnb.search import search_ids_near_lat_long, search_details, search_availability
import pandas as pd
from datetime import datetime

def search_address(address:str, range:int=500):
    """
    Searches for airbnbs within a range (meters) of an address and returns their details
    """

    # get the geo coordinates for the address
    lat, lon = geocode_address(address)

    # find airbnbs near the set of coordinates
    ids_near_address = search_ids_near_lat_long(str(lat), str(lon), range=str(range))

    # retrieve the information for each airbnb
    list_of_airbnbs = []
    for airbnb in ids_near_address:
        airbnb_details = search_details(airbnb["airbnb_id"])
        list_of_airbnbs.append(airbnb_details)

    return list_of_airbnbs

if __name__=='__main__':
    checkIn = "2025-02-10"
    checkOut = "2025-02-14"
            
    a = search_availability(1124683783587183030, checkIn, checkOut)
    print(a)



if __name__=='__main_':
    d = search_address("820 15 ave sw calgary ab")
    df = pd.DataFrame(d)
    df.to_csv("test_airbnb.csv", index=False)

