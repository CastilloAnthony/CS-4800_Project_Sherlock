import uuid
import time
import requests
from flask import Flask, render_template, request
import json
import ast
import re

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
        
    def parseStringToDict(self, stringedDictionary:str):
        # Define a regular expression pattern to match key-value pairs
        pattern = r"'(\w+)': (?:'([^']*)'|(?:\[(.*?)\])|(\d+\.\d+)|ObjectId\('([^']*)'\))"

        # Find all key-value pairs in the string
        matches = re.findall(pattern, stringedDictionary)

        # Create a dictionary from the matches
        data = {}
        for key, value_str, list_str, float_str, obj_id in matches:
            value = value_str if value_str else (list_str.split(', ') if list_str else (float(float_str) if float_str else obj_id))
            data[key] = value

        print("Data:",type(data), data)
        
        print("_id",type(data['_id']),data['_id'])
        print("name",type(data['name']),data['name'])
        print("presetLists",type(data['presetLists']),data['presetLists'])
        print("timestamp",type(data['timestamp']),data['timestamp'])
        
        return data
        
    def editPreset(self):
        #should return a list of presets wanted to be deleted
        print('I am here')
        preset_to_be_changed = request.form['selected_option[]']#.replace("'", "\"")
        preset_to_be_changed = self.parseStringToDict(preset_to_be_changed)
        
        # duh = "{'_id': ObjectId('653dae5111534f866611d128'), 'name': 'taco', 'presetLists': ['www.csustan.edu', 'www.microsoft.com'], 'timestamp': 1698541137.0775506}".replace("'", "\"")    
        #{'_id': ObjectId('653dae5111534f866611d128'), 'name': 'taco', 'presetLists': ['www.csustan.edu', 'www.microsoft.com'], 'timestamp': 1698541137.0775506}
        
        #HARD CODING
        new_dictionary = {'_id':preset_to_be_changed['_id'],'name':'taco', 'presetLists':['www.google.com', 'chat.openai.com', 'www.bbc.co.uk'], 'timestamp':preset_to_be_changed['timestamp']}
        
        presetRequest = {
            'id': uuid.uuid4(),
            'request_type': 'update',
            'column': 'presets', 
            'query': preset_to_be_changed,
            'changeTo': new_dictionary
        }
        #SEND THIS OVER TO ALLOW USERS TO CHOOSE A PRESET TO BE ABLE TO EDIT IT
        temp = self.requestData(presetRequest)
        return temp

    def editPreset1(self):
        self.query()
#end AddPreset