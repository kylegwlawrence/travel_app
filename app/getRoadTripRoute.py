from api_calls.openroute_service.directions import get_driving_directions, get_end_of_day_step, reached_end_first_segment, reached_end_trip, coordinates_from_waypoints
from api_calls.geocoder.search import geocode_address
from api_calls.airbnb.search import main as search_airbnb
from api_calls.priceline.search import main as search_priceline
import math
from typing import List

def get_route(start_address, finish_address, daily_driving_limit:float, trip_start_date:str) -> List[tuple]:
    """
    Get route for the road trip including stops at hotels

    Params:
    - addresses (list of strings)
    - daily_driving_limit (float): max duration in hours to drive in one day
    - trip_start_date (str): MM-DD-YYYY

    Returns:
    - (list of tuples): coordinates
    """

    start = geocode_address(start_address)
    finish = geocode_address(finish_address)
    initial_driving_directions = get_driving_directions(start, finish)
    total_trip_duration = initial_driving_directions["features"][0]["properties"]["summary"]["duration"]
    number_driving_days_required = math.ceil(total_trip_duration / (daily_driving_limit*3600))
    
    if number_driving_days_required > 1:
        day_counter = 1
        for day_index in range(1, number_driving_days_required+1):
            if day_counter < number_driving_days_required:
                directions = get_driving_directions(start, daily_driving_limit) 
                on "updated coordiantes", where stop, find hotel, append day_index complete coordinates, redefine updated iteration coordiantes with day_index
                day_counter += 1
            elif day_counter == number_driving_days_required:
                directions on "updated coordiantes", append complete coordinates,
        route = complete_coordinates
    else:
        route = geocoded_addresses

    return route