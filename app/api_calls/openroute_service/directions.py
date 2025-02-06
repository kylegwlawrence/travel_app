import requests
import os
import json

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

    # log to console if we get a non-200 response
    if call.status_code!=200:
        print(call.json())

    return call.json()

def get_driving_steps(response:dict) -> list:
    """
    Extract the driving steps and add their lat long coordinates from the driving directions API response

    Params:
    response (dict): driving directions from API response. See search_driving_directions function for more.

    Returns:
    list of dicts of driving steps
    """

    # extract segment data
    segments = response["features"][0]["properties"]["segments"]

    # extract list of geometry coords that define the route as a LineString
    geo_cords = response["features"][0]["geometry"]["coordinates"]

    # init counter to hold the segment number
    segment_number = 0

    # init list to hold dicts of step data
    steps_data = []

    # get the steps for each segment
    for segment in segments:
        segment_number+=1
        steps = segment["steps"]
        #print(f"""Number of steps in segment {segment_number}: {len(steps)}""")

        # init counter to hold the step number
        step_number = 0

        # get the lat and longs for each waypoint within the steps
        for step in steps:
            step_number+=1
            way_points = step["way_points"]

            # the way points are the indexes of the list of coordinates in the geometry dict from the geojson response
            first_way_point_coord = geo_cords[way_points[0]]
            last_way_point_coord = geo_cords[way_points[1]]

            # store data in a dict and append to a list
            step_dict_data = step

            step_dict_data["way_points"][0] = {step["way_points"][0]:first_way_point_coord}
            step_dict_data["way_points"][1] = {step["way_points"][1]:last_way_point_coord}

            step_dict_data["segment_number"] = segment_number
            step_dict_data["step_number"] = step_number
            
            steps_data.append(step_dict_data)

    return steps_data


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


if __name__=="__main__":
    dd = search_driving_directions()