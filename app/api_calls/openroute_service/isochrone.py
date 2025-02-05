import json
import requests
import os

def get_isochrone(coordinates:list, driving_times:list) -> dict:
    """
    Pass in one or multiple sets of coordinates to get an area that is accessible within a given driving time.

    Params:
    coordinates (list of lists of floats): list of a lists of coordinates (lat long)
    driving_time (list of floats): length of driving times in hours to define the boundaries of the isochrone. Pass in a list of multiple values to get multiple isochrones per location.

    Returns:
    - dict of isochrone geometry objects
    """

    # reverse the individual lists of coordinates for the input. openrouteservice uses longitude, latitude instead of standard latitude, longitude. 
    reversed_coordinates=[]   
    for c in coordinates:
        r = c[::-1]
        reversed_coordinates.append(r)

    # convert driving times to seconds
    driving_times_seconds = [hrs*60*60 for hrs in driving_times]

    # endpoint
    url = "https://api.openrouteservice.org/v2/isochrones/driving-car"
    
    # define our  ask
    query = {
        "locations":reversed_coordinates, 
        "range":driving_times_seconds
        }
    headers = {
        'Accept': 'application/json, application/geo+json, application/gpx+xml, img/png; charset=utf-8',
        'Authorization': os.environ["OPENROUTE_KEY"],
        'Content-Type': 'application/json; charset=utf-8'
    }

    # call api
    call = requests.post(url, json=query, headers=headers)

    # log if response is not 200
    if call.status_code!=200:
        print(call.status_code, call.reason)
        print(call.json())

    return call.json()

def calculate_isochrone_box(isochrone_dict:dict) -> dict:
    """
    Create a regular rectangle around the isochrone that fits all points just within it by using the max value for each of the four directions. Use this to create a matrix of coords to search over systematically.

    Params:
    isochrone (dict): the isochrone from the openroute service API

    Returns:
    a dict of tuples (lat, lon) that define the vertices of the rectangle
    """
   
    # access the coords within the isochrone dict
    isochrone_coords = isochrone_dict["features"][0]["geometry"]["coordinates"][0]

    # init vars
    highest_lat = None
    highest_lon = None
    lowest_lat = None
    lowest_lon = None

    # iterate over the coords defining the isochrone polygon:
    for coord in isochrone_coords:

        # remember openroute service formats their coordinates unconventionally as long, lat
        lat = coord[1]
        lon = coord[0]

        # most northern point (highest lat)
        if highest_lat == None or highest_lat < lat:
            highest_lat = lat

        # most southern point (lowest lat)
        if lowest_lat== None or lowest_lat > lat:
            lowest_lat = lat

        # most eastern point (highest lon)
        if highest_lon == None or highest_lon < lon:
            highest_lon = lon

        # most western point (lowest lon)
        if lowest_lon == None or lowest_lon > lon:
            lowest_lon = lon

    # create vertices coordinates
    vertices = {
        "north-east": (highest_lat, highest_lon),
        "north-west": (highest_lat, lowest_lon),
        "south-east": (lowest_lat, highest_lon),
        "south-west": (lowest_lat, lowest_lon)
        }

    return vertices


if __name__=="__main__":
    coords = [
        [49.41461,8.681495]
        ]
    
    range = [0.05]

    isos = get_isochrone(coords, range)

    vertices = calculate_isochrone_box(isos)

    print(vertices)

    #with open('data.json', 'w') as f:
    #    json.dump(isos, f)