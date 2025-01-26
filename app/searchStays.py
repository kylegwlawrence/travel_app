from searchAirbnbByAddress import search as searchAirbnb
from searchPricelineByAddress import search as searchPriceline
import pandas as pd

def search_all_stays(address:str, checkIn:str, checkOut:str, range:int=500, limit:int=10, page:int=1):
    """
    Takes all accommodation apis and searches across all of them with one function.
    range (metres from searched address) applies only to airbnbs.
    limit (number of results returned per page) applies only to priceline hotels.
    page (1-base indexed page of results) applies only to priceline hotels.
    """

    # search all accommodation sources
    airbnbs = searchAirbnb(address, checkIn, checkOut, range)
    hotels = searchPriceline(address, checkIn, checkOut, limit, page)

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

    # impost column order
    col_order = ['accomodationId', 'accomodationTitle', 'city', 'avgGuestRating', 'checkIn', 'checkOut', 'lat', 'long']
    df_airbnbs = df_airbnbs[col_order]
    df_hotels = df_hotels[col_order]

    # add airbnb/hotel indicator
    df_airbnbs["stayType"] = 'airbnb'
    df_hotels["stayType"] = 'hotel'

    # union dataframes
    df = pd.concat([df_airbnbs, df_hotels])

    # geocode correct ranges/proximities to search coords/address to stay consistent between stay types
    
    return df


if __name__=='__main__':
    df = search_all_stays("820 15 ave SW calgary ab", "2025-05-11", "2025-05-14", range=500, limit=10, page=1)
    df.to_csv("test_stays.csv", index=False)