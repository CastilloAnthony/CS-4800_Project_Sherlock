#CHRISTIAN
import uuid
import time
from flask import Flask, render_template, request
from bson import ObjectId
import re
from controllers.queueManager import requestData

class EditPreset(): # Controller
    def __init__(self, requestQ, dataQ):
        self.__requestQ, self.__dataQ = requestQ, dataQ
        self.old = []
        self.curr_email = ''

    def __del__(self):
        pass

    '''
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
    '''

    def getEmail(self, email):
        self.curr_email = email
    
    def query(self):
        """_summary_: want to grab everything from users specific document with query of email and then send over the data
            dwelling inside
        

        Returns:
            dict: contains either none if the thing is faulty for whatever reason or will return the data which is name, email, id, websites, presets
        """
        #ASKING
        userRequest = {
            'id': uuid.uuid4(),
            'request_type': 'request',
            'column': 'users', 
            'query': {"email":self.curr_email}
        }
        #SEND THIS OVER TO ALLOW USERS TO CHOOSE A PRESET TO BE ABLE TO EDIT IT
        temp = requestData(userRequest, self.__requestQ, self.__dataQ)
        if temp == None:
            return None
        else:
            return temp['data']
    
    def query1(self):
        """_summary_: simply making a request to the masterlist to grab all of the urls inside of it

        Returns:
            dict: uuid, timstamp, data; where data is all the documents in masterlist
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
        
    def parseStringToDict(self, stringedDictionary:str):
        """_summary_: We need this because forms loves to give us strings inside of the dictionary, it turns a string 
                        that should be a dictionary into a dictionary
        

        Args:
            stringedDictionary (str): it's as it sounds, it is a str that if printed looks exactly like a dictionary but is not

        Returns:
            dict: returns a dictionary from the string
        """
        # Define a regular expression pattern to match key-value pairs
        pattern = r"'(\w+)': (?:'([^']*)'|(?:\[(.*?)\])|(\d+\.\d+)|ObjectId\('([^']*)'\))"

        # Find all key-value pairs in the string
        matches = re.findall(pattern, stringedDictionary)

        # Create a dictionary from the matches
        data = {}
        for key, value_str, list_str, float_str, obj_id in matches:
            value = value_str if value_str else (list_str.split(', ') if list_str else (float(float_str) if float_str else obj_id))
            data[key] = value
        
        return self.remove_double_quotes(data)
    
    def remove_double_quotes(self, item):
        """_summary_: another problem with forms, it likes to make the list items inside of the form 
                        have quoutes like ["'taco'", "'burriot'"] so this fixxes that

        Args:
            item (dict): is a dictionary with odd quotation marks

        Returns:
            dict: with good quotation marks
        """
        if isinstance(item, list):
            return [self.remove_double_quotes(element) for element in item]
        elif isinstance(item, dict):
            return {key: self.remove_double_quotes(value) for key, value in item.items()}
        elif isinstance(item, str):
            return item.replace('"', '').replace("'", '')  # Remove both double and single quotes
        else:
            return item
        
    def editPreset(self):
        """_summary_: simply appends the dictionary to a list so we can use it later and then also return  it so it can be used in client.py

        Returns:
            dict: sending in what the user chose uptop so they can see the name and what they might want to keep
        """
        #should return a list of presets
        preset_to_be_changed = request.form['selected_option[]']
        
        preset_to_be_changed = self.parseStringToDict(preset_to_be_changed)
        
        self.old.append(preset_to_be_changed)
        
        #return this and on the next page show this up top as a reference to what it is currently
        return preset_to_be_changed        

    def editPreset1(self):
        """_summary_: we are grabbing what was given to us and making some queries and giving old 
                and new dictionaries so we have what we need to manipulate them in dbconnectionagent
        """
        preset_to_be_changed = self.old[0]
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
            'request_type': 'update2',
            'column': 'users', 
            #filter_criteria = {"_id": ObjectId("your-document-id")}
            'query': {'email':self.curr_email}, #the filter
            'old': {"presets": {"name": preset_to_be_changed['name']}},#what I want to remove
            'changeTo': {"presets":newDictionary} #what I want the new one to be
        }
        #SEND THIS OVER TO ALLOW USERS TO CHOOSE A PRESET TO BE ABLE TO EDIT IT
        requestData(presetRequest, self.__reqeustQ, self.__dataQ)
        #reassigning self.old so that it will be fresh for next edit
        self.old = []
        
#end AddPreset