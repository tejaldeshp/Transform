"""
This function filters the dataframe as per the parameters provided 
Input:  df- dataframe to be manipulated (type = dataframe)
        filter_dict- dictionary of columns and their values to be filtered on (type = dict)
Output: dataframe
Call : df = dfFilter(df, filter_dict = {"SettlementPointName": "ALVIN_RN","SettlementPointType": "RN",})
"""

import pandas as pd

# filter_dict={
#   "SettlementPointName": ["ALVIN_RN"],
#   "SettlementPointType": ["RN"],
# }

def dfFilter(df, filter_dict):
    for k,v in filter_dict.items():
        df = df[df[k].isin(v)]
    return df
