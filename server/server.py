# Created by Anthony Castillo
import time
import multiprocessing as mp
import socket
import numpy as np
from server.DBconnectionAgent import DBConnectionAgent
import client.client 
from controllers.predictionModel import PredictionModel # Temporary, testing
from controllers.graphGenerator import GraphGenerator
from uuid import uuid4

class Server(): # The main server handler class
    # Communicates with the MongoDB using DBconnection on behalf of the Clients using two multiprocessing.Queues 
    def __init__(self):
        """Initializes all attributes of the server class and calls the setupDBConnection function.
        """
        self.__DBconneciton = False # The connection agent
        self.__columns = ['masterList', 'pollingData', 'presets', 'users', 'auth'] # The "columns" in our SHERLOCK mongoDB. SHERLOCK['masterList']
        self.__requestTypes = ['insert', 'remove', 'request', 'update', 'setting'] # Types of requests the server can handle
        self.__httpPorts = [80, 443] # [HTTP, HTTPS] ports
        self.__pollingSpeed = 60/12 # The seconds between each master list poll
        self.__sampleSites = ['www.google.com', 'www.instagram.com', 'www.csustan.edu', 'www.microsoft.com', 'www.nasa.gov', 'chat.openai.com', 'www.bbc.co.uk', 'www.reddit.com', 'www.wikipedia.org', 'www.amazon.com'] # The sample of sites to use
        self.__requestsQ = mp.Queue(maxsize=1000000) # The request queue, only a clinet will put to this queue
        self.__dataQ = mp.Queue(maxsize=1000000) # The request queue, only the server will put to this queue
        self.__processes = {} # Process handles identifiers and handles for all processes created by the server
        self._setupDBConnection()

    def __del__(self): # WIP
        """Closes open processes and queues and destroys all attributes of the server class
        """
        for i in self.__processes:
            print('Process: '+i)
            print('\tIs Alive: '+str(self.__processes[i].is_alive()))
            if self.__processes[i].is_alive():
                print('\tJoined: '+str(self.__processes[i].join(timeout=3)==None))
                print('\tTerminated: '+str(self.__processes[i].terminate()==None))
                print('\tClosed: '+str(self.__processes[i].close()==None))
            else:
                try:
                    print('\tJoined: '+str(self.__processes[i].join(timeout=3)==None))
                    print('\tTerminated: '+str(self.__processes[i].terminate()==None))
                    print('\tClosed: '+str(self.__processes[i].close()==None))
                except:
                    print('\tClosed: '+str(self.__processes[i].close()==None))
        print('Queue: Request')
        print('\tClosed: '+str(self.__requestsQ.close()==None))
        print('\tJoined: '+str(self.__requestsQ.join_thread()==None))
        print('Queue: Data')
        print('\tClosed: '+str(self.__dataQ.close()==None))
        print('\tJoined: '+str(self.__dataQ.join_thread()==None))
        del self.__DBconneciton, self.__columns, self.__requestTypes, self.__httpPorts, self.__pollingSpeed, self.__sampleSites, self.__requestsQ, self.__dataQ, self.__processes
    
    def _checkForPresets(self):
        """Checks for the existence of the preset collection within the database and creates a default one if the collection could not be verified.
        """
        if self.__DBconneciton.verifyCollection('presets'):
            print('Presets collection verified.')
        else:
            print('Error in preset collection, rebuilding sample preset')
            samplePrest = {'name':'Sample Preset', 'user':'admin', 'timestamp':time.time(), 'data':[self.__sampleSites[0], self.__sampleSites[1], self.__sampleSites[2]]}
            self.sendToDB('presets', samplePrest)
            if self.__DBconneciton.verifyCollection('presets'):
                print('Preset collection was rebuilt successfully.')
            else:
                print('An unexpected error occured in the verification of the Preset collection.')

    def _checkForMasterlist(self):
        """Checks for the existence of the master list collection within the database and creates a default one if the collection could not be verified.
        """
        if self.__DBconneciton.verifyCollection('masterList'):
            print('Masterlist collection verified.')
        else:
            print('Error in masterlist, rebuilding the default masterlist.')
            self.__DBconneciton.clearDB('masterList')
            for i in self.__sampleSites:
                self.sendToDB('masterList', {'url':i, 'timestamp':time.time()})
            if self.__DBconneciton.verifyCollection('masterList'):
                print('Masterlist rebuilt successfully.')
            else:
                print('An unexpected error occured in the verification of the masterList.')

    def _checkForAuth(self):
        """Checks for the existence of the auth collection within the database and creates a default one if the collection could not be verified.
        """
        if self.__DBconneciton.verifyCollection('auth'):
            print('Auth collection verified.')
        else:
            print('Error in auth, rebuilding the default auth.')
            self.__DBconneciton.clearDB('Auth')

            self.sendToDB('auth', {'name': 'admin', 'email': 'admin@admin.com', 'id':1, 'password': 12345})

            self.sendToDB('auth', {'name': 'admin', 'email': 'admin@admin.com', 'id':str(uuid4()), 'password': 12345})
            if self.__DBconneciton.verifyCollection('auth'):
                print('Auth rebuilt successfully.')
            else:
                print('An unexpected error occured in the verification of auth.')

    def _checkForUsers(self):
        """Checks for the existence of the users collection within the database and creates a default one if the collection could not be verified.
        """
        if self.__DBconneciton.verifyCollection('users'):
            print('Users collection verified.')
        else:
            print('Error in users, rebuilding the default users.')
            self.__DBconneciton.clearDB('users')
            self.sendToDB('users', {'name':'admin', 'timestamp':time.time()})
            if self.__DBconneciton.verifyCollection('users'):
                print('Users rebuilt successfully.')
            else:
                print('An unexpected error occured in the verification of the users.')

    def _setupDBConnection(self, address="127.0.0.1", port="27017"):
        """Attempts to connect to the MongoDB at the specified address and port. Additionally, creates the SHERLOCK database if it doesn't exist and setups default collections for master list and preset

        Args:
            address (str, optional): The address for which the MongoDB is located. Defaults to "localhost".
            port (str, optional): The port number for which the MongoDB should be accessed from. Defaults to "27017".
        """
        self.__DBconneciton = DBConnectionAgent() # Maybe setup as a Daemon
        try:
            if self.__DBconneciton.connect(address, port):
                print("Successfully connected to DB at "+"mongodb://"+address+":"+port+"/")
                if self.__DBconneciton.useDB('SHERLOCK'):
                    print('Using the SHERLOCK database.')
                    self._checkForMasterlist()
                    self._checkForPresets()
                    self._checkForAuth()
                    self._checkForUsers()
                else:
                    print('Could not connect to the SHERLOCK database. Creating new one...')
                    self.__DBconneciton.createNewDB('SHERLOCK')
                    if 'SHERLOCK' in self.__DBconneciton.getDBs():
                        print('Successfully created new database.')
                        if self.__DBconneciton.useDB('SHERLOCK'):
                            print('Using the SHERLOCK database.')
                            self._checkForMasterlist()
                            self._checkForPresets()
                            self._checkForAuth()
                            self._checkForUsers()
                        else:
                            print('Could not connect to the new SHERLOCK database.')
                    else:
                        print('An Error occured while creating the new SHERLOCK database.')
            else:
                print("Unable to connect to DB at "+"mongodb://"+address+":"+port+"/")
        except:
            print('There was an error in connecting to MongoDB via ', address, ':', port)
            print('Aborting...')
            self.__del__()

    def setPollingSpeed(self, speed:int):
        """Sets the current polling speed, in seconds, that the server should wait before attempting to poll the URLs in the master list.

        Args:
            speed (int): The polling speed, in seconds, that the server will be set to

        Returns:
            bool: True/False on success/failure.
        """
        if isinstance(speed, int):
            self.__pollingSpeed = speed
            return True
        else:
            return False

    def getPollingSpeed(self):
        """Returns the current polling speed, in seconds, that the server waits before attempting to poll the URLs in the master list.

        Returns:
            integer: The current polling speed, in seconds, of the server
        """
        return self.__pollingSpeed
    
    def updateInDB(self, column:str, content:dict, changeTo:dict):
        """Updates a pre-existing document with new information

        Args:
            column (str): The specific collection to have its contents be updated
            content (dict): A dictionary containing the query to match with whats already in the database and content to replace the matched query with. FORMAT: {{query}, {modifications}}

        Returns:
            bool: True/False for success/failure to update data already existing in the database
        """
        if column in self.__columns:
            return self.__DBconneciton.updateInDB(column, content, changeTo)
        else:
            return False

    def sendToDB(self, column:str, content:dict):
        """Inserts a single dictionary into the database, formatted by the source of the dictionary. (Make sure everyone is inserting consistently.)

        Args:
            column (str): The specific collection to insert the data into 
            content (dict): The content being added into the collection

        Returns:
            bool: True/False on success/failure.
        """
        if column in self.__columns:
            return self.__DBconneciton.addToDB(column, content)
        else:
            return False

    def sendManyToDB(self, column:str, contents:dict): # WIP, Not used
        """_summary_

        Args:
            column (str): _description_
            contents (dict): _description_
        """
        pass

    def requestFromDB(self, column:str, query:dict):
        """Requests the first entry from the database in the specified collection that matches the given query. 

        Args:
            column (str): The specific collection to get data from
            query (dict): The content to match to in the database

        Returns:
            bool: True/False on success/failure.
        """
        if column in self.__columns:
            return self.__DBconneciton.requestFromDB(column, query)
        else:
            return False
    
    def requestManyFromDB(self, column:str, queries:dict):
        """Requests all entries within the database in the specified colleciton that matches the given query.

        Args:
            column (str): The specific collection to get data from
            queries (dict): The content to match to in the database

        Returns:
            bool: True/False on success/failure.
        """
        if column in self.__columns:
            return self.__DBconneciton.requestManyFromDB(column, queries)
        else:
                return False

    def removeFromDB(self, column:str, query:dict):
        """Removes the first entry from the database in the specified collection that matches the given query. 

        Args:
            column (str): The specific collection to remove data from
            query (dict): The content to match to in the database

        Returns:
            bool: True/False on success/failure.
        """
        if column in self.__columns:
            return self.__DBconneciton.removeFromDB(column, query)
        else:
            return False

    def removeManyFromDB(self, column:str, queries:dict):
        """Removes all entries from the database in the specified collection that matches the given query(queries).

        Args:
            column (str): The specific collection to remove data from
            queries (dict): The content to match to in the database

        Returns:
            bool: True/False on success/failure.
        """
        if column in self.__columns:
            return self.__DBconneciton.removeManyFromDB(column, queries)
        else:
            return False
    
    def _changeSettings(self, setting:str, changeTo):
        """Changes settings within the server. Currently supports changing the pollingSpeed

        Args:
            setting (str): The specific setting to be changed
            changeTo (int): The value to change the setting to

        Returns:
            bool: True/False on success/failure.
        """
        if setting == 'pollingSpeed':
                return self.setPollingSpeed(changeTo)
        else:
            return False

    def _checkForRequests(self):
        """This function is responsible for checking the requestsQ and responding to each request as is appropraite.
        """
        # Expected Request Formats # WIP
        #auth {'username':'Christian', 'email':'something@csustan.edu', 'id':uuid.uuid4(), 'password':'??????'}
        #users {'id':uuid.uuid4(), 'username':'Christian', 'email':'something@csustan.edu', 'websitesList':['www.google.com', 'www.csustan.edu'], 'presets':[{"name": "Christian", "presetLists": ["www.google.com", "www.csustan.edu", "www.microsoft.com", "www.nasa.gov"],"timestamp": 1698890950.1513646}, {"name": "Anthony", "presetLists": ["www.google.com", "www.instagram.com", "www.csustan.edu"], "timestamp": 1698890933.333366}]

        #{'id':uuid.uuid4(), 'timestamp':time.time(), 'request_type':'request', 'column':'masterList', 'query':{}}                                                               ### Gets all urls from the master list
        #{'id':uuid.uuid4(), 'timestamp':time.time(), 'request_type':'request', 'column':'pollingData', 'query':'wwww.google.com'}                                               ### Requests the polling data for a specific url
        #{'id':uuid.uuid4(), 'timestamp':time.time(), 'request_type':'request', 'column':'pollingData', 'query':['wwww.google.com', 'www.instgram.com', 'www.csustan.edu']}      ### Requests the polling data for a list of urls
        #{'id':uuid.uuid4(), 'timestamp':time.time(), 'request_type':'request', 'column':'pollingData', 'query':{'url':'wwww.google.com', 'timestamp':{$gte:time.time()-60*3}}}  ### Requests the polling data for a specified url with a timestamp greater tna or equal to the current timestamp - 3 minutes 
        #{'id':uuid.uuid4(), 'timestamp':time.time(), 'request_type':'insert', 'column':'masterList', 'query':'wwww.google.com'}                                                 ### Inserts a url into the masterList
        #{'id':uuid.uuid4(), 'timestamp':time.time(), 'request_type':'remove', 'column':'masterList', 'query':{url:'wwww.google.com'}}                                           ### Removes a url from the master list, be careful with this
        #{'id':uuid.uuid4(), 'timestamp':time.time(), 'request_type':'setting', 'column':'pollingSpeed', 'query':60}                                                             ### Changes the polling speed of the server. Query must be an integer
        # Additonal info: https://www.mongodb.com/docs/manual/reference/operator/query/#std-label-query-projection-operators-top
        while self.__requestsQ.empty() != True:
            newRequest = self.__requestsQ.get()
            if newRequest['request_type'] == 'request': # For requesting any data from the system
                if newRequest['column'] in 'masterList':
                    if newRequest['query'] == {}:
                        masterList = []
                        data = self.requestManyFromDB(newRequest['column'], newRequest['query'])
                        for doc in data:
                            masterList.append(doc['url'])
                        self.__dataQ.put({'id':newRequest['id'], 'timestamp':time.time(), 'data':masterList})
                    else:
                        self.__dataQ.put({'id':newRequest['id'], 'timestamp':time.time(), 'data':False})
                elif newRequest['column'] in 'pollingData':
                    if isinstance(newRequest['query'], list): # For a list of urls
                        tempData = []
                        for i in newRequest['query']:
                            tempData.append(self.requestManyFromDB(newRequest['column'], newRequest['query']))
                        self.__dataQ.put({'id':newRequest['id'], 'timestamp':time.time(), 'data':tempData})
                        del tempData
                    elif isinstance(newRequest['query'], dict):
                        self.__dataQ.put({'id':newRequest['id'], 'timestamp':time.time(), 'data':self.requestManyFromDB(newRequest['column'], newRequest['query'])})
                    elif isinstance(newRequest['query'], str): # For a single url
                        self.__dataQ.put({'id':newRequest['id'], 'timestamp':time.time(), 'data':self.requestManyFromDB(newRequest['column'], newRequest['query'])})
                    else:
                        self.__dataQ.put({'id':newRequest['id'], 'timestamp':time.time(), 'data':False})
                elif newRequest['column'] in 'presets':
                    if newRequest['query'] == {}:
                        self.__dataQ.put({'id':newRequest['id'], 'timestamp':time.time(), 'data':self.requestManyFromDB(newRequest['column'], newRequest['query'])})
                    elif isinstance(newRequest['query'], str):
                        self.__dataQ.put({'id':newRequest['id'], 'timestamp':time.time(), 'data':self.requestFromDB(newRequest['column'], newRequest['query'])})
                    elif isinstance(newRequest['query'], list):
                        tempData = []
                        for i in newRequest['query']:
                            tempData.append(self.requestManyFromDB(newRequest['column'], newRequest['query'][i]))
                        self.__dataQ.put({'id':newRequest['id'], 'timestamp':time.time(), 'data':tempData})
                        del tempData
                    elif isinstance(newRequest['query'], dict):
                        self.__dataQ.put({'id':newRequest['id'], 'timestamp':time.time(), 'data':'Not Yet Implemented'})
                elif newRequest['column'] in 'users':
                    if isinstance(newRequest['query'], dict):
                        self.__dataQ.put({'id':newRequest['id'], 'timestamp':time.time(), 'data':self.requestFromDB(newRequest['column'], newRequest['query'])})
                elif newRequest['column'] in 'auth':
                    self.__dataQ.put({'id':newRequest['id'], 'timestamp':time.time(), 'data':self.requestFromDB(newRequest['column'], newRequest['query'])})
                    #temp = self.requestFromDB(newRequest['column'], )
                    #if newRequest['query'] == '':
                        #if bcrypt.checkpw(newRequest['query']['password'], passwordcheck):
                    #else:
                        #self.__dataQ.put({'id':newRequest['id'], 'timestamp':time.time(), 'data':False})
                elif newRequest['column'] in self.__columns: # For all other requests
                    self.__dataQ.put({'id':newRequest['id'], 'timestamp':time.time(), 'data':'Not Yet Implemented'})
            elif newRequest['request_type'] == 'insert':
                if newRequest['column'] == 'masterList': # For url insertions into the master list
                    if self.requestFromDB('masterList', {'url':newRequest['query']}) == None:
                        self.__dataQ.put({'id':newRequest['id'], 'timestamp':time.time(), 'data':self.sendToDB(newRequest['column'], {'url':newRequest['query'], 'timestamp':time.time()})})
                    else:
                        self.__dataQ.put({'id':newRequest['id'], 'timestamp':time.time(), 'data':False})
                elif newRequest['column'] == 'presets':
                    self.__dataQ.put({'id':newRequest['id'], 'timestamp':time.time(), 'data':self.sendToDB(newRequest['column'], newRequest['query'])})
                elif newRequest['column'] == 'auth':
                    self.__dataQ.put({'id':newRequest['id'], 'timestamp':time.time(), 'data':self.sendToDB(newRequest['column'], newRequest['query'])})
                elif newRequest['column'] == 'users':
                    self.__dataQ.put({'id':newRequest['id'], 'timestamp':time.time(), 'data':self.sendToDB(newRequest['column'], newRequest['query'])})
                elif newRequest['column'] in self.__columns: # For all other insertions, might not be necessary (infact might not be good either)
                    self.__dataQ.put({'id':newRequest['id'], 'timestamp':time.time(), 'data':self.sendToDB(newRequest['column'], newRequest['query'])})
            elif newRequest['request_type'] == 'remove':
                if newRequest['column'] in self.__columns: # For all removals of data, might not be good, but works
                    self.__dataQ.put({'id':newRequest['id'], 'timestamp':time.time(), 'data':self.removeFromDB(newRequest['column'], newRequest['query'])})
            elif newRequest['request_type'] == 'setting': # For changing settings such as the polling speed of the server
                self.__dataQ.put({'id':newRequest['id'], 'timestamp':time.time(), 'data':self._changeSettings(newRequest['column'], newRequest['changeTo'])})
            elif newRequest['request_type'] == 'update':
                self.__dataQ.put({'id':newRequest['id'], 'timestamp':time.time(), 'data':self.updateInDB(newRequest['column'], newRequest['query'], newRequest['changeTo'])})
            else:
                self.__dataQ.put({'id':newRequest['id'], 'timestamp':time.time(), 'data':'Not Implemented'})

    def _clearDataQ(self):
        initial = None
        while not self.__dataQ.empty():
            tempData = self.__dataQ.get()
            print(tempData)
        '''
        while not self.__dataQ.empty():
            if initial == None:
                initial = self.__dataQ.get()
                while initial['timestamp'] < (time.time() - 60*1):
                    initial = self.__dataQ.get()
            tempData = self.__dataQ.get()
            print(tempData)
            if tempData == initial:
                self.__dataQ.put(tempData)
                break
            elif tempData['timestamp'] < (time.time() - 60*1):
                continue
            else:
                self.__dataQ.put(tempData)
        '''
        

    def _pollWebsites(self):
        """Funciton for requesting the masterlist from the database and for recording the latency for connections to each url in the masterlist. 
        """
        print(str(time.ctime())+' - Polling sites...')
        masterList = self.requestManyFromDB('masterList', {})
        for object in masterList:
            for port in self.__httpPorts:
                try:
                    latencyTimerStart = time.time()
                    temp = socket.create_connection((object['url'], port))
                    temp.close()
                    latencyTimerEnd = time.time()
                    self.sendToDB('pollingData', {'url':object['url'], 'port':port, 'timestamp':time.time(), 'up':True, 'latency':latencyTimerEnd-latencyTimerStart})
                    break
                except:
                    self.sendToDB('pollingData', {'url':object['url'], 'port':port, 'timestamp':time.time(), 'up':False, 'latency':np.nan})
    
    def _mainLoop(self):
        """The primary loop for the server, calls checkForRequests and pollWebsites.
        """
        #self.test()
        #self.test2()
        mainLoopTimerStart = 0 # We want to always poll site when the system first comes online
        dataQTimerStart = time.time()
        while True:
            self._checkForRequests()
            mainLoopTimerEnd = time.time()
            dataQTimerEnd = time.time()
            if (mainLoopTimerEnd-mainLoopTimerStart) >= self.__pollingSpeed:
                mainLoopTimerStart = time.time()
                self._pollWebsites()
            if (dataQTimerEnd-dataQTimerStart) >= 60:
                dataQTimerStart = time.time()
                self._clearDataQ()

    def startServer(self):
        """Creates the flask app in a separate processes, starts that process, and then intiates the mainloop. 
        """
        self.__processes['app'] = mp.Process(name ='Flask', target=client.client.startFlask, args=(self.__requestsQ, self.__dataQ))
        self.__processes['app'].start()
        self._mainLoop()

    def test(self):
        """Used for testing things at the start of the program
        """
        print('Begin test.')
        predModel = PredictionModel()
        data = self.requestManyFromDB('pollingData', {'url':'www.google.com'})
        tensorDataTime, tensorDataLatency = [], []
        for i in data:
            tensorDataTime.append(i['timestamp'])
            tensorDataLatency.append(i['latency'])
        tensorData = np.vstack((tensorDataTime, tensorDataLatency))
        print('Data gathered, transferring to PredictionModel...')
        predicitedData = predModel.predictOnData(tensorData)
        print('predictiedData =', predicitedData)
        print('length: ', len(predicitedData))
        print('Completed test.')
        
    def test2(self):
        graph = GraphGenerator()
        data = self.requestManyFromDB('pollingData', {'url':'www.google.com'})
        # add functions needed to generate graph from GenerateGraph
# end Server

def testServer():
    newServer = Server()
    #newServer._pollWebsites()
    #newServer.sendToDB('pollingData', {'website':'www.google.com', 'timestamp':time.ctime(), 'data':1035100})

if __name__ == '__main__':
    testServer()