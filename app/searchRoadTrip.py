from api_calls.openroute_service.directions import get_driving_directions, get_end_of_day_step, reached_end_first_segment, reached_end_trip, coordinates_from_waypoints
from api_calls.geocoder.search import geocode_address
from searchStays import get_best_stay, search_all_stays
import pandas as pd
import math
from datetime import datetime, timedelta

def _getSegmentDurationInfo(driving_directions:list, max_driving_duration_per_day_hrs:float=7, rest_every_n_hrs:float=3, rest_duration_hrs:float=0.33) -> dict:
    """
    Searches for driving directions and determines how many stays are required based on some criteria defined below. 

    Definitions:
        - segment = one day of driving between two points
        - segment-part = portion of a segment of driving that is inbetween rest stops or is inbetween the start of the segment and a rest stop or a rest stop and the end of the segment

    To determine how many stays are required for the road trip:
        Step 1: get the duration of the entire trip from the api response
        Step 2: get minimum number of segments for the trip by dividing the total trip duration by the max_driving_duration_per_day_hrs and round up to the nearest whole number

    To determine total time spent travelling between two destinations:
        Step 1: get total resting duration per segment, equal to the max_driving_duration_per_day_hrs divided by rest_every_n_hrs, rounded down, times resting_duration_hrs
            - the first divisor term is rounded down since there will be one less rest stop that there are number of segment-parts per day
        Step 2: get segment_driving_duration, equal to segment_max_driving_duration arg plus the total resting duration for the segment from step 1 above

    Params:
        addresses (list): a list of addresses defining the targetted start, mid, and endpoint destinations for the road trip. Must have at least 2 addresses.
        stay_args (dict): dictionary of arguments to pass into the searchStays function. See searchStays function more details. 
        max_driving_duration_per_day (float): the longest amount of time, in hours, to spend per day ACTIVELY driving. This does not include rest stops. This is only for time spent behind the wheel driving. 
        rest_every_n_hrs (float): how often, in hours, to stop for a rest
        rest_duration_hrs (float): how long, in hours, to rest

    Returns:
        A dictionary of driving segment information.
    """
    
    important_info = None

    # get the duration of the entire trip from the api response

    # add up the durations from each segment
    total_trip_duration=0
    for segment in important_info:
        total_trip_duration += float(segment["duration"])

    # convert total trip duration from seconds to hours
    total_trip_duration_hrs = total_trip_duration/(60**2)

    # get minimum number of segments for the trip
    min_segments_required = math.ceil(total_trip_duration_hrs / max_driving_duration_per_day_hrs)

    # total resting duration per segment
    if total_trip_duration_hrs<rest_every_n_hrs:
        total_resting_duration_hrs=0
    else:
        total_resting_duration_per_segment_hrs = math.floor(max_driving_duration_per_day_hrs / rest_every_n_hrs)*rest_duration_hrs
        total_resting_duration_hrs = total_resting_duration_per_segment_hrs*min_segments_required

    # get segment_driving_duration, equal to segment_max_driving_duration arg plus the total resting duration for the segment from step 2
    max_segment_duration_hrs = max_driving_duration_per_day_hrs + total_resting_duration_hrs

    # store all info in a dict
    segment_duration_info = {
        "total_trip_duration_hrs":total_trip_duration_hrs
        , "min_segments_required":min_segments_required
        , "total_resting_duration_hrs":total_resting_duration_hrs
        , "max_segment_duration_hrs":max_segment_duration_hrs
        }

    return segment_duration_info

def _getStayCoordsPerSegment(driving_directions, max_driving_duration_per_day_hrs:float=7, rest_every_n_hrs:float=3, rest_duration_hrs:float=0.33):
    """
    This should probably be in the function above since it is returning coorindates for locations to search for stays.

    Takes in the driving directions from searchDrivingDirections and from _getSegmentInfo and returns the recommended lat and longs to stay at for the end of each segment, excluding the last segment.

    This output is used to search for stays in each location. 
    """

    # grab important segment info from driving directions
    segment_duration_info = _getSegmentDurationInfo(driving_directions, max_driving_duration_per_day_hrs, rest_every_n_hrs, rest_duration_hrs)

    # find the step that is at the end of a segment
    running_total_duration_sec=0
    running_total_distance_m=0
    step_number=0
    step_info_list=[] # append dicts for each step to a list

    # iterate over segments
    for segs in driving_directions["features"][0]["properties"]["segments"]:
        print(f"Number segments: {len(segs)}")
        print(f"""Number steps: {len(segs["steps"])}""")

        # get distance and duration of each step
        for i in segs["steps"]:
            step_number+=1
            print(f"""Step number: {step_number} / {round(i["distance"]/(1000),2)}km / {round(i["duration"]/(60*60),2)}hrs""")

            # add this step's duration and distance to the total duration and distance
            running_total_duration_sec+=i["duration"]
            running_total_distance_m+=i["distance"]

            # init dict to hold step info
            step_info_dict = {
                "step_number":step_number
                , "duration_sec":i["duration"]
                , "distance_m":i["distance"]
                , "running_total_duration_sec":running_total_duration_sec
                , "running_total_distance_m":running_total_distance_m
                }

            # add the end of day flag to true if the step is the last one of the day, otherwise false and break the loop
            if (running_total_duration_sec + i["duration"]) > (max_driving_duration_per_day_hrs*60*60):
                step_info_dict["end_of_day_flag"] = True
            else:
                step_info_dict["end_of_day_flag"] = False
            
            step_info_list.append(step_info_dict)

    return step_info_list

    # use driving directions api to find the best location to end the segment based on allowed total drive time per segment. 
    max_drive_time_sec = max_driving_duration_per_day_hrs*60*60


        # need to estimate (seed) for the first guess to start the iteration to find best location to stop
            # the seed should be pulled from the driving direction steps - these have step by step instructions including the lat longs for each step
            # run a sum across the duration for all the steps sequentially until we find a location that is just under the max driving duration per segment.
            # if the stay location is inbetween two steps that are quite distant from eachother, then need to estimate between those two bounds
                # somehow we need to use the road number/exit number/street name information between steps to find acceptable segment endpoints

