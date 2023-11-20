#CHRISTIAN Y ANTHONY
import uuid
import time
from flask import Flask, render_template, request
import numpy as np
from controllers.graphGenerator import GraphGenerator

class ViewWebsite():
    def __init__(self, requestQ, dataQ):
        self.__requestQ, self.__dataQ = requestQ, dataQ
        self.graph_generator = GraphGenerator(requestQ, dataQ)

    def __del__(self):
        del self.__requestQ, self.__dataQ

    def process_request(self, request):
        if request['request_type'] == 'request':
            response_data = self.requestData(request)

    def requestData(self, request):
        self.__requestQ.put(request)
        time.sleep(1)
        initialDataID = False
        while self.__dataQ.empty() != True:
            newData = self.__dataQ.get()
            if newData['id'] == initialDataID:
                self.__requestQ.put(request)
                #print(request['id'])
                time.sleep(1) #import time
                initialDataID = False
            elif initialDataID == False:
                initialDataID = newData['id']
            if newData['id'] == request['id']:
                if newData['data'] is not False:
                    return newData
            else:
                self.__dataQ.put(newData)

        def sendData(self, data):
            print(f"Received Data: {data}")

    def query1(self):
        #Modified by Anthony Castillo
        #ASKING
        """_summary_: essentially taking a bit of polled data and giving it in a formattable way 

        Returns:
            dict: dictionary 
                that contains each of the websites we have in 
                masterlist and trying to see the average latency over about a minute 
        """
        Request1 = {
            'id': uuid.uuid4(),
            'request_type': 'request',
            'column': 'masterList',
            'query': {}
        }
        temp1 = self.requestData(Request1)
        while temp1 == None:
            tempData = self.requestData(Request1)
            if tempData == None:
                tempData = self.requestData(Request1)
            elif tempData['data'] == None:
                tempData = self.requestData(Request1)
            else:
                temp1 = tempData
        
        #ASKING
        # {'id': UUID('36d8c82d-4a56-4860-8f71-aff5f350f45e'), 
        # 'timestamp': 1698420651.296685, 'data': ['www.google.com', 'www.instagram.com', 
        # 'www.csustan.edu', 'www.microsoft.com', 'www.nasa.gov', 'chat.openai.com', 'www.bbc.co.uk', 
        # 'www.reddit.com', 'www.wikipedia.org', 'www.amazon.com']}
        
        
        
        # ANTHONY CODE
        temp2 = {}
        for url in temp1['data']:
            tempNPArray = np.empty(1)
            Request2 = {
                'id': uuid.uuid4(),
                'request_type': 'request',
                'column': 'pollingData',
                'query':{'url':url, 'timestamp':{'$gte':time.time()-60}}
            }
            # {'www.google.com': 0.03995800018310547, 'www.instagram.com': 0.0375054677327474, 'www.csustan.edu': 0.03724519411722819, 
            # 'www.microsoft.com': 0.04232287406921387, 'www.nasa.gov': 0.02367687225341797, 'chat.openai.com': 0.034199535846710205, 
            # 'www.bbc.co.uk': 0.04925578832626343, 
            # 'www.reddit.com': 0.05298107862472534, 'www.wikipedia.org': 0.024207770824432373, 'www.amazon.com': 0.037099480628967285}
            tempUrl = self.requestData(Request2)
            while tempUrl == None:
                tempData = self.requestData(Request2)
                if tempData == None:
                    tempData = self.requestData(Request2)
                elif tempData['data'] == None:
                    tempData = self.requestData(Request2)
                else:
                    tempUrl = tempData
            
            for doc in tempUrl['data']:
                tempNPArray = np.append(tempNPArray, doc['latency'])
            
            temp2[url] = round(np.nanmean(tempNPArray), 4)
            
        return temp2 
    
    def query2(self):
        """_summary_: grab things from master list

        Returns:
            dict: uuid, id, data
        """
        #ASKING
        masterListRequest = {
            'id': uuid.uuid4(),
            'request_type': 'request',
            'column': 'masterList',
            'query': {}
        }
        temp = self.requestData(masterListRequest)
        return temp
    
    def viewWebsite(self):
        """_summary_: grabs url from html form then asks for respective data to that url in PollingData 
        Collection, from that, duration url and interval are given as parameters as well into generate_graph
        

        Returns:
            picture: returns picture or plot that will be rendered in client.py
        """
        url = request.form['selected_options[]']
        pollingDataRequest = {
            'id': uuid.uuid4(),
            'request_type': 'request',
            'column': 'pollingData',
            'query': {'url':url, 'timestamp':{'$gte':time.time()-60}}
        }
        data = self.requestData(pollingDataRequest)
        tensorDataTime, tensorDataLatency = [], []
        for i in data:
            tensorDataTime.append(i['timestamp'])
            tensorDataLatency.append(i['latency'])
        tensorData = np.vstack((tensorDataTime, tensorDataLatency))
        # constant for now but maybe later make a 
        duration = 300 
        interval = 15
        # gives me graph
        temp = self.graph_generator.generate_graph(tensorData, url, duration, interval)
        print(temp)
        return self.graph_generator.generate_graph(tensorData, url, duration, interval)

    def generateGraph(self, url, duration, interval):
        self.graph_generator.generate_graph(url, duration, interval)

    