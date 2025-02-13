import requests
import os
from shapely.geometry import Polygon, Point
#import pointpats 

def request_isochrone(coordinates:tuple, driving_times:list) -> dict:
    """
    Pass in one set of coordinates to get an area that is accessible within a given driving time.

    Params:
    coordinates (tuple): tuple of(long lat)
    driving_time (float): length of driving time in hours to define the boundaries of the isochrone.

    Returns:
    - dict of isochrone geometry objects
    """

    driving_times_seconds = [hrs*60*60 for hrs in driving_times]
    url = "https://api.openrouteservice.org/v2/isochrones/driving-car"
    query = {
        "locations":[list(coordinates)], 
        "range":driving_times_seconds
        }
    headers = {
        'Accept': 'application/json, application/geo+json, application/gpx+xml, img/png; charset=utf-8',
        'Authorization': os.environ["OPENROUTE_KEY"],
        'Content-Type': 'application/json; charset=utf-8'
    }
    call = requests.post(url, json=query, headers=headers)
    
    if call.status_code!=200:
        print(call.json())
        raise Exception
    else:
        print(call.status_code, call.reason)

    return call.json()

def is_in_isochrone(coordinates: tuple, isochrone: dict) -> bool:
    """
    Determines is one set of coordinates is within an isochrone

    Params:
    coordinates (tuple): tuple of (long, lat)
    isochrone (dict): dict object returned from isochrone api call

    Returns:
    boolean
    """

    isochrone_geometry = isochrone["features"][0]["geometry"]["coordinates"][0]
    polygon = Polygon(isochrone_geometry)

    a = polygon.contains(Point(coordinates))

    return a

if __name__=="__main__":
    coords = (8.681495, 49.41461)
    range = [0.1]
    q = (8.6814939, 49.41458)

    isos = request_isochrone(coords, range)
    in_iso = is_in_isochrone(q, isos)

    print(in_iso)