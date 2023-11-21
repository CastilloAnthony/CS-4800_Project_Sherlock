#implemented by Sierra
#tested by Anthony
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import seaborn as sns
import datetime
from tzlocal import get_localzone  # Added import statement for tzlocal
import pytz
import requests
#from predictionModel import PredictionModel
from controllers.predictionModel import PredictionModel
import time
import uuid
import psutil
import io
import base64
import mpld3

class GraphGenerator:
    def __init__(self, requestQ, dataQ):
        self.__requestQ, self.__dataQ = requestQ, dataQ
        self.__predict = PredictionModel()

    #requestData implemented by Anthony
    def requestData(self, request):
        self.__requestQ.put(request)
        time = ()
        time.sleep(0.1)
        initialDataID = False
        selectedData = []
        while self.__dataQ.empty() != True:
            newData = self.__dataQ.get()
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
                
        def sendRequest (self, request):
            self.ViewWebsite.process_request(request)
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

    def timeConvert(self, dataQ):
       seconds = dataQ.timestamp()
       time_response = time.strftime('%m/%d/%y %H:%M:%S', time.localtime(seconds))
       
    # def monitorWebsite(self): #initially confirms whether the webpage is active or not
    #     listOfURLs = self.requestData({'id':uuid.uuid4(), 'timestamp':time.time(), 'request_type':'request', 'column':'masterList', 'query':{}}) #line implemented by Anthony
    #     r = requests.get(listOfURLs, timeout = 5)
    #     if r.status_code != 200:
    #         print ("Error: {} is unavailable".format(listOfURLs))
    #     else:
    #         return True

    '''
    def latency(self, dataQ, duration, interval):#C.A
        """_summary_

        Args:
            dataQ (_type_): _description_
            duration (_type_): _description_
            interval (_type_): _description_
        """
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
            
            return [bytes_received, bytes_sent, bytes_total]
    '''

    def generate_graph(self, tensorData, url, duration=300, interval=15):
        time_values, latency_values = tensorData[0], tensorData[1] #self.latency(psutil.net_io_counters(), duration, interval) #line implented by Anthony

        local_tz = get_localzone()
        #website_status = self.monitorWebsite(url)

        #sending tensorData to the prediction model
        #predictOnData(tensorData)

        #time_values = np.array([1,2,3])
        #latency_values = np.array([4,5,6])
        #foresight = self.predictOnData(tensorData, url= '')
        #foresight = self.predictOnData(tensorData, '', sampleRate='', epochs=[], predictions=[])
        
        #fig, ax = plt.subplots()
        #fig.autofmt_xdate() #line implemented by Anthony
        plt.figure(figsize=(16*0.65, 9*0.65))
        plt.plot(time_values.astype('datetime64[s]')-np.timedelta64(8, 'h'), latency_values * 100, label='Latency (ms)') #line altered by Anthony # WARNING: Hardcoded timedelta to be PST
        #plt.plot(foresight[0], foresight[1], label='Prediction (ms)')
        plt.ylabel('Latency (ms)')
        plt.gcf().axes[0].xaxis.set_major_locator(mdates.HourLocator(interval=6, tz=local_tz))
        plt.gcf().axes[0].xaxis.set_minor_locator(mdates.HourLocator(interval=1, tz=local_tz))
        plt.gcf().axes[0].xaxis.set_major_formatter(mdates.DateFormatter('%m/%d %H:%M')) #line implemented by Anthony
        plt.gcf().autofmt_xdate()
        plt.title('Latency and Website Monitoring of\n' + str(url) + "     (" + str(datetime.datetime.now()) + ")")
        plt.grid(True)
        plt.legend()
        plt.tight_layout()

        # if website_status:
        #     plt.axvline(x=datetime.datetime.now(), color='green', linestyle='--', label='Website UP')
        # else:
        #     plt.axvline(x=datetime.datetime.now(), color='red', linestyle='--', label='Website DOWN')

        #plt.text(datetime.datetime.now(), max(latency_values) * 0.9, f'Prediction: {foresight}', fontsize=12)
        #plt.text(datetime.datetime.now(), max(latency_values) * 0.9, fontsize=12)

        #plt.legend()
        #plt.show()
        img_buffer = io.BytesIO()
        plt.savefig(img_buffer, format='png')

        img_str = base64.b64encode(img_buffer.getvalue()).decode('utf-8')
        plt.close()
        
        #plot_html = mpld3.fig_to_html(fig)
    
        #return plot_html
        
        return img_str #line imnplemented by Christian 
        # image = plt #line altered by Anthony and Christian
        # return image #line implemented by Christian
        