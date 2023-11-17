#CHRISTIAN
import uuid
import time
import requests
from flask import Flask, render_template, request

class DeletePreset(): # Controller
    def __init__(self, requestQ, dataQ):
        self.__requestQ, self.__dataQ = requestQ, dataQ
        self.curr_email = ''
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
    
    def getEmail(self, email):
        self.curr_email = email
        
    def query(self):
        #ASKING
        masterListRequest = {
            'id': uuid.uuid4(),
            'request_type': 'request',
            'column': 'users',#masterList
            'query': {"email":self.curr_email}
        }
        #print('something who cares')
        temp = self.requestData(masterListRequest)
        return temp
        #{'id': UUID('2cfd8df6-d169-4342-81d7-49c74ecb610d'), 
        # 'timestamp': 1700183925.3842254, 
        # 'data': {'_id': ObjectId('65565327c3a6e4404edd07d9'), 'id': 'ee76936a-d4b0-4050-986d-b4a71041138b', 'username': 'ca', 'email': 'ca', 'websitesList': ['https://www.youtube.com/watch?v=fU-hbVHNrzo'], 'presets': [{'name': 'ca', 'presetLists': ['www.google.com', 'www.instagram.com'], 'timestamp': 1700173818.6764941}, {'name': 'taco', 'presetLists': ['www.google.com', 'www.instagram.com', 'www.csustan.edu'], 'timestamp': 1700174609.7962203}, {'name': 'Big Ben', 'presetLists': ['www.google.com', 'www.instagram.com', 'chat.openai.com', 'www.reddit.com'], 'timestamp': 1700174848.542619}]
        #           }
        # }
        
    def deletePreset(self):
        #should return a list of presets wanted to be deleted
        deletedPresets = request.form.getlist('selected_options[]') 
        print(deletedPresets)
        for preset in deletedPresets:
            deletePresetRequest = {
                'id': uuid.uuid4(),
                'request_type': 'remove',
                'column': 'users',
                'query': {'email':self.curr_email},
                'changeTo': {"presets": {"name": preset}}# preset == ca
            }
            self.requestData(deletePresetRequest)

    
#end AddPreset