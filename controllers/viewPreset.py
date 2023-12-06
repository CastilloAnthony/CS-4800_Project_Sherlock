#CHRISTIAN Y ANTHONY
import uuid
import time
from flask import Flask, render_template, request
import numpy as np
from controllers.graphGenerator import GraphGenerator
from controllers.queueManager import requestData
from controllers.editPreset import EditPreset

class ViewPreset():
    def __init__(self, requestQ, dataQ):
        self.__requestQ, self.__dataQ = requestQ, dataQ
        self.graph_generator = GraphGenerator(requestQ, dataQ)
        self.EditPreset = EditPreset(requestQ, dataQ)
        self.curr_email = ''

    def __del__(self):
        del self.__requestQ, self.__dataQ

    #def sendData(self, data): #line implemented by Sierra
        #print(f"Received Data: {data}")
    def getEmail(self, email):
        self.curr_email = email
        
    def query(self):
        """_summary_: grab things from master list

        Returns:
            dict: uuid, id, data
        """
        #ASKING
        masterListRequest = {
            'id': uuid.uuid4(),
            'request_type': 'request',
            'column': 'users',
            'query': {"email":self.curr_email}
        }
        temp = requestData(masterListRequest, self.__requestQ, self.__dataQ)
        if temp == None:
            return None
        else: return temp['data']
    
    def viewPreset(self):
        """_summary_: grabs preset from html form then asks for respective data to that url in PollingData 
        Collection, from that, duration url and interval are given as parameters as well into generate_graph
        

        Returns:
            picture: returns picture or plot that will be rendered in client.py
        """
        #This will be a stringed thing that looks like a dictionary
        presetStringedDict = request.form['selected_options[]']
        slider = int(request.form['slider'])
        
        #lets make it into a list
        presetDict = self.EditPreset.parseStringToDict(presetStringedDict)
        presetList = presetDict['presetLists']
        listOfWebsites = []
        #iterate through list of websites in presetList
        for i in presetList:
            pollingDataRequest = {
                'id': uuid.uuid4(),
                'request_type': 'request',
                'column': 'pollingData',
                'query': {'url':i, 'timestamp':{'$gte':time.time()-60*60*slider}}
            }
            data = requestData(pollingDataRequest, self.__requestQ, self.__dataQ)["data"] #line implented by Christian
            listOfWebsites.append(data)
        # constant for now but maybe later make variable
        duration = 300 
        interval = 15
        tensorList = []
        #iterate through list of dictionaries
        for data in listOfWebsites:
            tensorDataTime, tensorDataLatency = [], []
            for i in data:
                tensorDataTime.append(i['timestamp'])
                tensorDataLatency.append(i['latency'])
            tensorData = np.vstack((tensorDataTime, tensorDataLatency))
            tensorList.append(tensorData)
            
        #sending a list with tensorData, the url, duration, and interval
        temp = self.graph_generator.generateGraphs(tensorList, presetList, duration, interval)
        #temp = self.graph_generator.graphMulti(tensorList, presetList, duration, interval)
        return temp