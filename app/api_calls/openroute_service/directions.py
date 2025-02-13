import requests
import os
import json

def reverse_coordinates(coordinates:list) -> list:
    """
    Operates on one set of coordinates stored as floats in a list
    The coordinates from opernrouteservice are formatted long, lat instead of conventional lat long. 
    Reverse them for easier debugging/interacting.

    Params:
    coordinates (list): list of coordinates to reverse

    Return:
    list of coordinates in reverse order
    """
    print("Running reverse_coordinates....")

    # check if all elements are of the same type
    b = len(set(type(x) for x in coordinates)) == 1

    if b:
        # remove the one-level nested list
        if type(coordinates[0]) is list:
            # enforce list length of 2 for coordinates
            if len(coordinates[0])!=2:
                raise ValueError(f"Need two coordinates, you passed:\n{coordinates[0]}")
            else:
                coordinates = coordinates[0]
        else:
            # enforce list length of 2 for coordinates
            if len(coordinates)!=2:
                raise ValueError(f"Need two coordinates, you passed:\n{coordinates}")
    else:
        raise TypeError("Elements in coordinates list are not of the same type")

    coordinates.reverse()

    return coordinates

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

    print(f"Running driving_directions for {coordinates}....")

    # format coordinates for the API call (long, lat instead of conventional lat, long)
    formatted_coordinates = []
    for c in coordinates:
        r = [c[1], c[0]]
        formatted_coordinates.append(r)

    # format as long, lat for the API
    body = {"coordinates":formatted_coordinates}

    headers = {
        'Accept': 'application/json, application/geo+json, application/gpx+xml, img/png; charset=utf-8',
        'Authorization': os.environ["OPENROUTE_KEY"],
        'Content-Type': 'application/json; charset=utf-8'
    }

    call = requests.post('https://api.openrouteservice.org/v2/directions/driving-car/geojson', json=body, headers=headers)

    if call.status_code!=200:
        print(call.json())

    return call.json()

def end_of_day_step(segment:dict, max_driving_hours_per_day:float) -> dict:
    """
    Operates on one segment of directions. 
    Determines which step in the directions is the last one before the maximum driving time has been reached.
    
    Params:
    segment (dict): information for a driving directions step
    max_driving_hours_per_day (float): length of time allowed to drive between sleep stops
    """

    print("Running end_of_day_step....")

    # init some counters
    step_number = 0
    time_elapsed_sec = 0

    # convert hours to seconds
    driving_limit_sec = max_driving_hours_per_day*60*60

    for step in segment["steps"]:
        step_number+=1
        time_elapsed_sec += step["duration"]
        if time_elapsed_sec > driving_limit_sec: # the steps are in chronological order hence why we can iterate over them sequentially to get the eod step
            # get the previous step
            s = segment["steps"][step_number-1]
            # get elapsed time for previous step
            s["elapsed_time_sec"] = time_elapsed_sec-step["duration"]
            # from the previous step, get driving duration to the location matching our max daily driving duration
            s["duration_until_limit_sec"] = driving_limit_sec - s["elapsed_time_sec"]

            # current step is end of segment
            print(f"""EOD is end of a segment""")

            break
        else:
            
            s = step

    return s

def coordinates_from_waypoints(step: dict, route_geometry: list) -> list:
    """
    Get the start and end coordinates for a single driving step

    Params:
    driving_step (dict): single step
    route_geometry (list): list of coordinates defining the LineString

    Returns:
    list of two coordinate lists that locate the start and end of the driving step formatted as lat, long
    """

    print("Running coordinates_from_waypoints....")

    # get coordinates, reindex to 0-based
    start_way_point = step["way_points"][0]-1
    end_way_point = step["way_points"][1]-1

    # use way point as index
    start_coords = route_geometry["coordinates"][start_way_point]
    end_coords = route_geometry["coordinates"][end_way_point]

    start_coords = reverse_coordinates(start_coords)
    end_coords = reverse_coordinates(end_coords)

    return [start_coords, end_coords]

def reached_end_trip(step:dict, directions:list) -> bool:
    """
    Determines if a driving step is the last one of the entire trip

    Params:

    Returns:

    """
    
    print("Running reached_end_trip....")

    geometry = directions["features"][0]["geometry"]
    final_step = directions["features"][0]["properties"]["segments"][-1]["steps"][-1]

    step_coords = coordinates_from_waypoints(step, geometry)
    final_step_coords = coordinates_from_waypoints(final_step, geometry)

    if step_coords == final_step_coords:
        end_of_trip_reached = True
    else: 
        end_of_trip_reached = False

    return end_of_trip_reached

def reached_end_first_segment(step:dict, directions:list):
    """
    Determines if a driving step is the last one of the FIRST segment of driving directions

    Params:

    Returns:

    """

    print("Running reached_end_first_segment....")

    geometry = directions["features"][0]["geometry"]
    final_step = directions["features"][0]["properties"]["segments"][0]["steps"][-1]

    step_coords = coordinates_from_waypoints(step, geometry)
    final_step_coords = coordinates_from_waypoints(final_step, geometry)

    if step_coords == final_step_coords:
        end_of_segment_reached = True
    else: 
        end_of_segment_reached = False

    return end_of_segment_reached

def full_directions(coordinates:list, max_driving_hours_per_day:float) -> list:
    """
    Generates a list of coordinates for all of the stopping locations including original destinations

    Params:
    coordinates (list): list of list of coordinates defining route destinations formatted as lat long
    max_driving_hours_per_day (float): max allowable daily driving time, in hours (decimals accepted)

    Returns:
    Updated coordinates for all stops in a list
    """

    print("Running full_directions....")

    initial_directions = driving_directions(coordinates)

    # need to keep inital directions throught the loop
    updated_direction_coords = coordinates.copy()

    # init some stuff
    updated_route = []
    counter = 0
    end_of_trip_reached = False
    
    # iterate over updated directions until the end of the trip has been reached
    while end_of_trip_reached == False:
        if counter == 0:
            #use initial directions only in the first loop
            directions = initial_directions
        else:
            # use updated directions for all subsequent loops
            directions = updated_directions.copy()
        counter+=1

        first_segment = directions["features"][0]["properties"]["segments"][0]
        
        # determine end of day stop for the first segment
        first_eod = end_of_day_step(first_segment, max_driving_hours_per_day)

        # get c
        first_eod_waypoint_end = first_eod["way_points"][1]-1
        first_eod_coords_end = directions["features"][0]["geometry"]["coordinates"][first_eod_waypoint_end]

        # reverse the coordinate order to conventional order
        first_eod_coords_reversed = reverse_coordinates([first_eod_coords_end])

        # determine if we have reached a destination (ie segment end) or the end of te trip
        end_of_trip_reached = reached_end_trip(first_eod, directions)
        end_of_first_segment_reached = reached_end_first_segment(first_eod, directions)

        if end_of_trip_reached == False and end_of_first_segment_reached == False:
            updated_route.append(first_eod_coords_reversed)
            # delete first starting point and replace with eod location
            del updated_direction_coords[0]
            updated_direction_coords = [first_eod_coords_end]+updated_direction_coords
            updated_directions = driving_directions(updated_direction_coords)
            
        elif end_of_trip_reached == False and end_of_first_segment_reached:
            # store the locations (coords) in a list
            updated_route.append(first_eod_coords_reversed)
            # delete first starting point so we can update directions starting at segment end
            del updated_direction_coords[0]
            updated_directions = driving_directions(updated_direction_coords)

        elif end_of_trip_reached:
            print("End of trip")

    return updated_route