from searchStays import search_all_stays
from searchDrivingDirections import search as searchDrivingDirections
import pandas as pd
import math

# search both driving directions and stays for a road trip. 

def _getSegmentInfo(addresses:list, stay_args:dict=None, max_driving_duration_per_day_hrs:float=7, rest_every_n_hrs:float=3, rest_duration_hrs:float=0.25) -> dict:
    """
    Searches for stays and recommends how to split up driving directions into multiple segments, if applicable.

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
    
    # get the duration of the entire trip from the api response
    # call directions API
    driving_directions = searchDrivingDirections(addresses)

    # add up the durations from each segment
    total_trip_duration=0
    for segment in driving_directions:
        total_trip_duration += float(segment["duration"])

    # convert total trip duration from seconds to hours
    total_trip_duration_hrs = total_trip_duration/(60**2)

    # get minimum number of segments for the trip
    min_segments_required = math.ceil(total_trip_duration_hrs / max_driving_duration_per_day_hrs)

    # total resting duration per segment
    if total_trip_duration_hrs<rest_every_n_hrs:
        total_resting_duration_hrs=0
    else:
        total_resting_duration_per_segment = math.floor(max_driving_duration_per_day_hrs / rest_every_n_hrs)*rest_duration_hrs
        total_resting_duration_hrs = total_resting_duration_per_segment*min_segments_required

    # get segment_driving_duration, equal to segment_max_driving_duration arg plus the total resting duration for the segment from step 2
    max_segment_duration = max_driving_duration_per_day_hrs + total_resting_duration_per_segment

    # store all info in a dict
    segment_info = {
        "total_trip_duration_hrs":total_trip_duration_hrs
        , "min_segments_required":min_segments_required
        , "total_resting_duration_hrs":total_resting_duration_hrs
        , "max_segment_duration":max_segment_duration
        }

    return segment_info

if __name__=="__main__":
    print(_getSegmentInfo(["innisfail alberta", "Winnipeg manitoba"]))