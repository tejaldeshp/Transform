
from functions.createDf import *
from functions.datetimeCombine import *
from functions.dropCol import *
from functions.renameCol import *
from functions.pivot import *
from functions.resample import *
from functions.datetimeConvert import *
from functions.get_priceDfs import *
from functions.hashfunction import *
import pandas as pd
import numpy as np
import json


"""
This function transforms the data in a raw file to required form
Input: folder of iso, folder of type of file, startdate, enddate, node
Output: DataFrame or csv of cleanedup, merged - dam, rtm and ancillary data
"""


def transform(iso, node, freq="H", date=None):
    functions={
        "datetimeCombineErcot" : datetimeCombineErcot,
        "dropCol" :dropCol,
        "pivot" :pivot,
        "resample" :resample,
        "renameCol" :renameCol,
        "datetimeConvert" :datetimeConvert
    }

    mapfiles={
        "ercot" : "ErcotMapping.json"
    }

    f = open(mapfiles[iso])
    iso_map = json.load(f)

    damdf,rtmdf,ancillarydf = get_priceDfs(iso, date, mode="DEBUG")
    
    damdf = damdf[damdf[iso_map["dam"]["node"]]==node]
    rtmdf = rtmdf[rtmdf[iso_map["rtm"]["node"]]==node]

    
    #using the mapping json file run the required functions on each of the file
    print(damdf, rtmdf, ancillarydf)
    #dam
    for items in iso_map["dam"]["functions"]:
        damdf = functions[items](damdf, iso_map["dam"]["functions"][items])
    
    #ancillary
    for items in iso_map["ancillary"]["functions"]:
        ancillarydf = functions[items](ancillarydf, iso_map["ancillary"]["functions"][items])
    
    #rtm
    for items in iso_map["rtm"]["functions"]:
        rtmdf = functions[items](rtmdf, iso_map["rtm"]["functions"][items])
    
    rtmdf.sort_values("Date", inplace=True)
    # damdf.to_csv("dam.csv")
    # rtmdf.to_csv("rtm.csv")
    # ancillarydf.to_csv("ancillary.csv")

    #merge the 3 dataframes add the timezone specific to that iso
    df = pd.merge_ordered(rtmdf, damdf,  how="outer", on=["Date","node"], fill_method="ffill")
    df = pd.merge_ordered(df, ancillarydf,  on = "Date",how="outer", fill_method="ffill")
    df.dropna(inplace=True)
    df["timezone"] = "US/Central"

    #resample using input frequency
    iso_map["output"]["functions"]["resample"]["freq"] = freq
    for items in iso_map["output"]["functions"]:
        df = functions[items](df, iso_map["output"]["functions"][items])

    df = df[["Date","px_da","px_rt","px_up","px_down","px_spin"]]
    print(df)


    #save it as a csv with name - nodename_fromdate_todate_prices.csv
    df.to_csv(f"hist_darts_prices_{node}_{date}.csv", index=False)


transform("ercot", "CHISMGRD_RN", date ="2022-01-31", freq ="15T")
print("Testing Files:")
print("Created File :","/home/tejaldeshpande/Desktop/DjangoProjects/Transform/hist_darts_prices_CHISMGRD_RN_2022-01-31.csv")
print("Test File :","/home/tejaldeshpande/Desktop/DjangoProjects/Transform/TestFiles/chismgrd_rn_15min_jan31_2022.csv")
c_hash = create_hash("/home/tejaldeshpande/Desktop/DjangoProjects/Transform/hist_darts_prices_CHISMGRD_RN_2022-01-31.csv")
t_hash = create_hash("/home/tejaldeshpande/Desktop/DjangoProjects/Transform/TestFiles/chismgrd_rn_15min_jan31_2022.csv")
print(c_hash, t_hash)

####make a separate function for getting files of the 3 categories in 3 folders and send it to transform

##take freq input from function parameter and resample on that freq and default on hour....done

##test function - script set of dates with predefined nodes 