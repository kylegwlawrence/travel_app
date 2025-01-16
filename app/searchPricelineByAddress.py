from api_calls.geocoder.app import geocode_address
from api_calls.priceline.search import search_location_ids, search_hotels

def search(address:str, checkIn:str, checkOut:str, limit:str) -> dict:

    # get the geo coordinates for the address
    lat, lon = geocode_address(address)
    print(f"Coordinates: {lat}, {lon}")

    # find location ids near set of coordinates
    location_ids = search_location_ids(lat, lon)

    # get the location_id that matches exactly to the lat lon coordinates
    matched_location_id = location_ids["data"]["exactMatch"]["matchedCity"]["cityID"]

    # use location id to search for hotels
    hotels = search_hotels(locationId=matched_location_id, checkIn=checkIn, checkOut=checkOut, limit=limit)

    return hotels

if __name__=='__main__':
    print(search("Eureka Montana", "2025-04-12", "2025-04-14", limit=50))