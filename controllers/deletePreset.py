import uuid
import time
import requests
from flask import Flask, render_template, request

class DeletePreset(): # Controller
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
            'column': 'presets', #Cannot get presets yet {'id': UUID('575b1827-40da-4141-b2fe-af951dd7a518'), 'timestamp': 1698523276.91872, 'data': 'Not Yet Implemented'}
            'query': {}
        }
        temp = self.requestData(masterListRequest)
        return temp
        #requestQ.put(masterListRequest)
        #time.sleep(1) 
        #GRABBING
        #return super().checkForData(masterListRequest)
        
    def deletePreset(self):
        #should return a list of presets wanted to be deleted
        deletedPresets = request.form.getlist('deletedPresets') 
        for preset in deletedPresets:
            deletePresetRequest = {
                'id': uuid.uuid4(),
                'request_type': 'remove',
                'column': 'presets',
                'query': preset
            }
            self.app.requestQ.put(deletePresetRequest)
            self.requestData(deletePresetRequest)

    
#end AddPreset