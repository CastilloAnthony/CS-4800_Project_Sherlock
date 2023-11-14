import bcrypt
import uuid
import time
#ERROR: tensorflow-1.0.1-py2-none-any.whl is not a supported wheel on this platform.


# python3 -m pip install --upgrade https://storage.googleapis.com/tensorflow/mac/cpu/tensorflow-1.12.0-py3-none-any.whl
#ERROR: Could not install packages due to an OSError: [Errno 2] No such file or directory: 'C:\\Users\\Christian Alameda\\AppData\\Local\\Packages\\PythonSoftwareFoundation.Python.3.10_qbz5n2kfra8p0\\LocalCache\\local-packages\\Python310\\site-packages\\tensorflow\\include\\external\\aws\\aws-cpp-sdk-kinesis\\include\\aws\\kinesis\\model\\DecreaseStreamRetentionPeriodRequest.h'
#HINT: This error might have occurred since this system does not have Windows Long Path support enabled. You can find information on how to enable this at https://pip.pypa.io/warnings/enable-long-paths
# https://pip.pypa.io/warnings/enable-long-paths
# New-ItemProperty -Path "HKLM:\SYSTEM\CurrentControlSet\Control\FileSystem" `
# -Name "LongPathsEnabled" -Value 1 -PropertyType DWORD -Force
class Login:
    def __init__(self):
        pass
    
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
        
    
    
    