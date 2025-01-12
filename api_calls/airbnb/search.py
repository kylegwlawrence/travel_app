import requests
import json

def search_airbnb_listings_lat_long(lat, lng, range, offset, bedrooms, maxGuestCapacity) -> dict:
    """
    Takes search params and returns a dictionary of matching hotels.
    Params:
    lat (str): cartesian latitude coordinate
    lng (str): cartesian longitude coordinate
    range (str): 
    """
    url = "https://airbnb-listings.p.rapidapi.com/v2/listingsByLatLng"
    querystring = {"lat":lat,"lng":lng,"range":range,"offset":offset,"bedrooms":bedrooms,"maxGuestCapacity":maxGuestCapacity}

    # load api key
    with open('key.json', 'r') as f:
        headers = json.load(f)

    response = requests.get(url, headers=headers, params=querystring)

    return response.json()

def search_airbnb_listing_details() -> dict:
    """
    Pass in some search terms and get results for matching hotels with details.
    """
    url = "https://airbnb-search.p.rapidapi.com/property/search"

    querystring = {"query":"New York, NY"}

    headers = {
        "x-rapidapi-key": "6c3d5cd8fbmsh6d198fc2bad3880p101e53jsn7c22ceb20447",
        "x-rapidapi-host": "airbnb-search.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=querystring)

    # add checkIn and checkOut dates to the response
    response["checkIn"]=checkIn
    response["checkOut"]=checkOut

    return response

if __name__=='__main__':
    payload={

    }
    print(search_airbnb_listing_details(**payload))