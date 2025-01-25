from searchAirbnbByAddress import search as searchAirbnb
from searchPricelineByAddress import search as searchPriceline

def search_all_stays(address:str, checkIn:str, checkOut:str, range:int=500, limit:int=10, page:int=1):
    """
    Takes all accommodation apis and searches across all of them with one function.
    range (metres from searched address) applies only to airbnbs.
    limit (number of results returned per page) applies only to priceline hotels.
    page (1-base indexed page of results) applies only to priceline hotels.
    """
    # search all accommodation sources
    airbnbs = searchAirbnb(address, checkIn, checkOut, range)
    hotels = searchPriceline(address, checkIn, checkOut, limit, page)

    # TO DO combine into one result
    stays = airbnbs + hotels

    # geocode correct ranges/proximities to search coords/address to stay consistent between stay types
    for stay in stays:
        # use geoapify or openrouteservice to get distance from searched address via a directions/routing api
        pass
    
    return stays