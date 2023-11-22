#CHRISTIAN
import uuid
import time
import requests
from flask import Flask, render_template, request
from bson import ObjectId
from controllers.queueManager import requestData

class AddPreset(): # Controller
    def __init__(self, requestQ, dataQ):
        self.__requestQ, self.__dataQ = requestQ, dataQ
        self.email = ''

    def __del__(self):
        pass
    
    '''
    def requestData(self, request):
        """_summary_: in order to get the correct data and check for wrong insertions

        Args:
            request (dict): uuid, request_type, column, query, changeTo

        Returns:
            dict: uuid, id?,data
        """
        self.__requestQ.put(request)
        time.sleep(0.1)
        initialDataID = False
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
    '''

    def query(self):
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
        temp = requestData(masterListRequest, self.__requestQ, self.__dataQ)
        return temp
        #requestQ.put(masterListRequest)
        #time.sleep(1) 
        #GRABBING
        #return super().checkForData(masterListRequest)7
    
    def getEmail(self, email):
        """_summary_: simple get function for email which will be the key called in client.py

        Args:
            email (str): email that is learned from login
        """
        self.curr_email = email

    def addPreset(self):
        """_summary_: adding a preset given the information from the form in addPreset.html
        """
        presetLists = request.form.getlist('selected_options[]') #WE HAVE THIS
        name = request.form['name'] #WE HAVE THIS
        #maybe once logged in client should send the email to each of the controllers
        
        addition = {
                'name':name,
                'presetLists':presetLists,
                'timestamp':time.time()
            }
        
        presetUpdate = {
            #CHANGE WILL NEED TO BE INSERTED TO USERS
            #users {
            # 'id':uuid.uuid4(),
            # 'username':'Christian', 
            # 'email':'something@csustan.edu', 
            # 'websitesList':['www.google.com', 'www.csustan.edu'], 
            # 'presets':[
                # {"name": "Christian", "presetLists": ["www.google.com", "www.csustan.edu", "www.microsoft.com", "www.nasa.gov"],"timestamp": 1698890950.1513646}, 
                # {"name": "Anthony", "presetLists": ["www.google.com", "www.instagram.com", "www.csustan.edu"], "timestamp": 1698890933.333366}
            # ]
            'id': uuid.uuid4(),
            'request_type': 'update',
            'column': 'users', 
            #filter_criteria = {"_id": ObjectId("your-document-id")}
            'query': {'email': self.curr_email},#GOOD
            'changeTo':  {'presets':addition} #GOOD?
        }
        requestData(presetUpdate, self.__requestQ, self.__dataQ)
        # {'id': UUID('a846930f-60ab-40fd-adc0-9f1b5b6ece98'), 
        # 'timestamp': 1700172860.6941326, 
        # 'data': True}

    
#end AddPreset