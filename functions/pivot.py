"""
This function pivots the dataframe on parameters given
Input:  df- dataframe to be manipulated(type = dataframe)
        params- dict with keys: values(type=list), index(type=list), columns(type=list)-- (type=dict)
Output: dataframe
Call : df = pivot(df,params)
"""

import pandas as pd

# params={
# "values":["MCPC"],
# "index": ["DeliveryDate","HourEnding"],
# "columns": ["AncillaryType"]
# }

def pivot(df, params):
    df = df.pivot(index=params["index"],columns=params["columns"],values=params["values"])
    df = df.droplevel(0, axis=1).reset_index().rename_axis(columns=None)
    return df