from api_calls.openroute_service.directions import get_driving_directions, get_end_of_day_step, reached_end_first_segment, reached_end_trip, coordinates_from_waypoints
from api_calls.geocoder.search import geocode_address
from searchStays import search_all_stays, get_best_stay
from datetime import datetime, timedelta
from typing import List
import math

def get_route(start_address, finish_address, daily_driving_limit:float, trip_start_date:str) -> List[tuple]:
    """
    Get route for the road trip including stops at hotels

    Params:
    - start_address (str): free form address where the route starts
    - finish_address (str): free form address where the route ends
    - daily_driving_limit (float): max duration in hours to drive in one day
    - trip_start_date (str): MM-DD-YYYY

    Returns:
    - (list of tuples): coordinates
    """

    start_coordinate = geocode_address(start_address)
    finish_coordinate = geocode_address(finish_address)
    initial_driving_directions = get_driving_directions(start_coordinate, finish_coordinate)
    total_trip_duration = initial_driving_directions["features"][0]["properties"]["summary"]["duration"]
    number_driving_days_required = math.ceil(total_trip_duration / (daily_driving_limit*3600))
    copy_driving_directions = initial_driving_directions.copy()
    final_route_coordinates = [start_coordinate]
    
    if number_driving_days_required > 1:
        for day_index in range(1, number_driving_days_required+1):
            if day_index < number_driving_days_required:
                segment = copy_driving_directions["features"][0]["properties"]["segments"][0]
                last_step_current_day = get_end_of_day_step(segment, daily_driving_limit)
                geometry = copy_driving_directions["features"][0]["geometry"]
                last_coordinates_current_day = coordinates_from_waypoints(last_step_current_day, geometry)[1]
                checkIn = datetime.strptime(trip_start_date, '%mm-%dd-%yyyy')
                checkOut = checkIn + timedelta(days=1)
                accomodation_options = search_all_stays(last_coordinates_current_day, checkIn.strftime("%mm-%dd-%yyyy"), checkOut.strftime("%mm-%dd-%yyyy"), range=500, limit=2)
                best_accomodation = get_best_stay(accomodation_options, last_coordinates_current_day)
                best_accomodation_coordinates = (best_accomodation["lat"], best_accomodation["long"])
                final_route_coordinates.append(best_accomodation_coordinates)
                copy_driving_directions = get_driving_directions(best_accomodation_coordinates, finish_coordinate)
            elif day_index == number_driving_days_required:
                segment = copy_driving_directions["features"][0]["properties"]["segments"][0]
                last_step_current_day = get_end_of_day_step(segment, daily_driving_limit)
                geometry = copy_driving_directions["features"][0]["geometry"]
                last_coordinates_current_day = coordinates_from_waypoints(last_step_current_day, geometry)[1]
                final_route_coordinates.append(last_coordinates_current_day)
                break
        route = final_route_coordinates
    else:
        route = [start_coordinate, finish_coordinate]

    return route