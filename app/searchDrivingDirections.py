from api_calls.geocoder.search import geocode_address


from api_calls.openroute_service.directions import reached_end_first_segment, reached_end_trip, coordinates_from_waypoints, get_end_of_day_step, driving_directions, full_directions, reverse_coordinates
import json

def search(addresses:list) -> list:
    """
    Takes in a comma-separated list of addresses and provides driving directions between the addresses. The addresses must be in order.
    
    Params:
    addresses (list): a list, of at least length 2, of the addresses to retrieve driving directions between. If there are more than 2 addresses, then driving directions are created sequentially between the addresses. 

    Returns: 
    - list of dicts containing detailed directions
    """

    # enforce list length >1
    if len(addresses)<2:
        raise TypeError("list of addresses must have at least 2 addresses")

    # geocode the addresses and store in list
    geocoded_addresses = []
    for address in addresses:
        lat, long = geocode_address(address)
        geocoded_addresses.append([long, lat])

    # search for driving directions
    d = driving_directions(geocoded_addresses)
    #driving_directions = full_directions(geocoded_addresses)

    return d


def get_full_route_coordinates(addresses:list, max_driving_hours_per_day:float) -> list:
    """
    Generates a list of coordinates for all of the stopping locations including original destinations

    Params:
    coordinates (list): list of list of coordinates defining route destinations formatted as lat long
    max_driving_hours_per_day (float): max allowable daily driving time, in hours (decimals accepted)

    Returns:
    Updated coordinates for all stops in a list
    """

    # geocode addresses
    geocoded_addresses = []
    for address in addresses:
        lat, long = geocode_address(address)
        # format long, lat for API
        geocoded_addresses.append([long, lat])

    # test geocoding result
    print(f"\nAddresses {addresses} geocoded: {geocoded_addresses}")

    # use coordinates to get driving directions from the openrouteservice API
    initial_directions = driving_directions(geocoded_addresses)

    ##########################################
    ### OPERATING ON AN INDIVIDUAL SEGMENT ###
    ##########################################

    directions = initial_directions.copy()
    complete_route_coords = []

    for segment in directions["features"][0]["properties"]["segments"]:

        # get the first segment
        first_segment = segment[0]
        print(f"\nFirst segment: {first_segment}\n")

        # get the end of the first day for the first segment
        step = get_end_of_day_step(first_segment, max_driving_hours_per_day)
        print(f"\nLast step of the first day: {step}\n")

        # get the coords for the end of the first day
        route_geometry = initial_directions["features"][0]["geometry"]
        coords = coordinates_from_waypoints(step, route_geometry)

        print(f"Location at end of first day: {coords[1]}")

        # have we reached the end of the trip at the end of the first day?
        is_end_trip = reached_end_trip(step, initial_directions)
        print(f"\nAre we at the end of the trip? {is_end_trip}\n")

        # have we reached the end of the first segment?
        is_end_segment = reached_end_first_segment(step, initial_directions)
        print(f"\nAre we at the end of the first segment? {is_end_segment}\n")

        # if we have reached the end of the trip, then we have our full directions now
        if is_end_trip:
            print(f"\nTrip takes less than one full day of driving.\nUse initial directions as full directions.\nFull directions complete ending at {coords}")

        # if we have reached the end of the segment, but not the end of the trip, 
        # then we have full directions for one segment. we move to the next
        # segment
        elif is_end_segment and not is_end_trip:
            print(f"Reached end of segment at {coords} but not end of trip.")

            # just use the segment start and end - no need to update directions (when a hotel is chosen, the directions are updated from the hotel)

        # if we haven't reached the end of a trip or a segment, then we have only
        # reached the end of the driving day and we must find a hotel then get updated directions for the rest of the route from there
        else:
            print(f"Reached end of day at {coords} with a remainder of the segment to complete the next day.")

if __name__=="__main__":

    addresses = ["1709 F Street bellingham wa", "820 15 ave sw calgary ab"]
    max_driving_hours_per_day = 7

    d = get_full_route_coordinates(addresses, max_driving_hours_per_day)

    print(d)