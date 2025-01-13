import pandas as pd

def parse_airbnb_id(response:dict) -> pd.DataFrame:
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
    airbnb_df=pd.DataFrame(airbnb_ids)
    return airbnb_df

def parse_airbnb_details(response:dict) -> pd.DataFrame:
    """
    Parse the response for details on an individual airbnb unit.
    """
    results=response["results"]
    return response