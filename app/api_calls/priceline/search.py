import requests
import os

def search_location_ids(lat:float, lon:float) -> dict:
    """
    Gets a priceline-specific location id to use as an argument in other endpoints
    Params:
    - lat (float): latitude
    - lon (float): longitude
    Returns:
    - (dict): API response containing Priceline info for the given lat long
    """

    ENDPOINT = "https://priceline-com2.p.rapidapi.com/hotels/nearby"

    query = {"latitude":str(lat),"longitude":str(lon)}
    headers = {
        "x-rapidapi-key":os.environ["PRICELINE_KEY"],
        "x-rapidapi-host": "priceline-com2.p.rapidapi.com"
    }
               
    response = requests.get(ENDPOINT, headers=headers, params=query)
    response = response.json()
    print(f"""Api response for {ENDPOINT}\n{response["message"]}""")

    if response["data"] == None:
        raise Exception(f"Error: {response.status_code}")

    return response

def search_hotels(locationId:str, checkIn:str, checkOut:str, rooms:int=None, adults:int=None, children:int=None, limit:int=None, page:int=1, sort:str=None, hotelsType:str=None, minPrice:float=None, maxPrice:float=None, guestScore:float=None, starLevel:float=None, neighborhoods:str=None, amenities:str=None, propertyType:str=None, hotelName:str=None) -> list:
    """
    Get details for hotels that match the search criteria.

    Params:
    locationId (str): priceline's location id for the hotel
    checkIn (str): check in date. YYYY-MM-DD
    checkOut (str): check out date. YYYY-MM-DD
    rooms (int): number of rooms
    adults (int): number of adults
    children (int): number of children
    limit (int): number of results to display
    page (int): page number of resuts to display. Defaults to first page.
    sort (str): sort by various fields (not yet tested)
    hotelsType (str): type/category of hotel (not yet tested)
    minPrice (float): minimum nightly rate
    maxPrioce (float): maximum nightly rate
    guestScore (float): avg guest rating out of 10
    starLevel (float): star "tier" rating out of 5
    neighborhoods (str): neighborhood name (not yet tested)
    amenities (str): such as pet friendly, pool, etc (not yet tested)
    propertyType (str): not yet tested
    hotelName (str): not yet tested

    Returns: 
    - a list of dictionaries where each dictionary contains details for one hotel
    """

    # endpoint
    url = "https://priceline-com2.p.rapidapi.com/hotels/search"

    # query
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