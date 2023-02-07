import pandas as pd
from functions.skipRowCol import *
from functions.dfFilter import *
from functions.melt import *
from functions.datetimeCombine import *
from functions.dropCol import *
from functions.renameCol import *
from functions.pivot import *
from functions.addCol import *
from functions.addColsame import *


df = pd.read_csv("/home/tejaldeshpande/Desktop/DjangoProjects/Transform/TestFiles/miso/rawdata/20230101_asm_expost_damcp.csv", skiprows=4)
date = "2023/01/01"
node = "AECI"
add_dict={
  "date": date,
}
add_Col={
    "px_down":"GENREGMCP"
}
_skiprc={ 
    "skiprow" :[7],
    "skipcol" :[1]
}
_melt={
        "id_vars":["Unnamed: 0","MCP Type","date"],
        "value_vars": [" HE 1","HE 2","HE 3","HE 4","HE 5","HE 6","HE 7","HE 8","HE 9","HE 10","HE 11","HE 12","HE 13","HE 14","HE 15","HE 16","HE 17","HE 18","HE 19",
        "HE 20","HE 21","HE 22","HE 23","HE 24"],
        "var_name":"hour",
        "value_name":"price"
        }
_datetimeCombine={
        "dateCol":"date",
        "hourCol" :"hour",
        "minCol" :"",
        "format":"%Y/%m/%d",
        "hour_replace":"HE "
        }
_pivot={
    "values":["price"],
    "index": ["date","Unnamed: 0"],
    "columns": ["MCP Type"]
    }
_renameCol= {
        "Unnamed: 0" : "node",
        "GENREGMCP" : "px_up",
        "GENSPINMCP" : "px_spin",
        "GENSUPPMCP" : "px_nspin"
        }
_filter={
    "MCP Type" : ["GENREGMCP","GENSPINMCP","GENSUPPMCP"]
}

df = skipRowCol(df, _skiprc)
if node in df["Unnamed: 0"].values:
    df = df[df["Unnamed: 0"]==node]
else:
    df = df[df["Unnamed: 0"]=="MISO Wide"]
df = addCol(df, add_dict)
df = dfFilter(df, _filter)
df = melt(df, _melt)
df = datetimeCombine(df, _datetimeCombine)
df = pivot(df, _pivot)
df = addColsame(df,add_Col)
df = renameCol(df, _renameCol)
df.to_csv("ancillary.csv")