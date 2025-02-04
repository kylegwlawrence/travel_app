import requests
import os

def search_driving_directions(coordinates:list) -> dict:
    """
    Pass in a list of a list of coordinates and return the directions as a geojson formatted dict.
    If only list of coordinates are passed - one start and one end - then one segment of directions is returned. If more than 2 sets of coordinates are provided then there are multiple segments of directions returned. 

    An example: coordinates=[[49.41461,8.681495], [49.41943,8.686507], [49.420318, 8.687872]]. This will give directions between the first two lists of coordinates as segment one and then directions between the last two coordinates as segment two. 

    Params:
    coordinates (list of lists of floats): a list of a list of cartesian coordinates that define start and end points for each segment. Must be format [latitude, longitude].

    Returns: 
    - dict of driving directions
    """

    # reverse the individual lists of coordinates for the api input. API takes longitude, latitude instead of standard latitude, longitude. 
    reversed_coordinates=[]   
    for c in coordinates:
        r = c[::-1]
        reversed_coordinates.append(r)

    # pass in at least 2 sets of coordinates
    body = {"coordinates":reversed_coordinates}

    # define headers for api request
    headers = {
        'Accept': 'application/json, application/geo+json, application/gpx+xml, img/png; charset=utf-8',
        'Authorization': os.environ["OPENROUTE_KEY"],
        'Content-Type': 'application/json; charset=utf-8'
    }

    # call api and log status to console
    call = requests.post('https://api.openrouteservice.org/v2/directions/driving-car/geojson', json=body, headers=headers)
    print(call.status_code, call.reason)

    # log to console if we get a non-200 response
    if call.status_code!=200:
        print(call.json())

    return call.json()

def parse_info(addresses:list, response:dict) -> list:
    """
    Takes the response from the driving directions api and parses out key information.

    Params:
    addresses (list): list of addresses defining each segment sequentially
    response (dict): the response dictionary from the api call

    Returns:
    - list of dicts of key information for driving:
        - segment number
        - distance in metres
        - duration in seconds
        - start and end addresses
    """

    # init vars
    important_info = []
    segment_number = 1

    # access the segments info
    for segment in response["features"][0]["properties"]["segments"]:

        # grab the important segment info
        distance = segment["distance"]
        duration = segment["duration"]

        # start and endpoints per segment
        start_address = addresses[segment_number-1]
        end_address = addresses[segment_number]

        # add each segment info to list
        d = {
            "segment_number":segment_number
            , "distance":distance
            , "duration":duration
            , "start_address":start_address
            , "end_address":end_address}
        important_info.append(d)

        # move to next segment
        segment_number+=1

    return important_info

def search_isochrone(coordinates:list, driving_times:list) -> dict:
    """
    Pass in one or multiple sets of coordinates to get an area that is accessible within a given driving time.

    Params:
    coordinates (list of lists of floats): list of a lists of coordinates (lat long)
    driving_time (list of floats): length of driving times in hours to define the boundaries of the isochrone. Pass in a list of multiple values to get multiple isochrones per location.

    Returns:
    - dict of isochrone geometry objects
    """

    # endpoint
    url = "https://api.openrouteservice.org/v2/isochrones/driving-car"

    # reverse the individual lists of coordinates for the api input. API takes longitude, latitude instead of standard latitude, longitude. 
    reversed_coordinates=[]   
    for c in coordinates:
        r = c[::-1]
        reversed_coordinates.append(r)

    # convert driving times to seconds
    driving_times_seconds = [hrs*60*60 for hrs in driving_times]

    # query
    query = {"locations":reversed_coordinates, "range":driving_times_seconds}

    headers = {
        'Accept': 'application/json, application/geo+json, application/gpx+xml, img/png; charset=utf-8',
        'Authorization': os.environ["OPENROUTE_KEY"],
        'Content-Type': 'application/json; charset=utf-8'
    }

    # call api and log status to console
    call = requests.post(url, json=query, headers=headers)
    print(call.status_code, call.reason)
    if call.status_code!=200:
        print(call.json())

    return call.json()


if __name__=="__main__":
    coords = [
        [49.41461,8.681495]
        , [49.41943,8.686507]
        ]
    
    range = [0.05]

    isos = search_isochrone(coords, range)

    print(isos)