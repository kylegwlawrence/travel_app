from app.api_calls.openroute_service.isochrone import get_isochrone, calculate_isochrone_box
from searchDrivingDirections import search as search_directions
from shapely import Point, Polygon 

def simple_demo() -> bool:
    """demo shapely lib - determine if a point is inside a polygon"""
    area = Polygon([(0, 0), (1, 0), (1, 1), (0, 1), (0, 0)])
    result = area.contains(Point(0.5, 2))
    return result

# purpose:
    # find an area on the map between today's last step and tomorrow's first step such that the driving duration for the day is between 6 to 7 hours (as an example)

# why not use priceline and airbnb range params?
    # the limits for these apis are low whereas openrouteservice (500 isochrones/day) and geoapify limits are high


def search(coordinates_a:tuple, coordinates_b:tuple, n_estimates:int=30):
    """
    Find the point within an geomteric polygon that is closest, by driving, to another point inside or outside of the polygon.
    """
    # determine if the coordinates are inside the polygon
    
    
    result=None

    return result

if __name__=="__main__":

    addresses = [
        "1709 F Street bellingham wa"
        , "125 N Samish Way, Bellingham, WA 98225"
        , "1009 Larrabee Ave, Bellingham, WA 98225"
        ]
    
    
    
    directions = search_directions(addresses)

    # get the coordinate for the last step from directions
        # find the last step by evaluating the running total of duration per day and get it's coordinates

    last_step_lat = 49.987 #eg
    last_step_lon = -110.65 #eg

    max_daily_hours = 7
    last_step_running_duration = 6.4

    # get isochrone for the last step equal to the size of the remaining drive time for the day
    search_radius = max_daily_hours-last_step_running_duration # hours
    isochrone = search_isochrone([[last_step_lat, last_step_lon]], [search_radius])

    # next step lat and long
    next_step_lat = 49.783
    next_step_lon = -110.641

    # find a box that fits the isochrone: furthest north, east, south, west based on isochrone extremes

    # for range of coordinates in the isochrone-box:
        # split lat range into n parts to get estimator lat coordinates
        # split lon range into n parts to get estimator lon coordinates

    # cross combine these coordinates into a matrix
    # use this matrix of coordinates for the search points
        # for each coordinate:
            # check if the coord is in the isochrone using shapely. 
                # if not, move on, 
                # if yes, 
                    # check driving duration to the next step (ie. from estimated stay location to the next step) for the next day
                    # store this data

    # select the coordinates with the shortest duration to the next day's first step









    # is_in_isochrone = isochrone.contains(seed_coordinate)
    

    # method:
        # take the coordinates for today's last step and tomorrow's first step
        
        # using the running daily driving duration up to and including the last step, get an isochrone with duration = daily max duration - last step running total  
            # this gives you an area around the last driving step that keeps your total driving time just under the maximum daily limit
        
        # now using the coordinates for the next day's first step, iterate over some coordinates in the isochrone to estimate which coordinate within the isochrone minimize the distance to the next day's first step
            # for each estimated coordinate, find the directions to the next day's first step
            # do this n times (at least 5) - or scale with the size of the isochrone!
            # choose the coordinates with the shortest drive time to the next days first step, and search there for stays. 

# using the isochrone returned from the api call, search within the polygon by using shapely's contains(polygon, point)