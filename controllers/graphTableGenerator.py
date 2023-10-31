import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta
import pytz
import requests
from server import DBconnectionAgent

filename = 'gg'

#load files
#need function to read requested websites from database
#class DBconnectionAgent:
    #self. 

#df = pd.read_#
#for index, websites in df.iterrows():
##
#print(df)

#initialize timestamp
#format for timestamp function: ??

#need functions for uptime, downtime, and latency calculations
response = requests.get()
print(response.status_code) #gives the status of whether or not a website is active/inactive
