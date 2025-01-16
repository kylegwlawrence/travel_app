from search import search_airbnb_listings_lat_long, search_airbnb_listing_details
from extract import parse_airbnb_listings_lat_long, parse_airbnb_details
import pandas as pd
import json



def get_details(id)-> pd.DataFrame:
    """
    Grab data from the api and output selected fields as a dataframe
    """
    # call the api and save response to disk
    json_file_path = search_airbnb_listing_details(id)

    # open the response that was saved to disk
    with open(json_file_path, "r") as f:
        response = json.load(f)

    # parse into a dataframe
    airbnb_details=parse_airbnb_details(response)

    # make file name for csv
    csv_file_path = f"csvs/details_search/{json_file_path.split('/')[-1].replace('json','csv')}"

    # save df to a csv
    airbnb_details.to_csv(csv_file_path, index=False)

    # return csv file path
    return csv_file_path

def get_details_multiple_listings():
    """
    Need to return just a dataframe from get_details to then merge all dfs into one.
    """
    pass

if __name__=="__main__":
    #with open('test_args.json', 'r') as f:
    #    args = json.load(f)

    #file_path = get_airbnbs(**args)

    #print(file_path)



    id = "16910260"
    print(get_details(id))