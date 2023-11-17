#CHRISTIAN
import uuid
import time
import requests
from flask import Flask, render_template, request
from bson import ObjectId

class AddPreset(): # Controller
    def __init__(self, requestQ, dataQ):
        self.__requestQ, self.__dataQ = requestQ, dataQ
        self.email = ''

    def __del__(self):
        pass

    def requestData(self, request):
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

    def query(self):
        #ASKING
        masterListRequest = {
            'id': uuid.uuid4(),
            'request_type': 'request',
            'column': 'masterList',
            'query': {}
        }
        temp = self.requestData(masterListRequest)
        return temp
        #requestQ.put(masterListRequest)
        #time.sleep(1) 
        #GRABBING
        #return super().checkForData(masterListRequest)7
    
    def getEmail(self, email):
        self.curr_email = email
    
    #FIGURE OUT HOW TO GRAB curr_email
    def getCurrentUser(self):
        """_summary_

        Returns:
            dict:   _id: mongoDB id
                    name: "name"
                    email: "email"
                    id: uuid.uuid4()
                    password: hashed password
        """
        # print(self.curr_email) 
        #ca
        
        grabAuthThroughEmail = {
            'id': uuid.uuid4(),
            'request_type': 'request',
            'column': 'auth',
            'query': {"email":self.curr_email}
        }
        temp = self.requestData(grabAuthThroughEmail)
        
        #temp = 
        # {'id': UUID('18938276-4528-4865-922d-d6f0673adab9'), 
        # 'timestamp': 1700172860.5806377, 
        # 'data': {'_id': ObjectId('65565326c3a6e4404edd07d8'), 
        # 'name': 'ca', 
        # 'email': 'ca', 
        # 'id': 'ee76936a-d4b0-4050-986d-b4a71041138b', 
        # 'password': b'$2b$12$YL/oMnZx4cbALMWonGfQ4.WruGxhp/N/RPd.f3i.rg7aZxyEkW8Qi'}
        # }
        return temp
        
        
        
    def addPreset(self):
        presetLists = request.form.getlist('selected_options[]') #WE HAVE THIS
        name = request.form['name'] #WE HAVE THIS
        #maybe once logged in client should send the email to each of the controllers
        
        parser = self.getCurrentUser()
        
        
        #GRAB OLD PRESETS LIST AND WE WANT TO ADD ON TO IT BY APPENDING THE PRESETSLISTS AS WELL AS NAME AND A LITTLE TIMESTAMP
        # userDictionary = {
        #     # 'id':parser['id'],
        #     # 'username':parser['name'],
        #     # 'email':parser['email'],
        #     'name': name,
        #     'presetLists': presetLists,
        #     'timestamp':time.time()
        # }
        
        
        identifier = parser['data']['id']
        print(identifier)
        #ee76936a-d4b0-4050-986d-b4a71041138b
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
            'query': {'id': identifier},#GOOD
            'changeTo':  {'presets':addition} #GOOD?
        }
        print(self.requestData(presetUpdate))
        # {'id': UUID('a846930f-60ab-40fd-adc0-9f1b5b6ece98'), 
        # 'timestamp': 1700172860.6941326, 
        # 'data': True}

    
#end AddPreset