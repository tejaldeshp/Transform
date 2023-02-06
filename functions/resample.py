"""
This function resamples the data based on input params like frequency and aggregation funtion.
Input:  df- dataframe to be manipulated having datetime-like index or add on paramseter (type = dataframe)
        params- dictionary of freq and function to be carried out while resampling (type = dict)
        on- dataframe's date columnname to resample on(type=string)
Output: dataframe
Call : df = resample(df,params={"freq":"D","function"="mean"}) or df = resample(df,params={"freq":"D","function"="mean"}, on="fordate") 
"""



import pandas as pd


params ={
    "freq":"H",
    "function":"mean",
    "timezone":"US/Central",
    "format":"%m/%d/%Y %H%M%S",
    "on":"SCEDTimestamp"
}

def resample(df,params):
    grp_cols = [x for x in df.columns if df[x].dtype == "O" and x!=params["on"]]
    df = df.groupby(grp_cols).resample(params["freq"], on=params["on"]).aggregate(params["function"], numeric_only = True)
    df.reset_index(inplace=True)
    return df


