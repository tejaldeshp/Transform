from functions.getfiles import *
import json
from datetime import datetime, timedelta
import pandas as pd
from dotenv import load_dotenv
import io
from qws.Q3.shared import *


def get_priceDfs(iso, day, mode):
    mapfiles={
        "ercot" : "ErcotMapping.json"
    }

    f = open(mapfiles[iso])
    iso_map = json.load(f)
    load_dotenv()


    if mode =="DEBUG":
        paths = {
        "dam" : ["/home/tejaldeshpande/Desktop/DjangoProjects/Transform/TestFiles/rawfiles/damjan30_2022"],
        "rtm" :["/home/tejaldeshpande/Desktop/DjangoProjects/Transform/TestFiles/rawfiles/rtmjan31_2022"],
        "ancillary" :["/home/tejaldeshpande/Desktop/DjangoProjects/Transform/TestFiles/rawfiles/ancillaryjan30_2022"]
        }

        # get files using unzip function for specified daterange 
        dam = [get_csvfile_path(path) for path in (paths["dam"])]
        rtm = [get_csvfile_path(path) for path in (paths["rtm"])]
        ancillary = [get_csvfile_path(path) for path in (paths["ancillary"])] 
        
        #create dataframes from csv and concat all the files and get the data of specific node
        damdf = pd.concat([pd.read_csv(i) for sublist in dam for i in sublist])
        rtmdf = pd.concat([pd.read_csv(i) for sublist in rtm for i in sublist])
        ancillarydf = pd.concat([pd.read_csv(i) for sublist in ancillary for i in sublist])
        
    else: 
        day = datetime.strptime(day, "%Y-%m-%d")
        damday = day - timedelta(days=1)
    
        #get paths of S3 based on iso, its mapfile and year and month
        damS3path = iso_map["inputs"]["bucketname"]+iso_map["dam"]["reportfolder"]+"/"+"%04d" %damday.year+"/"+"%02d" % damday.month+"/" 
        rtmS3path = iso_map["inputs"]["bucketname"]+iso_map["rtm"]["reportfolder"]+"/"+"%04d" %day.year+"/"+"%02d" % day.month+"/" 
        ancillaryS3path = iso_map["inputs"]["bucketname"]+iso_map["ancillary"]["reportfolder"]+"/"+"%04d" %damday.year+"/"+"%02d" % damday.month+"/" 

        
        dateinstr = str(day.year) + "%02d" % day.month + "%02d" % day.day
        damdateinstr = str(damday.year) + "%02d" % damday.month + "%02d" % damday.day

        #get S3 files based on date
        q3 = Q3()
        damS3path = [x for x in q3.list("us-ercot",iso_map["dam"]["reportfolder"]+"/"+"%04d" %day.year+"/"+"%02d" % day.month+"/") if damdateinstr in x]
        rtmS3path = [x for x in q3.list("us-ercot",iso_map["rtm"]["reportfolder"]+"/"+"%04d" %day.year+"/"+"%02d" % day.month+"/") if dateinstr in x]
        ancillaryS3path = [x for x in q3.list("us-ercot",iso_map["ancillary"]["reportfolder"]+"/"+"%04d" %day.year+"/"+"%02d" % day.month+"/") if damdateinstr in x]

        #get dam files and convert to dataframe
        dadfs = []
        for path in damS3path:
            l = path.replace("s3://", "").split("/")
            path = "/".join(l[1:])
            buffer = q3.download_file("us-ercot",path)
            files = process_buff_zipfile(buffer)
            for file in files:
                dadfs.append(pd.read_csv(file))
        damdf = pd.concat(dadfs)
        print(damdf)


        #get rtm files and convert to dataframe
        rtdfs = []
        for path in rtmS3path:
            l = path.replace("s3://", "").split("/")
            path = "/".join(l[1:])
            buffer = q3.download_file("us-ercot",path)
            files = process_buff_zipfile(buffer)
            for file in files:
                rtdfs.append(pd.read_csv(file))
        rtmdf = pd.concat(rtdfs)
        print(rtmdf)

        #get ancillary files and convert to dataframe
        ancdfs = []
        for path in ancillaryS3path:
            l = path.replace("s3://", "").split("/")
            path = "/".join(l[1:])
            buffer = q3.download_file("us-ercot",path)
            files = process_buff_zipfile(buffer)
            for file in files:
                ancdfs.append(pd.read_csv(file))
        ancillarydf = pd.concat(ancdfs)
        print(ancillarydf)

    return damdf, rtmdf, ancillarydf