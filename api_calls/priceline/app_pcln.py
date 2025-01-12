from search import search_hotels
from extract import parse_data
import pandas as pd

def get_hotels(payload:dict) -> list:
    """
    Runs the api call and then returns a dict containing the parsed data.
    Payload is a dictionary of arguments to pass into the search function.
    Only locationId, checkIn, and checkOut are required.
    """
    search_results=search_hotels(**payload)
    hotel_dataframe=parse_data(search_results)

    return hotel_dataframe

if __name__=="__main__":
    payload={
        "locationId":3000012156
        , "checkIn":"2025-04-12"
        , "checkOut":"2025-04-14"
        , "limit":5
    }
    hotel_dataframe=get_hotels(payload)
    hotel_dataframe.to_csv("csvs/hotels.csv", index=False)