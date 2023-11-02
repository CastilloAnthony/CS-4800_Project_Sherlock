import uuid
import time
import requests
from flask import Flask, render_template, request

class EditPreset(): # Controller
    def __init__(self, requestQ, dataQ):
        self.__requestQ, self.__dataQ = requestQ, dataQ

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
        presetRequest = {
            'id': uuid.uuid4(),
            'request_type': 'request',
            'column': 'presets', #Cannot get presets yet {'id': UUID('575b1827-40da-4141-b2fe-af951dd7a518'), 'timestamp': 1698523276.91872, 'data': 'Not Yet Implemented'}
            'query': {}
        }
        #SEND THIS OVER TO ALLOW USERS TO CHOOSE A PRESET TO BE ABLE TO EDIT IT
        temp = self.requestData(presetRequest)
        return temp
        
        
    def editPreset(self):
        #should return a list of presets wanted to be deleted
        print('I am here')
        preset_to_be_changed = request.form['selected_option']
        
        new_dictionary = {'name':'taco', 'presetLists':['www.google.com', 'chat.openai.com', 'www.bbc.co.uk']}
        presetRequest = {
            'id': uuid.uuid4(),
            'request_type': 'update',
            'column': 'presets', 
            'query': (preset_to_be_changed, new_dictionary)
        }
        #SEND THIS OVER TO ALLOW USERS TO CHOOSE A PRESET TO BE ABLE TO EDIT IT
        temp = self.requestData(presetRequest)
        return temp

    def editPreset1(self):
        self.query()
#end AddPreset