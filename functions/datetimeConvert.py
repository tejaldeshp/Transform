import pandas as pd

# params ={
#     "timezone":"US/Central",
#     "format":"%m/%d/%Y %H:%M:%S",
#     "col":"SCEDTimestamp"
# }

def datetimeConvert(df, params):
    df[params["col"]] = pd.to_datetime(df[params["col"]], format = params["format"]).dt.tz_localize(params["timezone"], ambiguous=True)
    return df