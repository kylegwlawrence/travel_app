from api_calls.geocoder.search import geocode_address
from api_calls.openroute_service.directions import search_driving_directions, get_driving_steps
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
        geocoded_addresses.append([lat, long])

    # search for driving directions
    driving_directions = search_driving_directions(geocoded_addresses)

    return driving_directions

if __name__=="__main__":
    
    addresses = ["1709 F Street bellingham wa", "Blaine Washington", "114 H Street Road, Lynden Washington"]
    directions = search(addresses)

    with open("dd_test.json", "w+") as f:
        json.dump(directions, f)

    steps = get_driving_steps(directions)

    with open("steps_test.json", "w+") as f:
        json.dump(steps, f)