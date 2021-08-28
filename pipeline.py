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
