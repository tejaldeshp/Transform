"""
This function renames the columns in the dataframe
Input:  df- dataframe to be manipulated (type = dataframe)
        ren_dict- dictionary of columns and their respective new names (type = dict)
Output: dataframe
Call : df = renameCol(df, ren_dict = {"Node":"node","Type":"type"})
"""

import pandas as pd


""" function with 1 dataframe and 1 dict as input"""
#the other way of doing this would be to take in a dictionary of required columns and their rename values as input
def renameCol(df, ren_dict):
    return df.rename(columns = ren_dict)
    