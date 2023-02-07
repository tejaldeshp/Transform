"""
This function adds a column to the dataframe as per the parameters provided 
Input:  df- dataframe to be manipulated (type = dataframe)
        filter_dict- dictionary of columns and their values to be filtered on (type = dict)
Output: dataframe
Call : df = dfFilter(df, filter_dict = {"SettlementPointName": "ALVIN_RN","SettlementPointType": "RN",})
"""

import pandas as pd

# add_dict={
#   "date": "",
# }

def addCol(df, add_dict):
    for k,v in add_dict.items():
        df[k] = v
    return df