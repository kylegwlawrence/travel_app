from searchAirbnbByAddress import search as searchAirbnb
from searchPricelineByAddress import search as searchPriceline
from api_calls.geocoder.search import geocode_address
from api_calls.openroute_service.directions import driving_directions
import pandas as pd

def search_all_stays(coordinates:tuple, checkIn:str, checkOut:str, range:int=500, limit:int=10, page:int=1) -> pd.DataFrame:
    """
    Takes all accommodation apis and searches across all of them with one function.

    Params:
    coordinates (tuple): center of search area as (lat, long)
    checkIn (str): desired check in date
    checkOut (str): desired check out date
    range (int): metres from searched address, applies only to airbnbs.
    limit (int): number of results returned per page, applies only to priceline hotels.
    page (int): 1-base indexed page of results, applies only to priceline hotels.

    Returns: 
    - DataFrame with details for airbnbs and priceline hotels within the search parameters
    """

    # search all accommodation sources
    airbnbs = searchAirbnb(coordinates, checkIn, checkOut, range)
    hotels = searchPriceline(coordinates, checkIn, checkOut, limit, page)

    # convert to dataframes
    df_airbnbs = pd.DataFrame(airbnbs)
    df_hotels = pd.DataFrame(hotels)

    # keep fields that are common between airbnb and priceline
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

    # rename columns
    df_airbnbs.rename(columns=cols_airbnb, inplace=True)
    df_hotels.rename(columns=cols_hotels, inplace=True)

    # impose column order
    col_order = ['accomodationId', 'accomodationTitle', 'city', 'avgGuestRating', 'checkIn', 'checkOut', 'lat', 'long']
    df_airbnbs = df_airbnbs[col_order]
    df_hotels = df_hotels[col_order]

    # add airbnb/hotel indicator
    df_airbnbs["stayType"] = 'airbnb'
    df_hotels["stayType"] = 'hotel'

    # union dataframes
    df = pd.concat([df_airbnbs, df_hotels])

    # add timestamp
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
        format_coords = [[row["long"], row["lat"]], [centroid[1], centroid[0]]]
        d = driving_directions(format_coords)
        proximity_to_centroid = d["features"][0]["properties"]["summary"]["duration"]

        if best_stay is None or proximity_to_centroid < best_proximity:
            best_proximity = proximity_to_centroid # update with the better value
            best_stay = df.iloc[index]

    return best_stay.to_dict()

if __name__=='__main__':
    coords = geocode_address("820 15 ave SW calgary ab")

    #df = search_all_stays(coords, "2025-05-11", "2025-05-14", range=500, limit=10, page=1)
    
    df = pd.read_csv("stays.csv")

    best_stay = get_best_stay(df, coords)
    print(best_stay.to_dict())

    #df.to_csv("stays.csv", index=False)