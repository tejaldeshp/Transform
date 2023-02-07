"""
This function transforms the data in a raw file to required form
Input: folder of iso, date, node, frequency of data
Output: DataFrame or csv of cleanedup, merged - dam, rtm and ancillary data of that day
Call: transform("ercot", "CHISMGRD_RN", date ="2022-01-31", freq ="15T")
"""

from functions.datetimeCombine import *
from functions.dropCol import *
from functions.renameCol import *
from functions.pivot import *
from functions.resample import *
from functions.get_priceDfs import *
from functions.hashfunction import *
from functions.dfFilter import *
from functions.melt import *
from functions.addCol import *
from functions.addColsame import *
import pandas as pd
import json



def transform(iso, node, freq="H", date=None):
    functions={
        "datetimeCombine" : datetimeCombine,
        "dropCol" :dropCol,
        "pivot" :pivot,
        "resample" :resample,
        "renameCol" :renameCol,
        "dfFilter" :dfFilter,
        "melt" :melt,
        "addColsame":addColsame
    }

    mapfiles={
        "ercot" : "ErcotMapping.json",
        "miso" : "MisoMapping.json",
    }

    f = open(mapfiles[iso])
    iso_map = json.load(f)

    damdf,rtmdf,ancillarydf = get_priceDfs(iso, date, mode="DEBUG")
    
    damdf = damdf[damdf[iso_map["dam"]["node"]]==node]
    rtmdf = rtmdf[rtmdf[iso_map["rtm"]["node"]]==node]
    if iso == "miso":
        if node in ancillarydf["Unnamed: 0"].values:
            ancillarydf = ancillarydf[ancillarydf["Unnamed: 0"]==node]
        else:
            ancillarydf = ancillarydf[ancillarydf["Unnamed: 0"]=="MISO Wide"]
    
    #using the mapping json file run the required functions on each of the file
    #dam
    for items in iso_map["dam"]["functions"]:
        damdf = functions[items](damdf, iso_map["dam"]["functions"][items])
        print(damdf)
    
    #ancillary
    for items in iso_map["ancillary"]["functions"]:
        ancillarydf = functions[items](ancillarydf, iso_map["ancillary"]["functions"][items])
        print(ancillarydf)
    
    #rtm
    for items in iso_map["rtm"]["functions"]:
        rtmdf = functions[items](rtmdf, iso_map["rtm"]["functions"][items])
        print(rtmdf)
    
    
    
    # damdf.to_csv("dam.csv")
    # rtmdf.to_csv("rtm.csv")
    # ancillarydf.to_csv("ancillary.csv")

    #merge the 3 dataframes add the timezone specific to that iso
    df = pd.merge_ordered(rtmdf, damdf,  how="outer", on=["date","node"], fill_method="ffill")
    df = pd.merge_ordered(df, ancillarydf,  on = "date",how="outer", fill_method="ffill")
    print(df)
    df.dropna(inplace=True)
    df["timezone"] = iso_map["inputs"]["timezone"]

    #resample using input frequency
    iso_map["output"]["functions"]["resample"]["freq"] = freq
    for items in iso_map["output"]["functions"]:
        df = functions[items](df, iso_map["output"]["functions"][items])

    df = df[["date","px_da","px_rt","px_up","px_down","px_spin","px_nspin","timezone"]]
    df.sort_values("date", inplace=True)
    print(df)


    # #Testing if values are correct
    # testdf = pd.read_csv("/home/tejaldeshpande/Desktop/DjangoProjects/Transform/TestFiles/chismgrd_rn_15min_jan31_2022.csv")
    # testdf = testdf.iloc[:-1,:]
    # print(testdf)

    # newdf = df.compare(testdf)
    # if newdf.empty:
    #     print("Test Passed")
    # else:
    #     print("Test failed")


    #save it as a csv with name - nodename_fromdate_todate_prices.csv
    df.to_csv(f"hist_darts_prices_{node}_{date}.csv", index=False)


transform("miso", "AECI", date ="2022-01-01")