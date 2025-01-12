import pandas as pd

def parse_data(response:dict) -> pd.DataFrame:
    """
    Parse the response for the search() function.
    Return a list of dictionaries for each hotel containing the address info.
    """
    