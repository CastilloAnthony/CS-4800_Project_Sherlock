import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta
import pytz
import requests
import controllers.predictionModel

class graphTableGenerator:
    def __init__(self, requestQ, dataQ):
        self.__requestQ, self.__dataQ = requestQ, dataQ

    def requestData(self, request):
        self.__requestQ.put(request)
        time = ()
        time.sleep(0.1)
        initialDataID = False
        selectedData = []
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
                print(len(newData))

            # have the requested data print out in a list
    
    def timeConversion():
        registeredStartDate = datetime()
        GMT = [] # This our GMT_time 
        for i in datetime: 
            dt = datetime.strptime(i,"%d:%m:%Y %H:%M:%S") # Stripped information from each row 
            GMT.append(dt)   
            
        # Convert GMT to Local Time

        #PDT_time = []  
        T = pd.Series(data=GMT) # Inputting GMT_time into a series 

        # Converts GMT Dates and Times to Pacific Daylight Savings Time 
        local_Date_time = T.dt.tz_localize('GMT').dt.tz_convert('America/Los_Angeles').dt.tz_localize(None) # This line converts time_zones

        # Storing local dates and times into list  
        PDT_Date_time = []
        for i in local_Date_time: 
            dt_objects = i.to_pydatetime() # Turns the timestamps to datetime objects 
            PDT_Date_time.append(dt_objects)
            
        # Find the total seconds starting the week of april 4th 

        PDT_time = [] # official PDT time 

        for i in PDT_Date_time: # Takes time in 
            
            timediff = i.timestamp() - registeredStartDate.timestamp()
            
            PDT_time.append(timediff)
            
        print(PDT_Date_time[0])
        print(PDT_Date_time[0]- registeredStartDate)
        print(PDT_time[0])
        print(abs(df[selectedData].mean())**2)
        print(abs(np.mean(df[selectedData]))**2)




#need functions for uptime, downtime, and latency calculations
#response = requests.get()
#print(response.status_code) #gives the status of whether or not a website is active/inactive
