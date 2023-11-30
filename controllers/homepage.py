#CHRISTIAN
import uuid
import time
import requests
from flask import Flask, render_template, request
from controllers.queueManager import requestData

class Homepage(): # Controller
    def __init__(self, requestQ, dataQ):
        self.__requestQ, self.__dataQ = requestQ, dataQ
        self.curr_email = ''

    def __del__(self):
        pass
    
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
        grabAuthThroughEmail = {
            'id': uuid.uuid4(),
            'request_type': 'request',
            'column': 'users',
            'query': {"email":self.curr_email}
        }
        temp = requestData(grabAuthThroughEmail, self.__requestQ, self.__dataQ)['data']['username']
        
        return temp
        
