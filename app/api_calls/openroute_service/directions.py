import requests
import os
import json
from typing import List

def get_driving_directions(start: tuple, finish: tuple) -> dict:
    """
    Get driving directions between two coordinates.

    Params:
    - start (tuple): lat long coordinate for starting location
    - finish (tuple): lat long coordinate for finishing location

    Returns: 
    - (dict): driving directions
    """

    ENDPOINT = "https://api.openrouteservice.org/v2/directions/driving-car/geojson"
    
    with open("api_calls/openroute_service/api_params.json", "r") as f:
        headers = json.load(f)
        
    headers["Authorization"] = os.environ["OPENROUTE_KEY"]
    coordinates = [[start[1], start[0]], [finish[1], finish[0]]]
    print(f"Coordinates reversed: {coordinates}")
    response = requests.post(ENDPOINT, json={"coordinates":coordinates}, headers=headers)

    if response.status_code!=200:
        raise Exception(f"Error getting driving directions for {coordinates}:\n{response.status_code}")

    return response.json()

def get_end_of_day_step(segment:dict, max_driving_hours_per_day:float) -> dict:
    """
    Operates on one segment of directions. 
    Determines which step in the directions is the last one before the maximum driving time has been reached.

    Params:
    - segment (dict): information for a driving directions step
    - max_driving_hours_per_day (float): length of time allowed to drive between sleep stops

    Returns:
    - (dict): the last step of the day, and associated information, for a given segment. If the segment duration is less than the daily driving limit then returns the trip's finish coordinate
    """
    # init some counters
    step_number = 0
    time_elapsed_sec = 0

    # convert hours to seconds
    driving_limit_sec = max_driving_hours_per_day*60*60

    # the steps are in chronological order hence why we can iterate over them sequentially to get the eod step
    for step in segment["steps"]:

        step_number+=1
        time_elapsed_sec += step["duration"]

        # if we have just passed the driving limit with this step, use the previous step as the end of day step
        if time_elapsed_sec > driving_limit_sec: 

            # get the previous step
            prev_step = segment["steps"][step_number-1]
            prev_step["elapsed_time_sec"] = time_elapsed_sec-step["duration"]

            # driving duration remaining between the previous step and the daily limit
            prev_step["duration_until_daily_limit_sec"] = driving_limit_sec - prev_step["elapsed_time_sec"]

            s = prev_step

            break

        # if we are not yet beyond our driving limit in this segment, but we have reached the last step in the segment, then the current step is the end of day step
        else:
            s = step

    return s

def get_coordinates_from_waypoints(step: dict, route_geometry: list) -> List[tuple]:
    """
    Get the start and end coordinates for a single driving step

    Params:
    - driving_step (dict): single step
    - route_geometry (list): list of coordinates defining the LineString

    Returns:
    - (list of tuples): two coordinates that locate the start and end of the driving step formatted as long, lat
    """

    start_way_point = step["way_points"][0]-1
    end_way_point = step["way_points"][1]-1

    route_coordinates = route_geometry["coordinates"]

    start_coords = (route_coordinates[start_way_point][1], route_coordinates[start_way_point][0])
    end_coords = (route_coordinates[end_way_point][1], route_coordinates[end_way_point][0])

    return [start_coords, end_coords]

def reached_end_trip(step:dict, directions:list, final_step: dict) -> bool:
    """
    Determines if a driving step is the last one of the entire trip
    
    Params:
    - step (dict): step to evaluate
    - directions (list): from the current segment being iterated on
    - final_step (dict): the dictionary from driving directions of the last step to reach the final destination

    Returns:
    - (bool)
    """

    geometry = directions["features"][0]["geometry"]
    final_step = directions["features"][0]["properties"]["segments"][-1]["steps"][-1]

    step_coords = get_coordinates_from_waypoints(step, geometry)
    final_step_coords = get_coordinates_from_waypoints(final_step, geometry)

    if step_coords == final_step_coords:
        end_of_trip_reached = True
    else: 
        end_of_trip_reached = False

    return end_of_trip_reached

def reached_end_first_segment(step:dict, directions:list):
    """
    Determines if a driving step is the last one of the FIRST segment of driving directions

    Params:
    - step (dict): step to evaluate
    - directions (list): from the current segment being iterated on

    Returns:
    - (bool)
    """

    geometry = directions["features"][0]["geometry"]
    final_step = directions["features"][0]["properties"]["segments"][0]["steps"][-1]

    step_coords = get_coordinates_from_waypoints(step, geometry)
    final_step_coords = get_coordinates_from_waypoints(final_step, geometry)

    if step_coords == final_step_coords:
        end_of_segment_reached = True
    else: 
        end_of_segment_reached = False

    return end_of_segment_reached

def _defunct_full_directions(coordinates:list, max_driving_hours_per_day:float) -> list:
    """
    Generates a list of coordinates for all of the stopping locations including original destinations

    Params:
    - coordinates (list): list of list of coordinates defining route destinations formatted as lat long
    - max_driving_hours_per_day (float): max allowable daily driving time, in hours (decimals accepted)

    Returns:
    - (list): updated coordinates for all stops in a list
    """

    print("Running full_directions....")

    initial_directions = get_driving_directions(coordinates)

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
        first_eod = get_end_of_day_step(first_segment, max_driving_hours_per_day)

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
            updated_directions = get_driving_directions(updated_direction_coords)
            
        elif end_of_trip_reached == False and end_of_first_segment_reached:
            # store the locations (coords) in a list
            updated_route.append(first_eod_coords_reversed)
            # delete first starting point so we can update directions starting at segment end
            del updated_direction_coords[0]
            updated_directions = get_driving_directions(updated_direction_coords)

        elif end_of_trip_reached:
            print("End of trip")

    return updated_route