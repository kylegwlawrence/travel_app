import json
import requests
import os
from shapely.geometry import Polygon
import pointpats 

def request_isochrone(coordinates:list, driving_times:list) -> dict:
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

def generate_coords_in_isochrone(isochrone:dict, n:int=30) -> list:
    """
    Creates a list of n random coordinates that are contained within the isochrone

    Params:
    isochrone (dict): dict object returned from isochrone api call
    n (int): number of coordinates to generate. Defaults to 30.

    Returns:
    list of coordinate tuples
    """

    # coordinates of polygon edges
    coords = isochrone["features"][0]["geometry"]["coordinates"][0]
    polygon = Polygon(coords)

    # generates n random coords inside polygon
    random_coords = pointpats.random.poisson(polygon, size=n)

    return random_coords

if __name__=="__main__":
    coords = [[49.41461,8.681495]]
    range = [0.5]

    isos = request_isochrone(coords, range)
    random_coords = generate_coords_in_isochrone(isos)

    print(random_coords)