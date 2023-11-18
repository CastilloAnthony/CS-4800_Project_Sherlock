#CHRISTIAN
import uuid
import time
import requests
from flask import Flask, render_template, request

class AddWebsite(): # Controller
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
        """_summary_

        Returns:
            dict:   _id: mongoDB id
                    name: "name"
                    email: "email"
                    id: uuid.uuid4()
                    password: hashed password
        """
        # print(self.curr_email) 
        #ca
        
        grabAuthThroughEmail = {
            'id': uuid.uuid4(),
            'request_type': 'request',
            'column': 'auth',
            'query': {"email":self.curr_email}
        }
        temp = self.requestData(grabAuthThroughEmail)
        #temp = 
        # {'id': UUID('18938276-4528-4865-922d-d6f0673adab9'), 
        # 'timestamp': 1700172860.5806377, 
        # 'data': {'_id': ObjectId('65565326c3a6e4404edd07d8'), 
        # 'name': 'ca', 
        # 'email': 'ca', 
        # 'id': 'ee76936a-d4b0-4050-986d-b4a71041138b', 
        # 'password': b'$2b$12$YL/oMnZx4cbALMWonGfQ4.WruGxhp/N/RPd.f3i.rg7aZxyEkW8Qi'}
        # }
        return temp
        
    def addWebsite(self):
        identifier = self.query()['data']['id']
        url = request.form['url']
        oneWebsite = {
            'id': uuid.uuid4(),
            'request_type': 'insert',
            'column': 'masterList',
            'query': url
        }
        self.__requestQ.put(oneWebsite)
        oneWebsite = {
            'id': uuid.uuid4(),
            'request_type': 'update',
            'column': 'users', 
            #filter_criteria = {"_id": ObjectId("your-document-id")}
            'query': {'id': identifier},#GOOD
            'changeTo':  {'websitesList':url} #GOOD?
        }
        self.__requestQ.put(oneWebsite)
            
#end AddPreset