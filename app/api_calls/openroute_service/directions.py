import requests
import os
import json

def driving_directions(coordinates:list) -> dict:
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

def end_of_day_step(segment:dict, max_driving_hours_per_day:float):
    """
    Operates on one segment of directions. 
    Determines which step in the directions is the last one before the maximum driving time has been reached.
    
    Params:
    segment (dict): information for a driving directions step
    max_driving_hours_per_day (float): length of time allowed to drive between sleep stops
    """
    step_number = 0
    time_elapsed_sec = 0
    driving_limit_sec = max_driving_hours_per_day*60*60

 
    # iterate over the steps
    for step in segment["steps"]:
        step_number+=1

        # add duration to elapsed time
        time_elapsed_sec+=step["duration"]

        # check if time elapsed has passed the daily limit
        if time_elapsed_sec>driving_limit_sec:

            # return the previous step
            previous_step = segment["steps"][step_number-1]
            previous_step["elapsed_time_sec"] = time_elapsed_sec-step["duration"]
            previous_step["duration_until_limit_sec"] = driving_limit_sec - previous_step["elapsed_time_sec"]
            
            break

    return previous_step

def full_directions(coordinates:list, max_drive_per_day_hrs:float) -> list:
    """
    Generates full directions to include sleep locations and rest stops.

    Params:
    driving_steps (list of dicts): returned from function get_driving_steps()

    Returns:
    updated directions in a list of dicts
    """

    # get initial driving directions
    initial_directions = driving_directions(coordinates)
    print(initial_directions)

    # extract steps from the directions dictionary
    initial_driving_steps = driving_directions(initial_directions)

    # init vars
    reached_end_trip = False
    sleep_stop = None
    update_directions = False

    for step in initial_driving_steps:

        while update_directions == False:

            # find the first step in the segment that passes the max driving duration per day
            if step["segment_number"]==1 and step["running_segment_duration_sec"]>max_drive_per_day_hrs*60*60:
                    
                # take the previous step
                previous_step_number = step["step_number"]-1

                # end of previous step is the sleeping location
                sleep_spot_coords = initial_driving_steps[previous_step_number-1]["way_points"][1].values()

                # assemble the list of updated coordinates so that the sleep spot replaces the starting point of the last day
                for coord in coordinates[1:]:
                    updated_coords.append(coord)

                update_directions = True 

            # if we don't finda step that is further than the max driving duration, then the sleep spot is the end of this segment
            elif step["segment_number"]==1 and step["number"]==initial_driving_steps[-1]["step_number"]:

                # now remove the first set of coordinates from original coordinates
                sleep_spot_coords = step["way_points"][1].values()


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
    dd = get_driving_days()