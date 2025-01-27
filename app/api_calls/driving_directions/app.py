# open route api: https://openrouteservice.org/dev/#/api-docs/introduction
# free and open source. limit of 2,000 driving direction api calls per day @ max 40 per minute
# points of interest api: limit 500 per day @ max 60 per minute
# isochrones (reachability within a radius): limit 500 per day @ max 20 per minute

import requests
import json

def search_driving_directions(coordinates:list) -> dict:
    """
    Pass in a list of a list of coordinates and return the directions as a geojson formatted dict.
    If only list of coordinates are passed - one start and one end - then one segment of directions is returned. If more than 2 sets of coordinates are provided then there are multiple segments of directions returned. 

    An example: coordinates=[[49.41461,8.681495], [49.41943,8.686507], [49.420318, 8.687872]]. This will give directions between the first two lists of coordinates as segment one and then directions between the last two coordinates as segment two. 

    Params:
    coordinates (list of lists of floats): a list of a list of cartesian coordinates that define start and end points for each segment. Must be format [latitude, longitude].

    Returns (str): dict of driving directions
    """

    # reverse the individual lists of coordinates for the api input. API takes longitude, latitude instead of standard latitude, longitude. 
    print(coordinates)
    reversed_coordinates=[]   
    for c in coordinates:
        r = c[::-1]
        reversed_coordinates.append(r)

    # pass in a list of a list of coordinates as floats with at least two sets of coordinates
    body = {"coordinates":reversed_coordinates}

    # read api key
    with open("api_calls/driving_directions/key.json", "r") as f:
        apiKey=json.load(f)

    # define headers for api request
    headers = {
        'Accept': 'application/json, application/geo+json, application/gpx+xml, img/png; charset=utf-8',
        'Authorization': apiKey["apiKey"],
        'Content-Type': 'application/json; charset=utf-8'
    }

    # call api and log status to console
    call = requests.post('https://api.openrouteservice.org/v2/directions/driving-car/geojson', json=body, headers=headers)
    print(call.status_code, call.reason)

    return call.json()

def parse_info(response:dict) -> list:
    """
    Takes the response from the driving directions api and parses out key information.

    Params:
    response (dict): the response dictionary from the api call

    Returns:
    list of dicts of key information for driving:
    - distance in metres
    - duration in seconds
    """
    key_info = []
    segment_number = 1
    for segment in response["features"][0]["properties"]["segments"]:
        distance = segment["distance"]
        duration = segment["duration"]
        d = {"segment_number":segment_number, "distance":distance, "duration":duration}
        key_info.append(d)
        segment_number+=1

    return key_info
    
if __name__=='__main__':
    # use output_directions.json to dev the parsing function
    with open("output_directions.json", "r") as f:
        response = json.load(f)

    key_info = parse_info(response)
    print(key_info)