def get_roadtrip(addresses:list, start_date:str, max_driving_hours_per_day:float, stay_source='csv') -> list:
    """
    Generates a list of coordinates for all of the stopping locations including original destination and overnight stays

    Params:
    - addresses (list): a list of 2 free-form addresses, one the start and one the end of the roadtrip.
    - max_driving_hours_per_day (float): max allowable daily driving time, in hours (decimals accepted)

    Returns:
    - (list): updated coordinates for all stops
    """

    geocoded_addresses = []
    for address in addresses:
        lat, long = geocode_address(address)
        geocoded_addresses.append([long, lat])

    directions = get_driving_directions(geocoded_addresses)
    final_step = directions["features"][0]["properties"]["segments"][0]["steps"][-1]
    
    # use to update and rerun driving directions each loop
    updated_coords_for_next_loop = geocoded_addresses.copy()

    # store generated route
    complete_route_coords = [geocoded_addresses[0]]

    num_days_to_complete_trip = math.ceil(max_driving_hours_per_day / directions["features"][0]["properties"]["summary"]["duration"])

    is_end_trip = False
    while not is_end_trip:

        # find the location of the last driving step for the day
        segment = directions["features"][0]["properties"]["segments"][0]
        end_of_day_step = get_end_of_day_step(segment, max_driving_hours_per_day)
        end_of_day_coords = coordinates_from_waypoints(end_of_day_step, directions["features"][0]["geometry"])[1]
        print(f"Location at end of first day: {end_of_day_coords}")

        # if we have reached the end of the trip, then we have our full directions now
        is_end_trip = reached_end_trip(end_of_day_step, directions, final_step)
        if is_end_trip:
            # add the last coordinate to the full coordinates list 
            complete_route_coords.append(end_of_day_coords)
            print(f"\nTrip takes less than one full day of driving.\nUse initial directions as full directions.\nFull directions complete ending at {end_of_day_coords}")

        # if we haven't reached the end of a trip or a segment, find accomodations
        else:
            if stay_source == 'csv':
                df = pd.read_csv("stays.csv")
            else:
                checkIn = start_date
                checkOut = datetime.strptime(start_date, '%mm-%dd-%yyyy') + timedelta(days=1)
                df = search_all_stays(end_of_day_coords, checkIn, checkOut)
                # search for the closest stay

            best_stay = get_best_stay(df, (end_of_day_coords[1], end_of_day_coords[0]))
            print(f"""Best stay: {best_stay}""")
            best_stay_coords = [best_stay["long"], best_stay["lat"]]

            print(f"Reached end of day at {best_stay_coords} with a remainder of the segment to complete the next day.")
            complete_route_coords.append(best_stay_coords)

            # change the start point to the stay location and update driving directions
            print(f"""### Update coords: {updated_coords_for_next_loop} ###\n""")
            updated_coords_for_next_loop = updated_coords_for_next_loop[1:]
            print(f"""### Update coords: {updated_coords_for_next_loop} ###\n""")
            updated_coords_for_next_loop.insert(0, best_stay_coords)
            print(f"""### Update coords: {updated_coords_for_next_loop} ###\n""")

            directions = get_driving_directions(updated_coords_for_next_loop)

    return complete_route_coords

if __name__=="__main__":
    start_date = "04-10-2025" #MM-DD-YYYY
    addresses = ["1709 F Street bellingham wa", "820 15 ave sw calgary ab"]
    max_driving_hours_per_day = 7

    d = get_roadtrip(addresses, start_date, max_driving_hours_per_day)

    print(d)