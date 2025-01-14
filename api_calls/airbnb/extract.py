import pandas as pd
import json

def parse_airbnb_listings_lat_long(response:dict) -> pd.DataFrame:
    """
    Parse the response for the search() function.
    Return a list of dictionaries for each airbnb containing the address info.
    """
    airbnb_ids=[]
    for airbnb in response["results"]:
        airbnb_ids.append(
            {
                "airbnb_id":airbnb["airbnb_id"]
                , "distance":airbnb["distance"]
            }
        )
    airbnb_ids_df=pd.DataFrame(airbnb_ids)
    
    return airbnb_ids_df

def parse_airbnb_details(response:dict) -> pd.DataFrame:
    """
    Parse the response for details on an individual airbnb unit.
    """
    details_dict = response["results"][0]
    airbnb_details=[
        {
            "airbnb_id":details_dict["airbnb_id"]
            , "city":details_dict["city"]
            , "listingTitle": details_dict["listingTitle"]
            , "reviewCount":details_dict["reviewCount"]
            , "starRating":details_dict["starRating"]
            , "maxGuestCapacity":details_dict["maxGuestCapacity"]
            , "bedrooms":details_dict["bedrooms"]
            , "beds":details_dict["beds"]
            , "bathrooms":details_dict["bathrooms"]
            , "bathroomShared":details_dict["bathroomShared"]
            , "propertyType":details_dict["propertyType"]
            , "listingLat":details_dict["listingLat"]
            , "listingLng":details_dict["listingLng"]
            , "cancel_policy":details_dict["cancel_policy"]
            , "min_nights":details_dict["min_nights"]
            , "max_nights":details_dict["max_nights"]
            , "check_in_time":details_dict["check_in_time"]
            , "check_out_time":details_dict["check_out_time"]
            , "listingstatus":details_dict["listingstatus"]
        }
    ]
    
    airbnb_details_df=pd.DataFrame(airbnb_details)

    return airbnb_details_df

if __name__=='__main__':
    # load raw json response
    with open('./jsons/search_id/13-01-2025_10:54:22.json', 'r') as f:
        response = json.load(f)

    df = parse_airbnb_details(response)
    print(df.head())