import pandas as pd
import seaborn as sns
import numpy as np
import re
import os
import sys
sys.path.append('../')
import src.cleaning as cl

#import data from kaggle
cl.download_dataset()

#load dataset
pl = pd.read_csv('./data/openpowerlifting.csv',encoding="ISO-8859-1")

cl.nan(pl)
cl.drop(pl)