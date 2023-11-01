import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta
import pytz
import requests
import predictionModel

class graphTableGenerator:
    def __init__(self, requestQ, dataQ):
        self.__requestQ, self.__dataQ = requestQ, dataQ

    def requestData(self, request):
        self.__requestQ.put(request)
        time.sleep(0.1)
        initialDataID = False
        while self.__dataQ.empty() != True:
            newData = self.__dataQ.get()
            print(newData)
            if newData['id'] == initialDataID:
                self.__requestQ.put(request)
                time.sleep(0.1) #import time
                initialDataID = False
            elif initialDataID == False:
                initialDataID = newData['id']
            if newData['id'] == request['id']:
                if newData['data'] is not False:
                    return newData
            else:
                self.__dataQ.put(newData)


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
#response = requests.get()
#print(response.status_code) #gives the status of whether or not a website is active/inactive
