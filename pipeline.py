import pandas as pd
import sys
sys.path.append('../')
import src.cleaning as cl

#import data from kaggle
#cl.download_dataset()

#load datasets
pl = pd.read_csv('./data/openpowerlifting.csv',encoding="ISO-8859-1")
m = pd.read_csv('./data/meets.csv',encoding="ISO-8859-1")

#fix column names
cl.fix_col(pl)

#dron NaN columns and rows
cl.nan(pl)

#Drop columns with scarce data
cl.drop(pl)

#remove simultaneous division entries
cl.division(pl)

#merge date from another data frame 
cl.date(pl,m)

#fill NaN acording to dtype
cl.filna(pl)

#export data frame
pl.to_csv ('./output/pl.csv',index=False)

#add columns with relative values
cl.stats_(pl)

#negative numbers are failed attempts
cl.all_pos(pl)

#export clean dataframe
pl.to_csv ('./output/pl.csv', index=False)