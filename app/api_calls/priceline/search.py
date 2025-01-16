import requests
import json

def search_location_ids(lat, lon) -> dict:
    url = "https://priceline-com2.p.rapidapi.com/hotels/nearby"

    querystring = {"latitude":str(lat),"longitude":str(lon)}

    with open('api_calls/priceline/key.json', 'r') as f:
        apiKey = json.load(f)

    headers = {
        "x-rapidapi-key":apiKey["x-rapidapi-key"]
        , "x-rapidapi-host": "priceline-com2.p.rapidapi.com"
    }
               
    response = requests.get(url, headers=headers, params=querystring)
    response = response.json()
    print(response["message"])

    # print if there is no data available.
    if response["data"] == None:
        print("No data available.")

    return response

def search_hotels(locationId, checkIn, checkOut, rooms=None, adults=None, children=None, limit=None, page=None, sort=None, hotelsType=None, minPrice=None, maxPrice=None, guestScore=None, starLevel=None, neighborhoods=None, amenities=None, propertyType=None, hotelName=None) -> dict:
    """
    Pass in some search terms and get results for matching hotels with details.
    """
    url = "https://priceline-com2.p.rapidapi.com/hotels/search"

    querystring = {"locationId":locationId, "checkIn":checkIn, "checkOut": checkOut}

    if rooms is not None:
        querystring["rooms"]=rooms
    if adults is not None:
        querystring["adults"]=adults
    if children is not None:
        querystring["children"]=children
    if limit is not None:
        querystring["limit"]=limit
    if page is not None:
        querystring["page"]=page
    if sort is not None:
        querystring["sort"]=sort
    if hotelsType is not None:
        querystring["hotelsType"]=hotelsType
    if minPrice is not None:
        querystring["minPrice"]=minPrice
    if maxPrice is not None:
        querystring["maxPrice"]=maxPrice
    if guestScore is not None:
        querystring["guestScore"]=guestScore
    if starLevel is not None:
        querystring["starLevel"]=starLevel
    if neighborhoods is not None:
        querystring["neighborhoods"]=neighborhoods
    if amenities is not None:
        querystring["amenities"]=amenities
    if propertyType is not None:
        querystring["propertyType"]=propertyType
    if hotelName is not None:
        querystring["hotelName"]=hotelName

    print(f"Num records returning:{limit}")

    with open('api_calls/priceline/key.json', 'r') as f:
        apiKey = json.load(f)

    headers = {
        "x-rapidapi-key":apiKey["x-rapidapi-key"]
        , "x-rapidapi-host": "priceline-com2.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=querystring)
    response = response.json()
    print(response["message"])

    # print if there is no data available.
    if response["data"] == None:
        print("No data available.")

    # add checkIn and checkOut dates to the response
    response["checkIn"]=checkIn
    response["checkOut"]=checkOut

    # create a list of dicts containing subset of info returned for each hotel
    hotel_info = []
    for hotel in response["data"]["hotels"]:
        location_dict={
            "hotelName":hotel["name"]
            , "hotelId":hotel["hotelId"]
            , "pclnId":hotel["pclnId"]
            , "address":hotel["location"]["address"]["addressLine1"]
            , "cityName":hotel["location"]["address"]["cityName"]
            , "provinceCode":hotel["location"]["address"]["provinceCode"]
            , "neighborhoodName":hotel["location"]["neighborhoodName"]
            , "latitude":hotel["location"]["latitude"]
            , "longitude":hotel["location"]["longitude"]
            , "overallGuestRating":hotel["overallGuestRating"]
            # dealTypes is returned as a list if any entries exist, otherwise returns None
            , "dealTypes":"".join(str(z) for z in (['none' if hotel["dealTypes"]==None else (" ".join((str(x) for x in ['none' if d==None else d for d in hotel["dealTypes"]])))]))
            , "nightlyRateIncludingTaxesAndFees":hotel["ratesSummary"]["nightlyRateIncludingTaxesAndFees"]
            , "grandTotal":hotel["ratesSummary"]["grandTotal"]
            , "proximity":hotel["proximity"]
            , "checkIn":response["checkIn"]
            , "checkOut":response["checkOut"]
        }
        hotel_info.append(location_dict)

    return hotel_info

if __name__=='__main__':
    payload={
        "locationId":3000012156
        , "checkIn":"2025-04-12"
        , "checkOut":"2025-04-14"
        , "limit":1
    }
    print(search_hotels(**payload))