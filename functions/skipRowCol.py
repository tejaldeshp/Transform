"""
This function drops all the columns and rows whose index is passed as parameters
Input:  df- dataframe to be manipulated (type = dataframe)
        skiprow- list of row indices to be skipped(type = list)
        skipcol- list of column indices to be skipped(type = list)
Output: dataframe
Call : df = SkipRowCol(df,skiprow=[0,3,5], skipcol=[3])
"""

import pandas as pd

# params={
#     "skiprow" :[],
#     "skipcol" :[]
# }

def skipRowCol(df,params):
    rows=df.index
    cols = df.columns
    if params["skiprow"]:
        df = df.drop([rows[x] for x in params["skiprow"]], axis="rows")
    if params["skipcol"]:
        df = df.drop([cols[x] for x in params["skipcol"]], axis="columns")
    return df