import time
import multiprocessing as mp
import socket
import numpy as np
from server.DBconnectionAgent import DBConnectionAgent
import client.client 
import webbrowser

class Server(): # The main server handler class
    # Communicates with DB using DBconnection and Clients with clientManager
    def __init__(self):
        """_summary_
        """
        self.__DBconneciton = False # The connection agent
        self.__columns = ['masterList', 'pollingData', 'presets', 'users'] # The "columns" in our SHERLOCK mongoDB. SHERLOCK['masterList']
        self.__requestTypes = ['insert', 'remove', 'request', 'update', 'setting'] # Types of requests the server can handle
        self.__httpPorts = [80, 443] # [HTTP, HTTPS] ports
        self.__pollingSpeed = 60*1 # The seconds between each master list poll
        self.__sampleSites = ['www.google.com', 'www.instagram.com', 'www.csustan.edu', 'www.microsoft.com', 'www.nasa.gov', 'chat.openai.com', 'www.bbc.co.uk', 'www.reddit.com', 'www.wikipedia.org', 'www.amazon.com'] # The sample of sites to use
        self.__requestsQ = mp.Queue(maxsize=1000) # The request queue, only a clinet will put to this queue
        self.__dataQ = mp.Queue(maxsize=1000) # The request queue, only the server will put to this queue
        self.__processes = {} # Process handles identifiers and handles for all processes created by the server
        self._setupDBConnection()

    def __del__(self): # WIP
        """_summary_
        """
        for i in self.__processes:
            if self.__processes[i].is_alive():
                print('Process Alive: '+str(self.__processes[i].is_alive()))
                print('Joined: '+str(self.__processes[i].join(timeout=3)))
                print('Terminated: '+str(self.__processes[i].terminate()))
            else:
                print('Process Alive: '+str(self.__processes[i].is_alive()))
                print('Joined: '+str(self.__processes[i].join(timeout=3)))
            self.__processes[i].close()
        self.__requestsQ.close()
        while not self.__requestsQ.empty():
            print('Pulled '+str(self.__requestsQ.get())+' from queue.')
        self.__dataQ.close()
        while not self.__dataQ.empty():
            print('Pulled '+str(self.__dataQ.get())+' from queue.')
        del self.__DBconneciton, self.__columns, self.__requestTypes, self.__httpPorts, self.__pollingSpeed, self.__sampleSites, self.__requestsQ, self.__dataQ, self.__processes

    def _checkForPresets(self):
        """_summary_
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
        """_summary_
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

    def _setupDBConnection(self, address="127.0.0.1", port="27017"):
        """_summary_

        Args:
            address (str, optional): _description_. Defaults to "localhost".
            port (str, optional): _description_. Defaults to "27017".
        """
        self.__DBconneciton = DBConnectionAgent() # Maybe setup as a Daemon
        if self.__DBconneciton.connect(address, port):
            print("Successfully connected to DB at "+"mongodb://"+address+":"+port+"/")
            if self.__DBconneciton.useDB('SHERLOCK'):
                print('Using the SHERLOCK database.')
                self._checkForMasterlist()
                self._checkForPresets()
            else:
                print('Could not connect to the SHERLOCK database. Creating new one...')
                self.__DBconneciton.createNewDB('SHERLOCK')
                if 'SHERLOCK' in self.__DBconneciton.getDBs():
                    print('Successfully created new database.')
                    if self.__DBconneciton.useDB('SHERLOCK'):
                        print('Using the SHERLOCK database.')
                        self._checkForMasterlist()
                        self._checkForPresets()
                    else:
                        print('Could not connect to the new SHERLOCK database.')
                else:
                    print('An Error occured while creating the new SHERLOCK database.')
        else:
            print("Unable to connect to DB at "+"mongodb://"+address+":"+port+"/")

    def setPollingSpeed(self, speed:int):
        """_summary_

        Args:
            speed (int): _description_

        Returns:
            _type_: _description_
        """
        if isinstance(speed, int):
            self.__pollingSpeed = speed
            return True
        else:
            return False

    def getPollingSpeed(self):
        """_summary_

        Returns:
            _type_: _description_
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
            self.__DBconneciton.updateInDB(column, content, changeTo)
        else:
            return False

    def sendToDB(self, column:str, content:dict):
        """_summary_

        Args:
            column (str): _description_
            content (dict): _description_

        Returns:
            _type_: _description_
        """
        if column in self.__columns:
            self.__DBconneciton.addToDB(column, content)
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
        """_summary_

        Args:
            column (str): _description_
            query (dict): _description_

        Returns:
            _type_: _description_
        """
        if column in self.__columns:
            return self.__DBconneciton.requestFromDB(column, query)
        else:
            return False
    
    def requestManyFromDB(self, column:str, queries:dict):
        """_summary_

        Args:
            column (str): _description_
            queries (dict): _description_

        Returns:
            _type_: _description_
        """
        if column in self.__columns:
            return self.__DBconneciton.requestManyFromDB(column, queries)
        else:
                return False

    def removeFromDB(self, column:str, query:dict):
        """_summary_

        Args:
            column (str): _description_
            query (dict): _description_

        Returns:
            _type_: _description_
        """
        if column in self.__columns:
            return self.__DBconneciton.removeFromDB(column, query)
        else:
            return False

    def removeManyFromDB(self, column:str, queries:dict):
        """_summary_

        Args:
            column (str): _description_
            queries (dict): _description_

        Returns:
            _type_: _description_
        """
        if column in self.__columns:
            return self.__DBconneciton.removeManyFromDB(column, queries)
        else:
            return False
    
    def _changeSettings(self, setting:str, changeTo):
        """_summary_

        Args:
            setting (str): _description_
            changeTo (_type_): _description_

        Returns:
            _type_: _description_
        """
        if setting == 'pollingSpeed':
                return self.setPollingSpeed(changeTo)
        else:
            return False

    def _checkForRequests(self):
        """_summary_
        """
        # Expected Request Formats # WIP
        #{'id':uuid.uuid4(), 'timestamp':time.time(), 'request_type':'request', 'column':'masterList', 'query':{}}                                                               ### Gets all urls from the master list
        #{'id':uuid.uuid4(), 'timestamp':time.time(), 'request_type':'request', 'column':'pollingData', 'query':'wwww.google.com'}                                               ### Requests the polling data for a specific url
        #{'id':uuid.uuid4(), 'timestamp':time.time(), 'request_type':'request', 'column':'pollingData', 'query':['wwww.google.com', 'www.instgram.com', 'www.csustan.edu']}      ### Requests the polling data for a list of urls
        #{'id':uuid.uuid4(), 'timestamp':time.time(), 'request_type':'insert', 'column':'masterList', 'query':'wwww.google.com'}                                                 ### Inserts a url into the masterList
        #{'id':uuid.uuid4(), 'timestamp':time.time(), 'request_type':'remove', 'column':'masterList', 'query':{url:'wwww.google.com'}}                                           ### Removes a url from the master list, be careful with this
        #{'id':uuid.uuid4(), 'timestamp':time.time(), 'request_type':'setting', 'column':'pollingSpeed', 'query':60}                                                             ### Changes the polling speed of the server. Query must be an integer
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

    def _pollWebsites(self):
        """_summary_
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
        """_summary_
        """
        mainLoopTimerStart = 0 # We want to always poll site when the system first comes online
        homepage = "http://127.0.0.1:7777"
        time.sleep(3)
        webbrowser.open(homepage)
        while True:
            self._checkForRequests()
            mainLoopTimerEnd = time.time()
            if (mainLoopTimerEnd-mainLoopTimerStart) >= self.__pollingSpeed:
                mainLoopTimerStart = time.time()
                self._pollWebsites()

    def startServer(self):
        """_summary_
        """
        self.__processes['app'] = mp.Process(name ='Flask', target=client.client.startFlask, args=(self.__requestsQ, self.__dataQ))
        self.__processes['app'].start()
        self._mainLoop()
# end Server

def testServer():
    newServer = Server()
    #newServer._pollWebsites()
    #newServer.sendToDB('pollingData', {'website':'www.google.com', 'timestamp':time.ctime(), 'data':1035100})

if __name__ == '__main__':
    testServer()