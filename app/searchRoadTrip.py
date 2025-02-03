from searchStays import search_all_stays
from searchDrivingDirections import search as searchDrivingDirections
import pandas as pd
import math
from api_calls.driving_directions.app import search_driving_directions, parse_info

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
    
    important_info = parse_info(addresses, driving_directions)

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

if __name__=='__main__':
    addresses = ["1709 F Street Bellingham Washington", "820 15 ave sw calgary ab"]
    max_driving_duration_per_day_hrs=7.5
    rest_every_n_hrs=3
    rest_duration_hrs=0.5



    dd = searchDrivingDirections(addresses)

    segment_duration_info = _getSegmentDurationInfo(dd, max_driving_duration_per_day_hrs, rest_every_n_hrs, rest_duration_hrs )

    coords = _getStayCoordsPerSegment(dd, max_driving_duration_per_day_hrs, rest_every_n_hrs, rest_duration_hrs)

    print(coords)