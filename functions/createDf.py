"""
This function creates a dataframe from a csv or an xlsx file 
Input:  filename- filename with path (type = str)
        skiprows- no. of rows to skip (type = int)
Output: dataframe
Call : df = createDf(filename,4)
"""

import pandas as pd

def createDf(filename, skiprows=0):
    if filename.lower().endswith(".csv"):
        df = pd.read_csv(filename, skiprows=skiprows)
    elif filename.lower().endswith(".xlsx"):
        df = pd.read_excel(filename)
    return df