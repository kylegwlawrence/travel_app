from api_calls.geocoder.app import geocode_address
from api_calls.airbnb.search import listings_near_lat_long, listing_details
import pandas as pd

def search(address:str, range:int=500):
    # get the geo coordinates for the address
    lat, lon = geocode_address(address)
    print(f"Coordinates: {lat}, {lon}")

    # find airbnbs near the set of coordinates
    airbnbs_near_address = listings_near_lat_long(str(lat), str(lon), range=str(range))
    print(airbnbs_near_address)

    # retrieve the information for each airbnb
    list_of_airbnbs = []
    for airbnb in airbnbs_near_address:
        airbnb_details = listing_details(airbnb["airbnb_id"])
        list_of_airbnbs.append(airbnb_details)

    return list_of_airbnbs

if __name__=='__main__':
    d = search("820 15 ave sw calgary ab")
    df = pd.DataFrame(d)
    df.to_csv("test_airbnb.csv", index=False)