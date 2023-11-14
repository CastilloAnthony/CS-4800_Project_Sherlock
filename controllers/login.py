import bcrypt
import uuid
import time



class Login:
    def __init__(self, requestQ, dataQ):
        self.__requestQ, self.__dataQ = requestQ, dataQ
    
    def requestData(self, request):
        """_summary_: returns data or returns a not good query message

        Args:
            request (dict): specifies uuid, request type, where to query, and query

        Returns:
            dict: returns wanted data
        """
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
    
    #HELPER FUNCTIONS
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
            'column': 'users',
            'query': {"name":name}
        }
        temp = self.requestData(nameRequest)
        some_shit = int# or something idk
        if isinstance(temp, some_shit):
            pass
        else: 
            return temp
        return self.mycol.find_one({"name": name})

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
            'column': 'users',
            'query': {"email":email}
        }
        temp = self.requestData(emailRequest)
        some_shit = int# or something idk
        if isinstance(temp, some_shit):
            pass
        else: 
            return temp

    def insert_user(self, user_data):
        """_summary_: simply inserting the data into the database

        Args:
            user_data (dictionary): should be in form of {'name': user, 'email': email, 'id':uuid.uuid4(), 'password': hashed}
        """
        #ASKING
        insertUserRequest = {
            'id': uuid.uuid4(),
            'request_type': 'insert',
            'column': 'users',
            'query': {user_data}
        }
        self.requestData(insertUserRequest)
        
    
    
    