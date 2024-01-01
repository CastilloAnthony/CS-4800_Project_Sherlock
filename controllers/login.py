import uuid
import time
from controllers.queueManager import requestData
class Login:
    def __init__(self, requestQ, dataQ):
        self.__requestQ, self.__dataQ = requestQ, dataQ
    
    def find_user_by_name(self, name): 
        """_summary_: find out if name is in dictionary

        Args:
            name (string): should be name of user input

        Returns:
            Bool: true or false depending on if database had it
        """
        #ASKING
        nameRequest = {
            'id': uuid.uuid4(),
            'request_type': 'request',
            'column': 'auth',
            'query': {"name":name}
        }
        temp = requestData(nameRequest, self.__requestQ, self.__dataQ)['data']
        return temp

    def find_user_by_email(self, email):
        """_summary_: find out if email is in dictionary

        Args:
            email (str): email that user inputted

        Returns:
            bool: true or false depending on if database has it
        """
        #ASKING
        emailRequest = {
            'id': uuid.uuid4(),
            'request_type': 'request',
            'column': 'auth',
            'query': {"email":email}
        }
        temp = requestData(emailRequest, self.__requestQ, self.__dataQ)['data']
        return temp

    def insert_user(self, auth_data):
        """_summary_: simply inserting the data into the database

        Args:
            user_data (dictionary): should be in form of {'name': user, 'email': email, 'id':uuid.uuid4(), 'password': hashed}
        """
        #ASKING
        insertAuthRequest = {
            'id': uuid.uuid4(),
            'request_type': 'insert',
            'column': 'auth',
            'query': auth_data
        }
        requestData(insertAuthRequest, self.__requestQ, self.__dataQ)
        
        #ADDING IN A USER DOCUMENT Should be like:
        #users {
        # 'id':uuid.uuid4(),
        # 'username':'Christian', 
        # 'email':'something@csustan.edu', 
        # 'websitesList':['www.google.com', 'www.csustan.edu'], 
        # 'presets':[
            # {"name": "Christian", "presetLists": ["www.google.com", "www.csustan.edu", "www.microsoft.com", "www.nasa.gov"],"timestamp": 1698890950.1513646}, 
            # {"name": "Anthony", "presetLists": ["www.google.com", "www.instagram.com", "www.csustan.edu"], "timestamp": 1698890933.333366}
        # ]
        #WHAT auth_data is:
        #{'name': user, 
        # 'email': email, 
        # 'id':str(uuid.uuid4()), 
        # 'password': hashed}
        parse = auth_data
        user_document = {
            'id': parse['id'],
            'username':parse['name'],
            'email': parse['email'],
            'websitesList':[],
            'presets':[]
        }
        #ASKING
        insertUserRequest = {
            'id': uuid.uuid4(),
            'request_type': 'insert',
            'column': 'users',
            'query': user_document
        }
        requestData(insertUserRequest, self.__requestQ, self.__dataQ)
        

        
    
    
    