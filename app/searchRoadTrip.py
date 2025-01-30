from searchStays import search_all_stays
from searchDrivingDirections import search as searchDrivingDirections
import pandas as pd
import math

# search both driving directions and stays for a road trip. 

def search(addresses:list, stay_args:dict=None, max_driving_duration_per_day_hrs:float=7, rest_every_n_hrs:float=3, rest_duration_hrs:float=0.25) -> dict:
    """
    Searches for stays and recommends how to split up driving directions into multiple segments, if applicable.

    Definitions:
        - segment = one day of driving between two points
        - segment-part = portion of a segment of driving that is inbetween rest stops or is inbetween the start of the segment and a rest stop or a rest stop and the end of the segment

    To determine how many stays are required for the road trip:
        Step 1: get the duration of the entire trip from the api response
        Step 2: get minimum number of segments for the trip by dividing the total trip duration by the max_driving_duration_per_day_hrs

    To determine total time spent travelling between two destinations:
        Step 1: get total resting duration per segment, equal to the max_driving_duration_per_day_hrs divided by rest_every_n_hrs, rounded down, times resting_duration_hrs
            - the first divisor term is rounded down since there will be one less rest stop that there are number of segment-parts per day
        Step 2: get segment_driving_duration, equal to segment_max_driving_duration arg plus the total resting duration for the segment from step 2

    Params:
        addresses (list): a list of addresses defining the targetted start, mid, and endpoint destinations for the road trip. Must have at least 2 addresses.
        stay_args (dict): dictionary of arguments to pass into the searchStays function. See searchStays function more details. 
        max_driving_duration_per_day (float): the longest amount of time, in hours, to spend per day ACTIVELY driving. This does not include rest stops. This is only for time spent behind the wheel driving. 
        rest_every_n_hrs (float): how often, in hours, to stop for a rest
        rest_duration_hrs (float): how long, in hours, to rest

    Returns:
        A dictionary of recommended driving directions and stays.
    """
    
    # determine how many segments are required for the trip factoring in resting periods
        # 1. determine the duration of the entire trip
    driving_directions = searchDrivingDirections(addresses)
    total_trip_duration=0
    for segment in driving_directions:
        total_trip_duration += float(segment["duration"])

        # 2. divide the total trip duration by the max segment duration (add resting every n hours) to get the min number of segments required for the trip

    n_segments = max(0, (total_trip_duration / ((segment_max_duration*60*60)-(60*60)))) # arbitrarily adding 1 hour of resting per segment as seconds

    n_segments_rounded = math.ceil(n_segments)

    return n_segments, n_segments_rounded

    # find the latitudes and longitudes (ie a polygon) of the area at the end of each segment
        # 1. search for driving directions to the end of the first segment that meets the timing criteria
            # to do this, either find an api that can provide this or write some code to search over an estimated range of lats/longs based on an initial educated guess (seed)

    # search for stays within these coordinates (polygons)

    # filter down to a few reccommendations using some criteria
        # star ratings, guest ratings, proximity, price, pets allowed, parking, bed size, n beds


    #stays = search_all_stays(**stay_args)

if __name__=="__main__":
    print(search(["paris france", "dubrovnik"]))