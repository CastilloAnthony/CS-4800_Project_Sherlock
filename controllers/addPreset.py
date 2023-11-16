#CHRISTIAN
import uuid
import time
import requests
from flask import Flask, render_template, request

class AddPreset(): # Controller
    def __init__(self, requestQ, dataQ):
        self.__requestQ, self.__dataQ = requestQ, dataQ
        self.email = self.getEmail()

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
        return email
    
    #FIGURE OUT HOW TO GRAB curr_email
    def getCurrentUser(self, curr_email):
        """_summary_

        Args:
            curr_email (_type_): _description_

        Returns:
            dict:   _id: mongoDB id
                    name: "name"
                    email: "email"
                    id: uuid.uuid4()
                    password: hashed password
        """
        grabAuthThroughEmail = {
            'id': uuid.uuid4(),
            'request_type': 'request',
            'column': 'auth',
            'query': {"email":curr_email}
        }
        temp = self.requestData(grabAuthThroughEmail)
        
        return temp
        
        
        
    def addPreset(self):
        presetLists = request.form.getlist('selected_options[]') #WE HAVE THIS
        name = request.form['name'] #WE HAVE THIS
        #maybe once logged in client should send the email to each of the controllers
        parser = self.getCurrentUser(self.curr_email)
        
        
        userDictionary = {
            'id':parser['id'],
            'username':parser['name'],
            'email':parser['email'],
            'name': name,
            'presetLists': presetLists,
            'timestamp':time.time()
        }
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
        newPreset = {
            'id': uuid.uuid4(),
            'request_type': 'insert',
            'column': 'presets',
            'query': userDictionary
        }
        #WE ARE SENDING IN AN INSERT REQUEST AFTER THIS WE WILL BE DONE
        #SIMPLY GIVE THEM A "YOUR THING HAS INSERTED CORRECTLY AND BE ON WITH YOUR WAY"
        self.requestData(newPreset)

    
#end AddPreset