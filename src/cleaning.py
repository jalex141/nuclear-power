import pandas as pd
import seaborn as sns
import numpy as np
import re
import os
import sys
sys.path.append('../')

def download_dataset():
    '''Downloads a dataset from kaggle and only keeps the csv in your data file. Beware of your own data structure:
    this creates a data directory and also moves all the .csv files next to your jupyter notebooks to it.
    Takes: url from kaggle
    Returns: a folder with the downloaded and unzipped csv
    '''
    
    #Gets the name of the dataset.zip
    url = input("Introduce la url: ")
    
    #Gets the name ofA the dataset.zip
    endopint = url.split("/")[-1]
    #endopint was already like this 
    user = url.split("/")[-2]
    
    #Download, decompress and leaves only the csv
    download = f"kaggle datasets download -d {user}/{endopint}"
    decompress = f"unzip *.zip"
    delete = f"rm -rf *.zip"
    #make_directory = "mkdir data"
    lista = "ls >> archivos.txt"
    
    for i in [download, decompress, delete, lista]:
        os.system(i)
    
    #Move the csv to uour data folder
    for file in list("./archivos.txt"):
        os.system(f"mv *.csv ./data/{file}")
        f"{file}>> archivos.txt"
    return None

#fix col names
def fix_col(df):
    """fixes column names so thet can be used in functions without issues"""
    diccio_todas = {col: col.replace(" ","_")  for col in list(df.columns)}
    df.rename(columns=diccio_todas, inplace=True)
    return df

def nan(df):
    """takes a dataframe and removes all nan rows and columns"""
    df.dropna(axis=0, how = "all",inplace=True)
    df.dropna(axis=1, how = "all",inplace=True)
    return df

def drop(df):
    """asks for user authorization to drop columns with scarse data"""
    percent_missing = round(df.isnull().sum() * 100 / len(df), 2)
    #this I borrowed from Mª Luisa, it makes a pd.serie with percentages of missing data
    if input("drop poor data colums? [y/n] ")=="y":
        t=int(input("Threshold [%] for data "))
        for c,n in zip(percent_missing.index,percent_missing.values):
            if n>t:
                df.drop([c], axis=1, inplace=True)
    return df

def date(df,df2):
    """merges with another data frame to get the date for every entry"""
    df2_d=df2[["MeetID","Date"]]
    df = df.merge(df2_d, on="MeetID")
    return df


def filna(df):
    """takes a dataframe and replaces all NaN values depending on the type of the column
    if type is  string or object replaces with UNK 
    if type is int or float returns -1"""
    col_n = list(df.select_dtypes(include="object").columns) 
    for col in list(df.columns):
        if col in col_n:
            df.fillna("UNK",inplace=True)
        else:
            df.fillna(0,inplace=True)
    return df

def division(df):
    """there are some divisions running simultaneously this gets rid of one of them"""
    pl_d=df["Division"]
    df.drop(["Division"], axis=1,inplace=True)
    df.drop_duplicates(inplace=True)
    #recover the division column
    df = df.merge(pl_d, left_index=True, right_index=True)
    return df

def stats_(df):
    """add relative to bodyweight stat columns"""
    df["Squat%"]= round(df.BestSquatKg / df.BodyweightKg,3)
    df["Bench%"]= round(df.BestBenchKg / df.BodyweightKg,3)
    df["Dead%"]= round(df.BestDeadliftKg / df.BodyweightKg,3)
    df["Total%"]= round(df.TotalKg / df.BodyweightKg,3)
    return df

def all_pos(df):
    """there are some negative numbers floating around which represent failed attempts,
     lets fix that"""
    for col in list(df.select_dtypes(include=["int64", "float64"]).columns) :
        df[col] = df[col].apply(lambda x: 0 if x<0 else x)
    return df

def fix_stat(df):
    """the dataframe I scrapped toguether forms nicely but with some weird entries,
     this remedies thet"""
    for col in list(df.columns.values):
        df[col] = df[col].apply(lambda x: float(re.search("(\d+.\d)",f"{x}")[0]))
    return df

#was not able to make this work, still..
def weight_groups(item):
    #distributes participants by weight
    l= item.split("@")
    t=float(str(l[0]))   ; a=l[1]; 
    if a== "F":
        if t < 49.4:
            return "lw_female_m"
        else:
            return "mhw_female_m"
    else:
        if t < 70.7:
            return "lw_male_m"
        elif t > 107.7:
            return "hw_male_m"
        else:
            return "mw_male_m"
