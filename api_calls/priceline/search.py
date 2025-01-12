import requests

def search_hotels(locationId:int, checkIn, checkOut, rooms=None, adults=None, children=None, limit=None, page=None, sort=None, hotelsType=None, minPrice=None, maxPrice=None, guestScore=None, starLevel=None, neighborhoods=None, amenities=None, propertyType=None, hotelName=None) -> dict:
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

    headers = {

    }

    response = requests.get(url, headers=headers, params=querystring)
    response = response.json()

    # add checkIn and checkOut dates to the response
    response["checkIn"]=checkIn
    response["checkOut"]=checkOut

    return response

if __name__=='__main__':
    payload={
        "locationId":3000012156
        , "checkIn":"2025-04-12"
        , "checkOut":"2025-04-14"
        , "limit":1
    }
    print(search_hotels(**payload))