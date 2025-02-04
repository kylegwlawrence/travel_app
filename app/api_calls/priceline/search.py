import requests
import json
import os

def search_location_ids(lat, lon) -> dict:
    """
    Searches for hotels near a given lat and long set of coordinates. 
    Returns the response as a dictionary
    """

    # set api url
    url = "https://priceline-com2.p.rapidapi.com/hotels/nearby"

    # define query
    querystring = {"latitude":str(lat),"longitude":str(lon)}

    # define headers
    headers = {
        "x-rapidapi-key":os.environ["PRICELINE_KEY"]
        , "x-rapidapi-host": "priceline-com2.p.rapidapi.com"
    }
               
    # call api and get a response
    response = requests.get(url, headers=headers, params=querystring)
    response = response.json()
    print(f"""Api response for {url}\n{response["message"]}""")

    # log to console if there is no data available.
    if response["data"] == None:
        print("No data available.")

    return response

def search_hotels(locationId, checkIn, checkOut, rooms=None, adults=None, children=None, limit=None, page=1, sort=None, hotelsType=None, minPrice=None, maxPrice=None, guestScore=None, starLevel=None, neighborhoods=None, amenities=None, propertyType=None, hotelName=None) -> list:
    """
    Pass in some search terms to get results for matching hotels with details.

    Params:
    locationId ():
    checkIn ():
    checkOut ():
    rooms ():
    adults ():
    children ():
    limit ():
    page ():
    sort ():
    hotelsType ():
    minPrice ():
    maxPrioce ():
    guestScore ():
    starLevel ():
    neighborhoods ():
    amenities ():
    propertyType ():
    hotelName ():

    Returns: a list of dictionaries where each dictionary contains details for one hotel
    """

    # set api url
    url = "https://priceline-com2.p.rapidapi.com/hotels/search"

    # define query
    querystring = {"locationId":locationId, "checkIn":checkIn, "checkOut": checkOut}

    # add params to the querystring if they are passed into the function args
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

    # define headers
    headers = {
        "x-rapidapi-key":os.environ["PRICELINE_KEY"]
        , "x-rapidapi-host": "priceline-com2.p.rapidapi.com"
    }

    # call api and get a response
    response = requests.get(url, headers=headers, params=querystring)
    response = response.json()
    print(f"""Api response for {url}\n{response["message"]}""")

    # print if there is no data available.
    if response["data"] == None:
        print("No data available.")

    # add checkIn and checkOut dates to the data that will be returned
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