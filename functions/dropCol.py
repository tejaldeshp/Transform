"""
This function drops all the columns provided in parameter
Input:  df- dataframe to be manipulated (type = dataframe)
        col_drop- list of columns to drop from the dataframe (type = list)
Output: dataframe
Call : df = dropCol(df, col_drop = ["Value"])
"""

import pandas as pd

""" function with 1 dataframe and 1 dict as input"""
#the other way of doing this would be to take in a dictionary of required columns and their rename values as input
def dropCol(df, col_drop):
    return df.drop(list(col_drop), axis="columns")