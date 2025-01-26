# open route api: https://openrouteservice.org/dev/#/api-docs/introduction
# free and open source. limit of 2,000 driving direction api calls per day @ max 40 per minute
# points of interest api: limit 500 per day @ max 60 per minute
# isochrones (reachability within a radius): limit 500 per day @ max 20 per minute

import requests
import json

def get_driving_directions(coordinates:list) -> str:
    """
    Pass in a list of a list of coordinates and write the response containing driving directions to disk.
    If only list of coordinates are passed - one start and one end - then one segment of directions is returned. If more than 2 sets of coordinates are provided then there are multiple segments of directions returned. 

    An example: coordinates=[[8.681495,49.41461],[8.686507,49.41943],[8.687872,49.420318]]. This will give directions between the first two lists of coordinates as segment one and then directions between the last two coordinates as segment two. 

    Params:
    coordinates (list of lists of floats): a list of a list of cartesian coordinates that define start and end points for each segment. Must be format [latitude, longitude].

    Returns (str): json file name the response is written to. 
    """

    # reverse the individual lists of coordinates for the api input. API takes longitude, latitude instead of standard latitude, longitude. 
    print(coordinates)
    reversed_coordinates=[]   
    for c in coordinates:
        r = c[::-1]
        reversed_coordinates.append(r)
    print(reversed_coordinates)

    # pass in a list of a list of coordinates as floats with at least two sets of coordinates
    body = {"coordinates":reversed_coordinates}

    # read api key
    with open("key.json", "r") as f:
        apiKey=json.load(f)

    # define headers for api request
    headers = {
        'Accept': 'application/json, application/geo+json, application/gpx+xml, img/png; charset=utf-8',
        'Authorization': apiKey["apiKey"],
        'Content-Type': 'application/json; charset=utf-8'
    }

    # call api and log status to console
    call = requests.post('https://api.openrouteservice.org/v2/directions/driving-car', json=body, headers=headers)
    print(call.status_code, call.reason)

    # write response to json
    file_name="output.json"
    with open(file_name, "w") as outfile:
        json.dump(call.json(), outfile)
    
    # return the name of the file json is written to
    return file_name

if __name__=='__main__':
    # some coordinates in Germany
    # coordinates=[[49.41461, 8.681495],[49.41943, 8.686507],[49.420318, 8.687872]]

    # some road trip coordinates from Bellingham to HB with a stop in Eugene
    bham = [48.757713, -122.483891]
    eugene = [44.048323, -123.089221]
    hb = [33.720074, -118.012771]

    json_file_name=get_driving_directions([bham, eugene, hb])
    print(json_file_name)