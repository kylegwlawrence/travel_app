import requests
import json
from datetime import datetime

def search_ids_near_lat_long(lat:int, lon:int, maxGuestCapacity:int=6, range:int=500, offset:int=0) -> list:
    """
    Takes search filters and returns airbnb data matching the search criteria.
    Params:
    lat (int): cartesian latitude coordinate
    lon (int): cartesian longitude coordinate
    range (int): range in meters from latitude and longitude point to define search area
    bedrooms (int): number of bedrooms
    maxGuestCapacity (int): Max guest the listing can accomodate
    offset (int): index to start from

    Returns a list of airbnb ids matching the search criteria.
    """

    # api url
    url = "https://airbnb-listings.p.rapidapi.com/v2/listingsByLatLng"

    # build query params
    querystring = {
        "lat":str(lat)
        , "lng":str(lon)
        , "range":str(range)
        , "offset":str(offset)
        , "maxGuestCapacity":str(maxGuestCapacity)
        }

    # load api keys
    with open('api_calls/airbnb/key.json', 'r') as f:
        d = json.load(f)

    # use primary key first
    headers = {
        "x-rapidapi-key":d["primary_key"]
        , "x-rapidapi-host":d["x-rapidapi-host"]
        }

    # try calling with the primary_key
    response = requests.get(url, headers=headers, params=querystring)

    # determine if we need to try the secondary_key
    if response.status_code != 200:
        print(f"Primary key error, code {response.status_code}. Trying secondary key.")

        # load and try the secondary_key if we get an non-200 repsonse
        headers["x-rapidapi-key"] = d["secondary_key"]
        response = requests.get(url, headers=headers, params=querystring)

        # raise an exception if the secondary key returns anything other than a 200 code
        if response.status_code != 200:
            raise Exception(f"Secondary key error, code {response.status_code}")
        
    # convert response to json
    response = response.json()
    
    # if there are no results, return an empty list
    airbnb_ids=[]
    if "error" in response:
        print(f"""{response["error"]} for lat {lat} and long {lon}""")
    
    # save airbnb_ids and distance from lat, long to a dict
    else:
        for airbnb in response["results"]:
            airbnb_ids.append(
                {
                    "airbnb_id":airbnb["airbnb_id"]
                    , "distance":airbnb["distance"]
                }
            )

    return airbnb_ids

def search_details(airbnb_id:int) -> dict:
    """
    Pass in an airbnb id and write the response to json.
    """

    # api url
    url = "https://airbnb-listings.p.rapidapi.com/v2/listing"

    # search filters
    querystring = {"id":airbnb_id}

    # load api keys
    with open('api_calls/airbnb/key.json', 'r') as f:
        d = json.load(f)

    # use primary key first
    headers = {
        "x-rapidapi-key":d["primary_key"]
        , "x-rapidapi-host":d["x-rapidapi-host"]
        }

    # try calling with the primary_key
    response = requests.get(url, headers=headers, params=querystring)

    # determine if we need to try the secondary_key
    if response.status_code != 200:
        print(f"Primary key error, code {response.status_code}. Trying secondary key.")

        # load and try the secondary_key if we get an non-200 repsonse
        headers["x-rapidapi-key"] = d["secondary_key"]
        response = requests.get(url, headers=headers, params=querystring)

        # raise an exception if the secondary key returns anything other than a 200 code
        if response.status_code != 200:
            raise Exception(f"Secondary key error, code {response.status_code}")

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

def get_calendar(airbnb_id:int) -> list:
    """
    Calls API and returns data on availability for a specific airbnb for the next 12 months.
    If a date in the range of checkIn and checkOut is not available then return False, otherwise if all days are available then return True
    """

    url = "https://airbnb-listings.p.rapidapi.com/v2/listingAvailabilityFull"
    querystring = {"id":airbnb_id}

    # load api keys
    with open('api_calls/airbnb/key.json', 'r') as f:
        d = json.load(f)

    # use primary key first
    headers = {
        "x-rapidapi-key":d["primary_key"]
        , "x-rapidapi-host":d["x-rapidapi-host"]
        }

    # try calling with the primary_key
    response = requests.get(url, headers=headers, params=querystring)

    # determine if we need to try the secondary_key
    if response.status_code != 200:
        print(f"Primary key error, code {response.status_code}. Trying secondary key.")

        # load and try the secondary_key if we get an non-200 repsonse
        headers["x-rapidapi-key"] = d["secondary_key"]
        response = requests.get(url, headers=headers, params=querystring)

        # raise an exception if the secondary key returns anything other than a 200 code
        if response.status_code != 200:
            raise Exception(f"Secondary key error, code {response.status_code}")

    # call api and receive response
    response = requests.get(url, headers=headers, params=querystring)

    # pull data from the response
    results = response.json()["results"]

    return results

def search_availability(results, checkIn, checkOut) -> bool:
    """
    Take the results from the availability api call and determines if the airbnb is available for the range of the stay
    """
    # format checkin and checkout dates
    checkIn = datetime.strptime(checkIn, '%Y-%m-%d')
    checkOut = datetime.strptime(checkOut, '%Y-%m-%d')

    # iterate over each dict in the list
    for day in results:

        # format the date string as datetime
        dt = datetime.strptime(day["date"], '%Y-%m-%d')

        # continue to the next loop if the calendar day is not within the stay range
        if dt < checkIn or dt > checkOut:
            continue

        # if the day is in the stay range then check if it is available
        elif dt >= checkIn and dt <= checkOut:

            # continue the loop to check if the next day is available
            if day["available"]==1:
                is_available = True

            # break the loop if there is a day in the stay range that is unavailable
            else:
                is_available = False
                break

    return is_available

if __name__=="__main__":
    ids = search_ids_near_lat_long(51.05, -114.07)
    print(ids)