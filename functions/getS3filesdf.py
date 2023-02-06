"""
This function returns the dataframe of the files of 1 type(dam, rtm or ancillary), 
Input: S3path list for that type
Output: DataFrame of data of input type
Call: damdf = getS3filesdf(damS3path)
"""

import pandas as pd
from functions.getfiles import *
from qws.Q3.shared import *   

def getS3filesdf(paths):
    q3 = Q3()
    dfs = []
    for path in paths:
        l = path.replace("s3://", "").split("/")
        path = "/".join(l[1:])
        buffer = q3.download_file("us-ercot",path)
        files = process_buff_zipfile(buffer)
        for file in files:
            dfs.append(pd.read_csv(file))
    df = pd.concat(dfs)
    return df