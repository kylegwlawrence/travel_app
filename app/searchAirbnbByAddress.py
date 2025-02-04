from app.api_calls.geocoder.search import geocode_address
from api_calls.airbnb.search import search_near_lat_long, search_details, search_availability, get_calendar

def search(address:str, checkIn:str, checkOut:str, range:int=500) -> list:
    """
    Searches for airbnbs and returns the listing details for each airbnb as a list of dictionaries

    Params:
    address (str): free form address for the search centroid
    checkIn (str): desired check in date
    checkOut (str): desired check out date
    range (int): the search radius in metres

    Returns: 
    - list of dictionaries
    - an empty list if there are no available airbnbs for the serached date range
    - passes by this function if there are no airbnbs found within the range of the address
    """

    # get the geo coordinates for the address
    lat, lon = geocode_address(address)

    # find airbnbs near the set of coordinates
    ids_near_address = search_near_lat_long(str(lat), str(lon), range=str(range))

    # hold airbnb listing details
    list_of_airbnbs = []

    # pass by the remainder of the function if there are no results
    if len(ids_near_address) == 0:
        pass

    # find which airbnbs are available and grab their listing details
    else:
        for airbnb in ids_near_address:

            # get the unique airbnb id
            airbnb_id = airbnb["airbnb_id"]

            # retrieve availability dates
            calendar = get_calendar(airbnb_id)
            is_available = search_availability(calendar, checkIn, checkOut)

            # if this airbnb is not available then move onto next airbnb
            if is_available==False:
                continue

            # if it is available, get listing details
            elif is_available:
                airbnb_details = search_details(airbnb_id)
                list_of_airbnbs.append(airbnb_details)

            # raise value error if "is_available" is neither True nor False
            else:
                raise ValueError(f"""Parameter returned "is_available" = {is_available} is neither True nor False""")
        
    return list_of_airbnbs

if __name__=='__main__':
    checkIn = "2025-05-10"
    checkOut = "2025-05-14"
    a = search("820 15 Ave SW Calgary Alberta", checkIn, checkOut, range=500)
    print(a)