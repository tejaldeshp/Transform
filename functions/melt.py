"""
This function melts the dataframe on parameters given
Input:  df- dataframe to be manipulated(type = dataframe)
        params- dict with keys: id_vars(type=list), value_vars(type=list)--(type=dict)
Output: dataframe
Call : df = melt(df,params)
"""

import pandas as pd

# params={
# "id_vars":["Node","Type", "Value"],
# "value_vars": ["HE 1","HE 2","HE 3","HE 4","HE 5","HE 6","HE 7","HE 8","HE 9","HE 10","HE 11","HE 12","HE 13","HE 14","HE 15","HE 16","HE 17","HE 18","HE 19",
# "HE 20","HE 21","HE 22","HE 23","HE 24"],
# "var_name":"hour",
# "value_name":"price"
# }

def melt(df, params):
    return df.melt(id_vars=params["id_vars"],value_vars=params["value_vars"], var_name = params["var_name"], value_name = params["value_name"])
