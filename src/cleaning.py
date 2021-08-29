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
    move_and_delete = f"mv *.csv ./data/data_set.csv"
    return os.system(move_and_delete)

def nan(df):
    """takes a data frame and removes all nan rows and columns"""
    df.dropna(axis=0, how = "all",inplace=True)
    df.dropna(axis=1, how = "all",inplace=True)
    return df

def drop(df):
    """asks for user autorization to drop columns with scarse data"""
    percent_missing = round(df.isnull().sum() * 100 / len(df), 2)
    if input("drop poor data colums? [y/n] ")=="y":
        for c,n in zip(percent_missing.index,percent_missing.values):
            if n>70:
                df.drop([c], axis=1, inplace=True)
    return df


