from search import search_airbnb_listings_lat_long, search_airbnb_listing_details
from extract import parse_airbnb_listings_lat_long, parse_airbnb_details
import pandas as pd
import json

def get_airbnbs(lat, lng, bedrooms, maxGuestCapacity, range="500", offset="0") -> str:
    """
    Runs api call to airbnb to get airbnb ids and their proximity in meters to the lat lng coordinates.

    Returns the name of the csv file dataframe is saved to.
    """
    # call for data and save response to disk
    json_file_path = search_airbnb_listings_lat_long(lat, lng, bedrooms, maxGuestCapacity, range, offset)

    # open the response that was saved to disk
    with open(json_file_path, "r") as f:
        response = json.load(f)

    # parse into a dataframe
    airbnbs=parse_airbnb_listings_lat_long(response)

    # make file name for csv
    csv_file_path = f"csvs/lat_lng_search/{json_file_path.split('/')[-1].replace('json','csv')}"

    # save df to a csv
    airbnbs.to_csv(csv_file_path, index=False)

    # return csv file path
    return csv_file_path

def get_details(id)-> pd.DataFrame:
    """
    Grab data from the api and output selected fields as a dataframe
    """
    # call the api and save response to disk
    file_name = search_airbnb_listing_details(id)

    # open the response that was saved to disk
    with open(file_name, "r") as f:
        response = json.load(f)

    # parse into a dataframe
    airbnb_details=parse_airbnb_details(response)

    # save df to a csv
    airbnb_details.to_csv(f"""csvs/details_search/{file_name.replace('json','csv')}""", index=False)

    # return csv file name
    return f"{file_name.replace('json','csv')}"

if __name__=="__main__":
    with open('test_args.json', 'r') as f:
        args = json.load(f)

    file_path = get_airbnbs(**args)

    print(file_path)



    #id = "619966061834034729"
    #print(get_details(id))