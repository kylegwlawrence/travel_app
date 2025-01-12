import pandas as pd

def parse_data(response:dict) -> pd.DataFrame:
    """
    Parse the response for the search() function.
    Return a list of dictionaries for each hotel containing the address info.
    """
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
    hotel_dataframe=pd.DataFrame(hotel_info)

    return hotel_dataframe