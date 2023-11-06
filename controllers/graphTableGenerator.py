#implemented by Sierra
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta
import pytz
import requests
import controllers.predictionModel
import time
import psutil


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
    '''
        def timeConversion():
            registeredStartDate = datetime()
            for i in datetime: 
                dt = datetime.strptime(i,"%d:%m:%Y %H:%M:%S") # Stripped information from each row 
                
            #PDT_time = []  
            T = pd.Series(data=GMT) # Inputting GMT_time into a series 
            # Storing local dates and times into list  
            PDT_Date_time = []
            for i in local_Date_time: 
                dt_objects = i.to_pydatetime() # Turns the timestamps to datetime objects 
                PDT_Date_time.append(dt_objects)
            PDT_time = [] # official PDT time 
            for i in PDT_Date_time: # Takes time in 
                timediff = i.timestamp() - registeredStartDate.timestamp()
                PDT_time.append(timediff)
                
            print(PDT_Date_time[0])
            print(PDT_Date_time[0]- registeredStartDate)
            print(PDT_time[0])
            print(abs(df[selectedData].mean())**2)
            print(abs(np.mean(df[selectedData]))**2)
    '''
    #def upTime
    #def downTime
    def monitorWebsite(self, dataQ): #initially confirms whether the webpage is active or not
        r = requests.get(dataQ, timeout = 5)
        if r.status_code != 200:
            print ("Error: {} is unavailable")
        else:
            return True
        
    def upTime(self, dataQ):
        print('ggg')


    def latency(self, dataQ):
        last_received = psutil.net_io_counters(dataQ).bytes_recv
        last_sent = psutil.net_io_counters(dataQ).bytes_sent
        last_total = last_received + last_sent

        while True:
            bytes_received = psutil.net_io_counters(dataQ).bytes_recv
            bytes_sent = psutil.net_io_counters(dataQ).bytes_sent
            bytes_total = bytes_received + bytes_sent

            new_received = bytes_received + last_received
            new_sent = bytes_sent - last_sent
            new_total = bytes_total - last_total

            mb_new_received = new_received / 1024 / 1024
            mb_new_sent = new_sent / 1024 / 1024 
            mb_new_total = new_total / 1024 / 1024

            print(f"{mb_new_received:.2f} MB received")
            print(f"{mb_new_sent:.2f} MB sent")
            print(f"{mb_new_total:.2f} MB total")

            last_received = bytes_received
            last_sent = bytes_sent
            last_total = bytes_total

            time.sleep(15) #recounts every 15 seconds

            if False:
                print('Error: Latency Unavailable')

#need functions for uptime, downtime, and latency calculations
#response = requests.get()
#print(response.status_code) #gives the status of whether or not a website is active/inactive