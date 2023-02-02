from functions.getfiles import *
from functions.createDf import *
from functions.datetimeCombine import *
from functions.dropCol import *
from functions.renameCol import *
from functions.pivot import *
from functions.resample import *
from functions.datetimeConvert import *
import pandas as pd
import numpy as np
import json


"""
This function transforms the data in a raw file to required form
Input: folder of iso, folder of type of file, startdate, enddate, node
Output: DataFrame or csv of cleanedup, merged - dam, rtm and ancillary data
"""


def transform(paths, node, startdate=None, enddate=None):
    functions={
        "datetimeCombineErcot" : datetimeCombineErcot,
        "dropCol" :dropCol,
        "pivot" :pivot,
        "resample" :resample,
        "renameCol" :renameCol,
        "datetimeConvert" :datetimeConvert
    }

    f = open("ErcotMapping.json")
    ercot_map = json.load(f)

    # get files using unzip function for specified daterange 
    dam = [get_csvfile_path(path) for path in (paths["dam"])]
    rtm = [get_csvfile_path(path) for path in (paths["rtm"])]
    ancillary = [get_csvfile_path(path) for path in (paths["ancillary"])] 
    
    #create dataframes from csv and concat all the files and get the data of specific node
    damdf = pd.concat([pd.read_csv(i) for sublist in dam for i in sublist])
    rtmdf = pd.concat([pd.read_csv(i) for sublist in rtm for i in sublist])
    ancillarydf = pd.concat([pd.read_csv(i) for sublist in ancillary for i in sublist])
    
    damdf = damdf[damdf["SettlementPoint"]==node]
    rtmdf = rtmdf[rtmdf["SettlementPoint"]==node]

    
    #using the mapping json file run the required functions on each of the file

    #dam
    for items in ercot_map["dam"]["functions"]:
        damdf = functions[items](damdf, ercot_map["dam"]["functions"][items])
    
    #ancillary
    for items in ercot_map["ancillary"]["functions"]:
        ancillarydf = functions[items](ancillarydf, ercot_map["ancillary"]["functions"][items])
    
    #rtm
    for items in ercot_map["rtm"]["functions"]:
        rtmdf = functions[items](rtmdf, ercot_map["rtm"]["functions"][items])
    
    rtmdf.sort_values("date", inplace=True)
    damdf.to_csv("dam.csv")
    rtmdf.to_csv("rtm.csv")
    ancillarydf.to_csv("ancillary.csv")

    #merge the 3 dataframes add the timezone specific to that iso
    df = pd.merge_ordered(rtmdf, damdf,  how="outer", on=["date","node"], fill_method="ffill")
    df = pd.merge_ordered(df, ancillarydf,  on = "date",how="outer", fill_method="ffill")
    df.dropna(inplace=True)
    print(df)

    #save it as a csv with name - nodename_fromdate_todate_prices.csv
    df.to_csv(f"hist_darts_prices_{node}_{startdate}_{enddate}.csv")

paths = {
    "dam" : ["/home/tejaldeshpande/Desktop/DjangoProjects/Transform/ercot/dam"],
    "rtm" :["/home/tejaldeshpande/Desktop/DjangoProjects/Transform/ercot/rtm"],
    "ancillary" :["/home/tejaldeshpande/Desktop/DjangoProjects/Transform/ercot/ancillary"]
    }
transform(paths, "AMO_AMOCO_G1")

####make a separate function for getting files of the 3 categories in 3 folders and send it to transform

##merge function needs to merge on dam hourly and rtm 5-min and add the timezone column

##take freq input from function parameter and resample on that freq and default on hour

##test function - script set of dates with predefined nodes 