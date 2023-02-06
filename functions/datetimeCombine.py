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
# "dateCol":"DeliveryDate",
# "hourCol" :"DeliveryHour",
# "minCol" :"DeliveryInterval",
# "format":"%m/%d/%Y",
# "timezone":"US/Central",
# "hour_replace":""
# }


# def datetimeCombineMiso(df, params):
#     df[params["hourCol"]]= df[params["hourCol"]].replace("HE ","",regex=True)
#     df = df.astype({params["hourCol"]:"int"})
#     df[params["hourCol"]] -= 1
#     df[params["dateCol"]] = pd.to_datetime(df[params["dateCol"]]) + df[params["hourCol"]].astype("timedelta64[h]")
#     df.drop([params["hourCol"]], axis=1, inplace=True)
#     return df

def datetimeCombine(df, params):
    df[params["dateCol"]] = pd.to_datetime(df[params["dateCol"]], format=params["format"])
    if params["hour_replace"]:
        df[params["hourCol"]]= df[params["hourCol"]].replace(params["hour_replace"],"",regex=True)
    df = df.astype({params["hourCol"]:"int"})
    df[params["hourCol"]] -= 1
    if params["minCol"]:
        df[params["minCol"]] = (df[params["minCol"]]*15) -15
        df[params["dateCol"]] = pd.to_datetime(df[params["dateCol"]]) + df[params["hourCol"]].astype("timedelta64[h]")+df[params["minCol"]].astype("timedelta64[m]")
        df.drop([params["hourCol"], params["minCol"]], axis=1, inplace=True)
    else:
        df[params["dateCol"]] = pd.to_datetime(df[params["dateCol"]]) + df[params["hourCol"]].astype("timedelta64[h]")
        df.drop([params["hourCol"]], axis=1, inplace=True)
    return df