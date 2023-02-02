import os
import pandas as pd
from zipfile import ZipFile

#unzipping files on path
def process_zipfile(zip_file):
        """
        Returns a list of unzipped files from a zip file
        """
        result = []
        if zip_file.endswith(".zip"):
            zip_files = ZipFile(zip_file)
            zip_list = zip_files.infolist()
            for file in zip_list:
                result.append(zip_files.open(file))
        elif zip_file.endswith(".csv"):
            result.append(zip_file)
        return result

#gives a list of paths of csv files
def get_csvfile_path(csvpath):
    filelist =[]
    dirs = os.listdir(csvpath)
    dirs.sort()
    for d in dirs:
        if d == ".DS_Store":
            continue
        path =os.path.join(csvpath, d)
        zip_files = os.listdir(path)
        for zip_file in zip_files:
            unzipped_files = process_zipfile(os.path.join(path, zip_file))
            filelist=filelist+unzipped_files
    return filelist