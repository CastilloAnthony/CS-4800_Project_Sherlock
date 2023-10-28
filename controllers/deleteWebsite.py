import uuid
import time
import requests
from flask import Flask, render_template, request

class DeleteWebsite(): # Controller
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
            print(newData)
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
        #return super().checkForData(masterListRequest)
        
    def deleteWebsite(self):
        websiteLists = request.form.getlist('selected_options[]') #WE HAVE THIS
        
        for website in websiteLists:
            removeWebsites = {
                'id': uuid.uuid4(),
                'request_type': 'remove',
                'column': 'masterList',
                'query': {"url":website}
            }
            #WE ARE SENDING IN AN INSERT REQUEST AFTER THIS WE WILL BE DONE
            #SIMPLY GIVE THEM A "YOUR THING HAS DELETED CORRECTLY AND BE ON WITH YOUR WAY"
            self.requestData(removeWebsites)