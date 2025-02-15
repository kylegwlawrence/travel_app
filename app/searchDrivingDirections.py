from api_calls.geocoder.search import geocode_address
from api_calls.openroute_service.directions import reached_end_first_segment, reached_end_trip, coordinates_from_waypoints, get_end_of_day_step, driving_directions

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


