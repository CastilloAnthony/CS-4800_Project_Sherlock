#CHRISTIAN
import uuid
import time
from flask import Flask, render_template, request
from bson import ObjectId
import re

class EditPreset(): # Controller
    def __init__(self, requestQ, dataQ):
        self.__requestQ, self.__dataQ = requestQ, dataQ
        self.old = []
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
        print(self.curr_email)
        userRequest = {
            'id': uuid.uuid4(),
            'request_type': 'request',
            'column': 'users', 
            'query': {"email":self.curr_email}
        }
        #SEND THIS OVER TO ALLOW USERS TO CHOOSE A PRESET TO BE ABLE TO EDIT IT
        temp = self.requestData(userRequest)
        if temp == None:
            return None
        else:
            # print(temp)
            return temp['data']
    
    def query1(self):
        #ASKING
        masterListRequest = {
            'id': uuid.uuid4(),
            'request_type': 'request',
            'column': 'masterList',
            'query': {}
        }
        temp = self.requestData(masterListRequest)
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
        
        data = self.remove_double_quotes(data)
        return data
    
    def remove_double_quotes(self, item):
        if isinstance(item, list):
            return [self.remove_double_quotes(element) for element in item]
        elif isinstance(item, dict):
            return {key: self.remove_double_quotes(value) for key, value in item.items()}
        elif isinstance(item, str):
            return item.replace('"', '').replace("'", '')  # Remove both double and single quotes
        else:
            return item
        
    def editPreset(self):
        #should return a list of presets
        
        preset_to_be_changed = request.form['selected_option[]']
        
        # print(preset_to_be_changed) #Big Ben: name of one of the presetLists
        preset_to_be_changed = self.parseStringToDict(preset_to_be_changed)
        print(preset_to_be_changed)
        self.old.append(preset_to_be_changed)
        #return this and on the next page show this up top as a reference to what it is currently
        
        return preset_to_be_changed        

    def editPreset1(self):
        preset_to_be_changed = self.old[0]
        # print(preset_to_be_changed)
        #GRAB THINGS USER WANTED TO CHANGE: NAME OR PRESETLIST
        urlList = request.form.getlist('selected_options[]') #WE HAVE THIS
        name = request.form['name'] #WE HAVE THIS
        newDictionary = {
            'name':name,
            'presetLists':urlList,
            'timestamp': time.time()
        }
        # I want to make it so when they give me a new name
        # and a new presetsList I will simply remove the old 
        # list, grab the new list, and insert the new list in for 
        # where the old list lived, I will do the same thing for 
        # name as well
        
        
        
        presetRequest = {
            'id': uuid.uuid4(),
            'request_type': 'update',
            'column': 'users', 
            #filter_criteria = {"_id": ObjectId("your-document-id")}
            'query': {'email':self.curr_email},
            'old': preset_to_be_changed,
            'changeTo': newDictionary
        }
        #SEND THIS OVER TO ALLOW USERS TO CHOOSE A PRESET TO BE ABLE TO EDIT IT
        temp = self.requestData(presetRequest)
        #reassigning self.old so that it will be fresh for next edit
        self.old = []
        return temp
#end AddPreset