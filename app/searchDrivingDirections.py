from api_calls.geocoder.app import geocode_address
from api_calls.driving_directions.app import search_driving_directions, parse_info
import json

def search(addresses:list):
    """
    Takes in a comma-separated list of addresses and provides driving directions between the addresses. The addresses must be in order.
    
    Params:
    addresses (list): a list, of at least length 2, of the addresses to retrieve driving directions between. If there are more than 2 addresses, then driving directions are created sequentially between the addresses. 

    Returns (list of dicts): detailed directions
    """

    # enforce list length >1
    if len(addresses)<2:
        raise TypeError("list of addresses must have at least 2 addresses")

    # geocode the addresses
    geocoded_addresses = []
    for address in addresses:

        # get lat and long from geocoder and add it to the geocoded address list
        lat, long = geocode_address(address)
        geocoded_addresses.append([lat, long])

    # search for directions between the ordered addresses using lat and long
    driving_directions = search_driving_directions(geocoded_addresses)

    # pull the important information out of the results
    #important_info = parse_info(addresses, driving_directions)

    return driving_directions

if __name__=="__main__":
    
    addresses = ["1709 F Street bellingham wa", "125 N Samish Way, Bellingham, WA 98225", "1009 Larrabee Ave, Bellingham, WA 98225"]
    directions = search(addresses)

    print(directions)