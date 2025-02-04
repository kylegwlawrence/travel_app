import requests
import json
import os
from datetime import datetime

def search_ids_near_lat_long(lat:int, lon:int, maxGuestCapacity:int=6, range:int=500, offset:int=0) -> list:
    """
    Takes search filters and returns airbnb ids matching the search criteria.

    Params:
    lat (int): cartesian latitude coordinate
    lon (int): cartesian longitude coordinate
    range (int): range in metres (verify this unit) from latitude and longitude point to define search area
    bedrooms (int): number of bedrooms
    maxGuestCapacity (int): Max guest the listing can accomodate
    offset (int): index to start from

    Returns:
    - list of dicts of airbnbs ids with proximity, in metres(?) to the searched lat, long coordinates
    """

    # endpoint
    url = "https://airbnb-listings.p.rapidapi.com/v2/listingsByLatLng"

    # query
    querystring = {
        "lat":str(lat)
        , "lng":str(lon)
        , "range":str(range)
        , "offset":str(offset)
        , "maxGuestCapacity":str(maxGuestCapacity)
        }
    
    # use primary key first
    headers = {
        "x-rapidapi-key":os.environ["AIRBNB_KEY_1"]
        , "x-rapidapi-host":"airbnb-listings.p.rapidapi.com"
        }

    # try calling with the primary_key
    response = requests.get(url, headers=headers, params=querystring)

    # determine if we need to try the secondary_key
    if response.status_code != 200:
        print(f"Airbnb primary key error, code {response.status_code}. Trying secondary key.")

        # load and try the secondary_key if we get an non-200 repsonse
        headers["x-rapidapi-key"] = os.environ["AIRBNB_KEY_2"]
        response = requests.get(url, headers=headers, params=querystring)

        # raise an exception if the secondary key returns anything other than a 200 code
        if response.status_code != 200:
            raise Exception(f"Secondary key error, code {response.status_code}")
        
    # convert response to json
    response = response.json()
    
    # if there is an error returned with no results, return an empty list
    airbnb_ids=[]
    if "error" in response:
        print(f"""{response["error"]} for lat {lat} and long {lon}""")
    
    # save airbnb_ids and distance from lat, long to a dict and store in a list
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
    Get the listing details for a specific airbnb_id.

    Params:
    airbnb_id (int): the airbnb_id for which we want details

    Returns:
    - dict of listing details
    """

    # endpoint
    url = "https://airbnb-listings.p.rapidapi.com/v2/listing"

    # query
    querystring = {"id":airbnb_id}

    # use primary key first
    headers = {
        "x-rapidapi-key":os.environ["AIRBNB_KEY_1"]
        , "x-rapidapi-host":"airbnb-listings.p.rapidapi.com"
        }

    # try calling with the primary_key
    response = requests.get(url, headers=headers, params=querystring)

    # determine if we need to try the secondary_key
    if response.status_code != 200:
        print(f"Airbnb primary key error, code {response.status_code}. Trying secondary key.")

        # load and try the secondary_key if we get an non-200 repsonse
        headers["x-rapidapi-key"] = os.environ["AIRBNB_KEY_2"]
        response = requests.get(url, headers=headers, params=querystring)

        # raise an exception if the secondary key returns anything other than a 200 code
        if response.status_code != 200:
            raise Exception(f"Secondary key error, code {response.status_code}")

    # access the listing details and store in a dictionary
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
    Gets data on availability for a specific airbnb_id for the next 12 months.

    Params:
    airbnb_id (int): the airbnb_id for which we want availability by day

    Returns:
    - list of results from the api call

    If a date in the range of checkIn and checkOut is not available then return False, otherwise if all days are available then return True
    """

    # endpoint
    url = "https://airbnb-listings.p.rapidapi.com/v2/listingAvailabilityFull"

    # query
    querystring = {"id":airbnb_id}

    # use primary key first
    headers = {
        "x-rapidapi-key":os.environ["AIRBNB_KEY_1"]
        , "x-rapidapi-host":"airbnb-listings.p.rapidapi.com"
        }

    # try calling with the primary_key
    response = requests.get(url, headers=headers, params=querystring)

    # determine if we need to try the secondary_key
    if response.status_code != 200:
        print(f"Airbnb primary key error, code {response.status_code}. Trying secondary key.")

        # load and try the secondary_key if we get an non-200 repsonse
        headers["x-rapidapi-key"] = os.environ["AIRBNB_KEY_2"]
        response = requests.get(url, headers=headers, params=querystring)

        # raise an exception if the secondary key returns anything other than a 200 code
        if response.status_code != 200:
            raise Exception(f"Secondary key error, code {response.status_code}")

    # call api and receive response
    response = requests.get(url, headers=headers, params=querystring)

    # pull data from the response
    results = response.json()["results"]

    return results

def search_availability(results:list, checkIn:str, checkOut:str) -> bool:
    """
    Take the list of results from the availability api call and determines if the airbnb is available for the range of the requested dates.

    Params:
    results (list): the results value from the api call
    checkIn (str): check in date. YYYY-MM-DD
    checkOut (str): check out date. YYYY-MM-DD

    Returns:
    - boolean indicating if the airbnb is available for the requested dates
    - only checks if all days in the stay range are available for both checking-in and staying. There are a few flags for availability: one flags if guests can check in that day and another flags if the unit is available to stay that day. In some cases guests cannot check in on a date however they can stay if their stay is in progress.
    - there might also be edge cases for check-out flag - is this a thing?
    """
    # format checkin and checkout dates
    checkIn = datetime.strptime(checkIn, '%Y-%m-%d')
    checkOut = datetime.strptime(checkOut, '%Y-%m-%d')

    # iterate over each dict (date) in the list
    for day in results:

        # format the date string as datetime
        dt = datetime.strptime(day["date"], '%Y-%m-%d')

        # continue to the next date if the current date is not within the stay range
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