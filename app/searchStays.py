from api_calls.airbnb.search import main as search_airbnb
from api_calls.priceline.search import main as search_priceline
from api_calls.openroute_service.directions import get_driving_directions
import pandas as pd

def search_all_stays(coordinates:tuple, checkIn:str, checkOut:str, range:int=500, limit:int=5, page:int=1) -> pd.DataFrame:
    """
    Takes all accommodation apis and searches across all of them with one function.

    Params:
    coordinates (tuple): center of search area as (lat, long)
    checkIn (str): desired check in date YYYY-MM-DD
    checkOut (str): desired check out date YYYY-MM-DD
    range (int): metres from searched address, applies only to airbnbs.
    limit (int): number of results returned per page, applies only to priceline hotels.
    page (int): 1-base indexed page of results, applies only to priceline hotels.

    Returns: 
    - DataFrame with details for airbnbs and priceline hotels within the search parameters
    """

    col_order = ['accomodationId', 'accomodationTitle', 'city', 'avgGuestRating', 'checkIn', 'checkOut', 'lat', 'long']

    hotels = search_priceline(coordinates, checkIn, checkOut, limit, page)
    df_hotels = pd.DataFrame(hotels)
    cols_hotels = {
        'hotelId':'accomodationId'
        , 'hotelName':'accomodationTitle'
        , 'cityName':'city'
        , 'overallGuestRating':'avgGuestRating'
        #, 'dealTypes'
        #, 'nightlyRateIncludingTaxesAndFees'
        #, 'grandTotal'
        , 'checkIn':'checkIn'
        , 'checkOut':'checkOut'
        , 'latitude':'lat'
        , 'longitude':'long'
    }
    df_hotels.rename(columns=cols_hotels, inplace=True)
    df_hotels = df_hotels[col_order]
    df_hotels["stayType"] = 'hotel'

    airbnbs = search_airbnb(coordinates, checkIn, checkOut, range)
    if airbnbs is not None:
        df_airbnbs = pd.DataFrame(airbnbs)
        cols_airbnb = {
        'airbnb_id':'accomodationId'
        , 'listingTitle':'accomodationTitle'
        , 'city':'city'
        # is this guest rating or hotel star-level?
        , 'starRating':'avgGuestRating'

        ### need to get price from another airbnb api call
        #, 'nightlyRate'

        #, 'maxGuestCapacity'
        #, 'bedrooms'
        #, 'beds'
        #, 'bathrooms'
        #, 'bathroomsShared'
        #, 'propertyType'
        #, 'cancel_policy'
        #, 'min_nights'
        #, 'max_nights'
        , 'check_in_time':'checkIn'
        , 'check_out_time':'checkOut'
        #, 'listingstatus'
        , 'listingLat':'lat'
        , 'listingLng':'long'
        }
        df_airbnbs.rename(columns=cols_airbnb, inplace=True)
        df_airbnbs = df_airbnbs[col_order]
        df_airbnbs["stayType"] = 'airbnb'

        df = pd.concat([df_airbnbs, df_hotels]) 
    else:
        df = df_hotels

    df['createdTimestamp'] = pd.Timestamp.now()  

    return df

def get_best_stay(df, centroid: tuple) -> dict:
    """
    Determine what accommodation is closest to the center of the search area

    Params:
    - df (pd.DataFrame): combined data for all accommodation providers including the location's coordinates
    - centroid (tuple): center of the search area as lat, long
    
    Returns:
    - (dict) the row from the dataframe that contains the best stay
    """
    best_stay = None
    best_proximity = None

    for index, row in df.iterrows():
        start_coordinates = (row["lat"], row["long"])
        driving_directions = get_driving_directions(start_coordinates, centroid)
        proximity_to_centroid = driving_directions["features"][0]["properties"]["summary"]["duration"]

        if best_stay is None or proximity_to_centroid < best_proximity:
            best_proximity = proximity_to_centroid # update with the better value
            best_stay = df.iloc[index]

    return best_stay.to_dict()