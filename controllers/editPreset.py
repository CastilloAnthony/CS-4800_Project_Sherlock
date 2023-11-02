import uuid
import time
import requests
from flask import Flask, render_template, request
import json
import ast

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
        # duh = request.form['selected_option'].replace("'", "\"")
        # preset_to_be_changed = request.form.to_dict("selected_option")
        # preset_to_be_changed = request.form["selected_option"]
        input_string = "{'_id': ObjectId('6542ea752079dc2a9c74ca6c'), 'name': 'adfa', 'presetLists': ['www.csustan.edu', 'www.microsoft.com', 'www.nasa.gov', 'chat.openai.com'], 'timestamp': 1698884213.945767}"
        # print(type(preset_to_be_changed),'   ', preset_to_be_changed)
        # input_string = preset_to_be_changed
        print(type(input_string),input_string) 
        # Convert the string to a dictionary
        my_dict = ast.literal_eval(input_string)

        # Now, 'my_dict' is a Python dictionary
        print(my_dict)
        
        
        #RECKAGE
        # preset_to_be_changed = preset_to_be_changed['selected_option']
        # duh = "{'_id': ObjectId('653dae5111534f866611d128'), 'name': 'taco', 'presetLists': ['www.csustan.edu', 'www.microsoft.com'], 'timestamp': 1698541137.0775506}".replace("'", "\"")
        # preset_to_be_changed = json.loads(duh)# string by default has single quoutes and that is why no work :(
    
        
        #{'_id': ObjectId('653dae5111534f866611d128'), 'name': 'taco', 'presetLists': ['www.csustan.edu', 'www.microsoft.com'], 'timestamp': 1698541137.0775506}
        #HARD CODING
        new_dictionary = {'_id':preset_to_be_changed['_id'],'name':'taco', 'presetLists':['www.google.com', 'chat.openai.com', 'www.bbc.co.uk'], 'timestamp':preset_to_be_changed['timestamp']}
        
        presetRequest = {
            'id': uuid.uuid4(),
            'request_type': 'update',
            'column': 'presets', 
            'query': preset_to_be_changed,
            'changeTo':new_dictionary
        }
        #SEND THIS OVER TO ALLOW USERS TO CHOOSE A PRESET TO BE ABLE TO EDIT IT
        temp = self.requestData(presetRequest)
        return temp

    def editPreset1(self):
        self.query()
#end AddPreset