import requests
import os
import json
from datetime import datetime

def get_airbnbs_near_lat_long(lat:int, lon:int, maxGuestCapacity:int=6, range:int=500, offset:int=0) -> list:
    """
    Searches for airbnbs matching the criteria arguments
    Params:
    - lat (int): cartesian latitude coordinate
    - lon (int): cartesian longitude coordinate
    - range (int): range in metres (verify this unit) from latitude and longitude point to define search area
    - bedrooms (int): number of bedrooms
    - maxGuestCapacity (int): Max guest the listing can accomodate
    - offset (int): index to start from
    Returns:
    - (list of dictionaries): airbnbs ids and proximity, in meters, to the searched coordinates.
    """

    with open("api_params.json", "r") as f:
        api_params = json.load(f)

    querystring = {
        "lat":str(lat),
        "lng":str(lon),
        "range":str(range),
        "offset":str(offset),
        "maxGuestCapacity":str(maxGuestCapacity)
        }
    # use primary key first
    headers = {
        "x-rapidapi-key":os.environ["AIRBNB_KEY_1"],
        "x-rapidapi-host":api_params["x-rapidapi-host"]
        }
    response = requests.get(api_params["endpoint_lat_long"], headers=headers, params=querystring)

    if response.status_code != 200:
        print(f"Primary key error: {response.status_code}")

        # try the second key
        headers["x-rapidapi-key"] = os.environ["AIRBNB_KEY_2"]
        response = requests.get(api_params["endpoint_lat_long"], headers=headers, params=querystring)

        if response.status_code != 200:
            raise Exception(f"Secondary key error: {response.status_code}")
        
    response = response.json()
 
    airbnb_ids=[]
    for airbnb in response["results"]:
        airbnb_ids.append(
            {
                "airbnb_id":airbnb["airbnb_id"],
                "distance":airbnb["distance"]
            }
        )

    return airbnb_ids

def get_airbnb_details(airbnb_id:int) -> dict:
    """
    Get the listing details for a specific airbnb
    Params:
    - airbnb_id (int): the airbnb_id for which we want details
    Returns:
    - (dictionary): listing details
    """

    with open("api_params.json", "r") as f:
        api_params = json.load(f)

    querystring = {"id":airbnb_id}
    # use primary key first
    headers = {
        "x-rapidapi-key":os.environ["AIRBNB_KEY_1"],
        "x-rapidapi-host":api_params["x-rapidapi-host"]
        }
    response = requests.get(api_params["endpoint_details"], headers=headers, params=querystring)

    if response.status_code != 200:
        print(f"Primary key error: {response.status_code}")
        # try the secondary key
        headers["x-rapidapi-key"] = os.environ["AIRBNB_KEY_2"]
        response = requests.get(api_params["endpoint_details"], headers=headers, params=querystring)
        if response.status_code != 200:
            raise Exception(f"Secondary key error: {response.status_code}")

    response = response.json()

    details_dict = response["results"][0]
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
    Gets data on availability for a specific airbnb for the next 12 months.
    If a date in the range of checkIn and checkOut is not available then return False, otherwise if all days are available then return True
    Params:
    - airbnb_id (int): the airbnb_id for which we want availability by day
    Returns:
    - (list): results from the api call
    """

    with open("api_params.json", "r") as f:
        api_params = json.load(f)

    querystring = {"id":airbnb_id}
    # use primary key first
    headers = {
        "x-rapidapi-key":os.environ["AIRBNB_KEY_1"],
        "x-rapidapi-host":api_params["x-rapidapi-host"]
        }
    response = requests.get(api_params["endpoint_availability"], headers=headers, params=querystring)

    if response.status_code != 200:
        print(f"Primary key error: {response.status_code}")
        # try the second key
        headers["x-rapidapi-key"] = os.environ["AIRBNB_KEY_2"]
        response = requests.get(api_params["endpoint_availability"], headers=headers, params=querystring)
        if response.status_code != 200:
            raise Exception(f"Secondary key error: {response.status_code}")

    response = response.json()

    return response["results"]

def get_availability(results:list, checkIn:str, checkOut:str) -> bool:
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