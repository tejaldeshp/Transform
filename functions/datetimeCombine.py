"""
This function combines the dataframe's date and hour column
Input:  df- dataframe to be manipulated (type = dataframe)
        dateCol- name of column containing date data(type = str)
    [params["hourCol"]- name of column containing hour data(type = str)
Output: dataframe
Call : df = 
"""

import pandas as pd
# params={
# "dateCol":"",
# "hourCol" :"",
# "format":"",
# "timezone":""
# }


def datetimeCombineMiso(df, params):
    df[params["hourCol"]]= df[params["hourCol"]].replace("HE ","",regex=True)
    df = df.astype({params["hourCol"]:"int"})
    df[params["hourCol"]] -= 1
    df[params["dateCol"]] = pd.to_datetime(df[params["dateCol"]]) + df[params["hourCol"]].astype("timedelta64[h]")
    df.drop([params["hourCol"]], axis=1, inplace=True)
    return df

def datetimeCombineErcot(df, params):
    df[params["dateCol"]] = pd.to_datetime(df[params["dateCol"]], format=params["format"])
    df[params["hourCol"]]= df[params["hourCol"]].replace(":00","",regex=True)
    df = df.astype({params["hourCol"]:"int"})
    df[params["hourCol"]] -= 1
    df[params["dateCol"]] = pd.to_datetime(df[params["dateCol"]]) + df[params["hourCol"]].astype("timedelta64[h]")
    df.drop([params["hourCol"]], axis=1, inplace=True)
    df[params["dateCol"]] = pd.to_datetime(df[params["dateCol"]].dt.tz_localize(params["timezone"], ambiguous=True))
    return df