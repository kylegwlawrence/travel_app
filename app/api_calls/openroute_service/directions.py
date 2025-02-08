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
    Extract the driving steps and obtain their lat long coordinates from the driving directions API response

    Params:
    response (dict): driving directions from API response. See search_driving_directions function for more.

    Returns:
    list of dicts of driving steps
    """

    # extract trip summary data
    trip_summary = response["features"][0]["properties"]["summary"]

    # extract segment data
    segments = response["features"][0]["properties"]["segments"]

    # extract list of geometry coords that define the route as a LineString
    geo_cords = response["features"][0]["geometry"]["coordinates"]

    # init counter to hold the segment number
    segment_number = 0

    # init list to hold dicts of step data
    driving_steps = []

    # init vars to hold the running total for the trip duraitona nd distance
    running_trip_duration_sec = 0
    running_trip_distance_m = 0

    # get the steps for each segment
    for segment in segments:

        # start on segment 1
        segment_number+=1

        # init counter to hold the step number
        step_number = 0

        # extract steps data only
        steps = segment["steps"]

        # extract segment summary data
        total_segment_duration_sec = segment["duration"]
        total_segment_distance_m = segment["distance"]

        # init vars to hold the segment running total of the duration and distance
        running_segment_duration_sec = 0
        running_segment_distance_m = 0

        # iterate over the steps within the segment
        for step in steps:
            step_number+=1

            # get the lat and longs for each waypoint within the steps
            way_points = step["way_points"]
            first_way_point_coord = geo_cords[way_points[0]]
            last_way_point_coord = geo_cords[way_points[1]]

            # take the original dict for each step and add the way points coordinates
            step_dict_data = step
            step_dict_data["way_points"][0] = {step["way_points"][0]:first_way_point_coord}
            step_dict_data["way_points"][1] = {step["way_points"][1]:last_way_point_coord}

            # add segment numbers and step numbers
            step_dict_data["segment_number"] = segment_number
            step_dict_data["step_number"] = step_number

            # add total segment duration and distance
            step_dict_data["segment_duration_sec"] = total_segment_duration_sec
            step_dict_data["segment_distance_m"] = total_segment_distance_m

            # add running total segment duration and distance for each step
            running_segment_duration_sec += step["duration"]
            running_segment_distance_m += step["distance"]
            step["running_segment_duration_sec"] = running_segment_duration_sec
            step["running_segment_distance_m"] = running_segment_distance_m

            # add total trip duration and distance
            step["trip_duration_sec"] = trip_summary["duration"]
            step["trip_distance_m"] = trip_summary["distance"]

            # add runnign total trip duration and distance for each step
            # if this is segment 1, take the same running total as the segment running total
            # if this is not the first segment, take the total(s) from the previous segments and add to it the runnig total for the current segment
            # how to store previous segments: get number of segments, use loop to iterate over segments while checking the segment_number every step. if the segment_number changes, then freeze previous segment running total and start a new one. store this in a dict
            running_trip_duration_sec += step["duration"]
            running_trip_distance_m += step["distance"]
            step["running_trip_duration_sec"] = running_trip_duration_sec
            step["running_trip_distance_m"] = running_trip_distance_m

            # store dict in a list
            driving_steps.append(step_dict_data)

    return driving_steps

def get_driving_days(driving_steps:list, max_drive_per_day_hrs:float) -> dict:
    """
    Determines how many days are required for the roadtrip based on the max hours per day the driver will be behind the wheel

    Params:
    driving_steps (list  of dicts): returned from get_driving_steps function
    max_drive_per_day_hrs (float): max length of time driver will be behind the wheel between sleeping

    Returns:
    dict of day endpoints with location data
    """

    # convert hours to seconds
    max_drive_per_day_sec = max_drive_per_day_hrs*60*60

    # find the steps which will define the end of a day

    # if the total segment duration is less than the daily driving time, then the end of the day is defined as the segment destination.

    # need to save last step's delta (to max driving time) and this step's delta in order to retireve last step's delta when the current step delta is out of the driving duration bound
    eod_found = False 
    for step in driving_steps:
        # special case for the first segment
        if step["segment_number"]==1:
            while eod_found==False:
        
                # define the end of day: get previous step by referencing step number
                if step["running_segment_duration_sec"] >= max_drive_per_day_sec:
                    eod_step_number = step["step_number"]-1

                    eod_step = [step for step in driving_steps if step["step_number"] == eod_step_number]

                    eod_found = True

                    print(f"""### Step number {step["step_number"]} is an EOD candidate ###\nRunning segment duration: {step["running_segment_duration_sec"]} sec\nMax driving per day:{max_drive_per_day_sec} sec""")

                    print(f"""### Next step number {step["step_number"]} is an EOD candidate ###\nRunning segment duration: {step["running_segment_duration_sec"]} sec\nMax driving per day:{max_drive_per_day_sec} sec""")
                # dont do anything (yet) if the step is before the end of the max driving duration
                else:
                    continue

                

        elif step["segment_number"]>1:
            print(f"""### Skipping segment {step["segment_number"]} ###""")
            break
                
           
    return eod_step

                

        # use while loop - while total running duration (for all segments) is less than total trip duration
            # iterate over the driving steps and get the running total for duration

                # find the first step that has running total duration > max driving hours per day

                # take the step from above and find the step before it

                # store day number with the step information

                # check total running duration against the while loop

            # now start iterating over the steps again starting from the day 1 endpoint and get running total duration
            
                # find the first step that has running total duration > max driving hours per day

                # take the step from above and find the step before it

                # store day number with the step information

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