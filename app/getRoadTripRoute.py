from api_calls.openroute_service.directions import get_driving_directions, get_end_of_day_step, get_coordinates_from_waypoints
from api_calls.geocoder.search import get_geocoded_address
from searchStays import search_all_stays, get_best_stay
from datetime import datetime, timedelta
from typing import List
import math

def get_route(start_address:str, finish_address:str, daily_driving_limit:float, trip_start_date:str) -> List[tuple]:
    """
    Get route for the road trip including stops at hotels

    Params:
    - start_address (str): free form address where the route starts YYYY-MM-DD
    - finish_address (str): free form address where the route ends YYYY-MM-DD
    - daily_driving_limit (float): max duration in hours to drive in one day
    - trip_start_date (str): MM-DD-YYYY

    Returns:
    - (list of tuples): coordinates
    """
    date_format = "%Y-%m-%d"

    start_coordinate = get_geocoded_address(start_address)
    finish_coordinate = get_geocoded_address(finish_address)
    initial_driving_directions = get_driving_directions(start_coordinate, finish_coordinate)
    total_trip_duration = initial_driving_directions["features"][0]["properties"]["summary"]["duration"]
    number_driving_days_required = math.ceil(total_trip_duration / (daily_driving_limit*3600))
    copy_driving_directions = initial_driving_directions.copy()
    final_route_coordinates = [start_coordinate]
    
    range_of_days = range(1, number_driving_days_required+1)

    if number_driving_days_required > 1:
        for day_index in range_of_days:
            if day_index < number_driving_days_required:
                segment = copy_driving_directions["features"][0]["properties"]["segments"][0]
                last_step_current_day = get_end_of_day_step(segment, daily_driving_limit)
                geometry = copy_driving_directions["features"][0]["geometry"]
                last_coordinates_current_day = get_coordinates_from_waypoints(last_step_current_day, geometry)[1]
                checkIn = datetime.strptime(trip_start_date, date_format)
                checkOut = checkIn + timedelta(days=1)
                accomodation_options = search_all_stays(last_coordinates_current_day, checkIn.strftime(date_format), checkOut.strftime(date_format), range=2000, limit=2)
                best_accomodation = get_best_stay(accomodation_options, last_coordinates_current_day)
                best_accomodation_coordinates = (best_accomodation["lat"], best_accomodation["long"])
                final_route_coordinates.append(best_accomodation_coordinates)
                copy_driving_directions = get_driving_directions(best_accomodation_coordinates, finish_coordinate)
            elif day_index == number_driving_days_required:
                final_route_coordinates.append(finish_coordinate)
                break
        route = final_route_coordinates
    else:
        route = [start_coordinate, finish_coordinate]

    return route

if __name__=="__main__":
    args = {
        "start_address":"1709 F Street Bellingham Washington",
        "finish_address":"820 15 Ave SW Calgary Alberta",
        "daily_driving_limit":7,
        "trip_start_date":"2025-03-25"
        }
    
    route = get_route(**args)

    print(route)