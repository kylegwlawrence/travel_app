import requests
import os
from typing import List, Dict

def get_priceline_location_ids(lat:float, lon:float) -> dict:
    """
    Gets a priceline-specific location id to use as an argument in other endpoints

    Params:
    - lat (float): latitude
    - lon (float): longitude
    
    Returns:
    - (dict): API response containing Priceline info for the given lat long
    """

    ENDPOINT = "https://priceline-com2.p.rapidapi.com/hotels/nearby"
    HOST = "priceline-com2.p.rapidapi.com"

    headers={
        "x-rapidapi-key":os.environ["PRICELINE_KEY"],
        "x-rapidapi-host": HOST
        }
    query={
        "latitude":str(lat),
        "longitude":str(lon)
        }
    response = requests.get(ENDPOINT, headers=headers, params=query)
    status_code = response.status_code
    response = response.json()

    if response["data"] is None:
        raise Exception(f"No data:: {status_code}\n{response}")

    return response

def get_priceline_hotels(locationId:str, checkIn:str, checkOut:str, rooms:int=None, adults:int=None, children:int=None, limit:int=None, page:int=1, sort:str=None, hotelsType:str=None, minPrice:float=None, maxPrice:float=None, guestScore:float=None, starLevel:float=None, neighborhoods:str=None, amenities:str=None, propertyType:str=None, hotelName:str=None) -> List[Dict]:
    """
    Get details for hotels that match the search criteria.
    
    Params:
    - locationId (str): priceline's location id for the hotel
    - checkIn (str): check in date. YYYY-MM-DD
    - checkOut (str): check out date. YYYY-MM-DD
    - rooms (int): number of rooms
    - adults (int): number of adults
    - children (int): number of children
    - limit (int): number of results to display
    - page (int): page number of resuts to display. Defaults to first page.
    - sort (str): sort by various fields (not yet tested)
    - hotelsType (str): type/category of hotel (not yet tested)
    - minPrice (float): minimum nightly rate
    - maxPrioce (float): maximum nightly rate
    - guestScore (float): avg guest rating out of 10
    - starLevel (float): star "tier" rating out of 5
    - neighborhoods (str): neighborhood name (not yet tested)
    - amenities (str): such as pet friendly, pool, etc (not yet tested)
    - propertyType (str): not yet tested
    - hotelName (str): not yet tested

    Returns: 
    - (list of dictionaries): each dictionary contains details for one hotel
    """

    ENDPOINT = "https://priceline-com2.p.rapidapi.com/hotels/search"
    HOST = "priceline-com2.p.rapidapi.com"

    query = {
        "locationId":locationId, 
        "checkIn":checkIn, 
        "checkOut": checkOut
        }
    if rooms is not None:
        query["rooms"]=rooms
    if adults is not None:
        query["adults"]=adults
    if children is not None:
        query["children"]=children
    if limit is not None:
        query["limit"]=limit
    if page is not None:
        query["page"]=page
    if sort is not None:
        query["sort"]=sort
    if hotelsType is not None:
        query["hotelsType"]=hotelsType
    if minPrice is not None:
        query["minPrice"]=minPrice
    if maxPrice is not None:
        query["maxPrice"]=maxPrice
    if guestScore is not None:
        query["guestScore"]=guestScore
    if starLevel is not None:
        query["starLevel"]=starLevel
    if neighborhoods is not None:
        query["neighborhoods"]=neighborhoods
    if amenities is not None:
        query["amenities"]=amenities
    if propertyType is not None:
        query["propertyType"]=propertyType
    if hotelName is not None:
        query["hotelName"]=hotelName

    headers = {
        "x-rapidapi-key":os.environ["PRICELINE_KEY"]
        , "x-rapidapi-host": HOST
    }
    response = requests.get(ENDPOINT, headers=headers, params=query)
    status_code = response.status_code
    response = response.json()

    if response["data"] == None:
        raise Exception(f"No data:: {status_code}\n{response}")

    hotel_info = []
    for hotel in response["data"]["hotels"]:
        location_dict={
            "hotelName":hotel["name"],
            "hotelId":hotel["hotelId"],
            "pclnId":hotel["pclnId"],
            "address":hotel["location"]["address"]["addressLine1"],
            "cityName":hotel["location"]["address"]["cityName"],
            "provinceCode":hotel["location"]["address"]["provinceCode"],
            "neighborhoodName":hotel["location"]["neighborhoodName"],
            "latitude":hotel["location"]["latitude"],
            "longitude":hotel["location"]["longitude"],
            "overallGuestRating":hotel["overallGuestRating"],
            #dealTypes is returned as a list if any entries exist, otherwise returns None
            "dealTypes":"".join(str(z) for z in (['none' if hotel["dealTypes"]==None else (" ".join((str(x) for x in ['none' if d==None else d for d in hotel["dealTypes"]])))])),
            "nightlyRateIncludingTaxesAndFees":hotel["ratesSummary"]["nightlyRateIncludingTaxesAndFees"],
            "grandTotal":hotel["ratesSummary"]["grandTotal"],
            "proximity":hotel["proximity"],
            "checkIn":checkIn,
            "checkOut":checkOut
        }
        hotel_info.append(location_dict)

    return hotel_info

def main(coordinates:tuple, checkIn:str, checkOut:str, limit:int, page:int=1) -> List[Dict]:
    """
    Takes a freeform addressand check in and checkout date to find matching hotels.
    
    Params:
    - coordinates (tuple): search area as (lat, long)
    - checkIn (str): check in time formatted "yyyy-mm-dd"
    - checkOut (str): check out time formatted "yyyy-mm-dd"
    - limit (int): number of records to limit per page.
    - page (int): index of page to return, 1-indexed. Defaults to first page. 

    Returns: 
    - (list of dictionaries): each dict as a hotel with its details
    - empty list if there are no exactly matching cities for the given address
    """

    location_ids = get_priceline_location_ids(coordinates[0], coordinates[1])

    matched_location_id = location_ids["data"]["exactMatch"]["matchedCity"]["cityID"]
    hotels = get_priceline_hotels(locationId=matched_location_id, checkIn=checkIn, checkOut=checkOut, limit=limit, page=page)

    return hotels