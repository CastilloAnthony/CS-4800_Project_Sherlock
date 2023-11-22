#CHRISTIAN
import uuid
import time
import requests
from flask import Flask, render_template, request
from controllers.queueManager import requestData

class DeleteWebsite(): # Controller
    def __init__(self, requestQ, dataQ):
        self.__requestQ, self.__dataQ = requestQ, dataQ
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
        """_summary_: asking for a certain document in users using email as query

        Returns:
            dict: contains the document with the corresponding email
        """
        #ASKING
        masterListRequest = {
            'id': uuid.uuid4(),
            'request_type': 'request',
            'column': 'users',#masterList
            'query': {"email":self.curr_email}
        }
        temp = requestData(masterListRequest, self.__requestQ, self.__dataQ)
        return temp
        
    def deleteWebsite(self):
        """_summary_: grab information from deleteWebsite.html which will come in form of a list of names 
                that correspond to fields in documents so we can disect and remove
        """ 
        websiteLists = request.form.getlist('selected_options[]') #WE HAVE THIS
        
        for website in websiteLists:
            removeWebsites = {
                'id': uuid.uuid4(),
                'request_type': 'remove',
                'column': 'users',
                'query': {'email':self.curr_email},
                'changeTo': {"websitesList":website}
                
            }
            #WE ARE SENDING IN AN INSERT REQUEST AFTER THIS WE WILL BE DONE
            #SIMPLY GIVE THEM A "YOUR THING HAS DELETED CORRECTLY AND BE ON WITH YOUR WAY"
            requestData(removeWebsites, self.__requestQ, self.__dataQ)