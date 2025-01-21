from api_calls.geocoder.app import geocode_address
from api_calls.airbnb.search import search_ids_near_lat_long, search_details, search_availability, get_calendar

def search_address(address:str, checkIn:str, checkOut:str, range:int=500):
    """
    Searches for airbnbs within a distance range (meters) of the given lat and long and returns listing details for available airbnbs. 
    """

    # get the geo coordinates for the address
    lat, lon = geocode_address(address)

    # find airbnbs near the set of coordinates
    ids_near_address = search_ids_near_lat_long(str(lat), str(lon), range=str(range))

    # pass by the remainder of the function if there are no results
    if len(ids_near_address) == 0:
        pass

    else:
        # find which airbnbs are available and grab their listing details
        # iterate over each airbnb found within the search range
        list_of_airbnbs = []
        for airbnb in ids_near_address:

            # get the unique id
            airbnb_id = airbnb["airbnb_id"]

            # airbnb being itereated over now
            print(f"Searching Airbnb ID: {airbnb_id}")

            # retrieve availability for each airbnb
            calendar = get_calendar(airbnb_id)
            is_available = search_availability(calendar, checkIn, checkOut)

            # if this airbnb is not available then move onto next airbnb
            if is_available==False:
                print(f"Airbnb {airbnb_id} not available")
                continue

            # get listing data if the airbnb is available
            elif is_available:
                # retrieve listing details for each airbnb
                airbnb_details = search_details(airbnb_id)
                list_of_airbnbs.append(airbnb_details)

            else:
                raise Exception("Parameter returned `is_available` is neither True nor False")
        
    return list_of_airbnbs

if __name__=='__main__':
    checkIn = "2025-05-10"
    checkOut = "2025-05-14"
    a = search_address("820 15 Ave SW Calgary Alberta", checkIn, checkOut, range=500)
    print(a)