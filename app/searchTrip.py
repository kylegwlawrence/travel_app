from searchStays import search_all_stays
from searchDrivingDirections import search as searchDrivingDirections
import pandas as pd
import math

# search both driving directions and stays for a road trip. 

def search(addresses:list, stay_args:dict=None, segment_max_duration:float=7, rest_every_n_hours:float=3):
    """
    Searches for stays and recommends how to split up driving directions into multiple segments, if applicable.
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