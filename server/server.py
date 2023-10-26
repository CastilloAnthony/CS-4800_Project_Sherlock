import time
import multiprocessing as mp
#import uuid
import socket
import numpy as np
from server.DBconnectionAgent import DBConnectionAgent
import app
#from clientListener import ClientListener

class Server(): # The main server handler class
    # Communicates with DB using DBconnection and Clients with clientManager
    def __init__(self):
        self.__DBconneciton = False # The connection agent
        self.__columns = ['masterList', 'pollingData', 'presets', 'users'] # The "columns" in our SHERLOCK mongoDB. SHERLOCK['masterList']
        self.__requestTypes = ['insert', 'remove', 'request', 'setting'] # Types of requests the server can handle
        self.__httpPorts = [80, 443] # [HTTP, HTTPS] ports
        self.__pollingSpeed = 60*1 # The seconds between each master list poll
        self.__sampleSites = ['www.google.com', 'www.instagram.com', 'www.csustan.edu', 'www.microsoft.com', 'www.nasa.gov', 'chat.openai.com', 'www.bbc.co.uk', 'www.reddit.com', 'www.wikipedia.org', 'www.amazon.com'] # The sample of sites to use
        self.__requestsQ = mp.Queue(maxsize=1000) # The request queue, only a clinet will put to this queue
        self.__dataQ = mp.Queue(maxsize=1000) # The request queue, only the server will put to this queue
        self.__processes = {} # Process handles identifiers and handles for all processes created by the server
        self._setupDBConnection()

    def __del__(self): # WIP
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

    def _checkForMasterlist(self):
        if self.__DBconneciton.verifyCollection('masterList'):
            print('Masterlist collection verified.')
        else:
            print('Error in masterlist, rebuilding the default masterlist.')
            self.__DBconneciton.clearDB('masterList')
            for i in self.__sampleSites:
                self.sendToDB('masterList', {'url':i})
            if self.__DBconneciton.verifyCollection('masterList'):
                print('Masterlist rebuilt successfully.')
            else:
                print('An unexpected error occured in the verification of the masterList.')

    def _setupDBConnection(self, address="localhost", port="27017"):
        self.__DBconneciton = DBConnectionAgent() # Maybe setup as a Daemon
        if self.__DBconneciton.connect(address, port):
            print("Successfully connected to DB at "+"mongodb://"+address+":"+port+"/")
            if self.__DBconneciton.useDB('SHERLOCK'):
                print('Using the SHERLOCK database.')
                self._checkForMasterlist()
            else:
                print('Could not connect to the SHERLOCK database. Creating new one...')
                self.__DBconneciton.createNewDB('SHERLOCK')
                if 'SHERLOCK' in self.__DBconneciton.getDBs():
                    print('Successfully created new database.')
                    if self.__DBconneciton.useDB('SHERLOCK'):
                        print('Using the SHERLOCK database.')
                        self._checkForMasterlist()
                    else:
                        print('Could not connect to the new SHERLOCK database.')
                else:
                    print('An Error occured while creating the new SHERLOCK database.')
        else:
            print("Unable to connect to DB at "+"mongodb://"+address+":"+port+"/")

    def setPollingSpeed(self, speed:int):
        if isinstance(speed, int):
            self.__pollingSpeed = speed
            return True
        else:
            return False

    def getPollingSpeed(self):
        return self.__pollingSpeed
    
    def sendToDB(self, column:str, content:dict):
        if column in self.__columns:
            self.__DBconneciton.addToDB(column, content)
        else:
            return False

    def sendManyToDB(self, column:str, contents:dict): # What would the format of 'contents' be for multiple inserts?
        pass

    def requestFromDB(self, column:str, query:dict):
        if column in self.__columns:
            return self.__DBconneciton.requestFromDB(column, query)
        else:
            return False
    
    def requestManyFromDB(self, column:str, queries:dict):
        if column in self.__columns:
            return self.__DBconneciton.requestManyFromDB(column, queries)
        else:
                return False

    def removeFromDB(self, column:str, query:dict):
        if column in self.__columns:
            return self.__DBconneciton.removeFromDB(column, query)
        else:
            return False

    def removeManyFromDB(self, column:str, queries:dict):
        if column in self.__columns:
            return self.__DBconneciton.removeManyFromDB(column, queries)
        else:
            return False

    def _changeSettings(self, setting:str, changeTo):
        if setting == 'pollingSpeed':
                return self.setPollingSpeed(changeTo)
        else:
            return False

    def _checkForRequests(self):
        # Expected Request Formats # WIP
        #{'id':uuid.uuid4(), 'request_type':'request', 'column':'masterList', 'query':{}}                                                               ### Gets all urls from the master list
        #{'id':uuid.uuid4(), 'request_type':'request', 'column':'pollingData', 'query':'wwww.google.com'}                                               ### Requests the polling data for a specific url
        #{'id':uuid.uuid4(), 'request_type':'request', 'column':'pollingData', 'query':['wwww.google.com', 'www.instgram.com', 'www.csustan.edu']}      ### Requests the polling data for a list of urls
        #{'id':uuid.uuid4(), 'request_type':'insert', 'column':'masterList', 'query':'wwww.google.com'}                                                 ### Inserts a url into the masterList
        #{'id':uuid.uuid4(), 'request_type':'remove', 'column':'masterList', 'query':{url:'wwww.google.com'}}                                           ### Removes a url from the master list, be careful with this
        #{'id':uuid.uuid4(), 'request_type':'setting', 'column':'pollingSpeed', 'query':60}                                                             ### Changes the polling speed of the server. Query must be an integer
        while self.__requestsQ.empty() != True:
            newRequest = self.__requestsQ.get()
            if newRequest['request_type'] == 'request': # For requesting any data from the system
                if newRequest['column'] in 'masterList':
                    self.__dataQ.put({'id':newRequest['id'], 'data':self.requestManyFromDBmDB(newRequest['column'], newRequest['query'])})
                elif newRequest['column'] in 'pollingData':
                    if isinstance(newRequest['query'], list): # For a list of urls
                        tempData = []
                        for i in newRequest['query']:
                            tempData.append(self.requestManyFromDB(newRequest['column'], newRequest['query']))
                        self.__dataQ.put({'id':newRequest['id'], 'data':tempData})
                        del tempData
                    elif isinstance(newRequest['query'], str): # For a single url
                        self.__dataQ.put({'id':newRequest['id'], 'data':self.requestManyFromDBmDB(newRequest['column'], newRequest['query'])})
                    else:
                        self.__dataQ.put({'id':newRequest['id'], 'data':False})
                elif newRequest['column'] in self.__columns: # For all other requests
                    self.__dataQ.put({'id':newRequest['id'], 'data':'Not Yet Implemented'})
            elif newRequest['request_type'] == 'insert':
                if newRequest['column'] == 'masterList': # For url insertions into the master list
                    self.__dataQ.put({'id':newRequest['id'], 'data':self.sendToDB(newRequest['column'], {'url':newRequest['query']})})
                elif newRequest['column'] in self.__columns: # For all other insertions, might not be necessary (infact might not be good either)
                    self.__dataQ.put({'id':newRequest['id'], 'data':self.sendToDB(newRequest['column'], newRequest['query'])})
            elif newRequest['request_type'] == 'remove':
                if newRequest['column'] in self.__columns: # For all removals of data, might not be good, but works
                    self.__dataQ.put({'id':newRequest['id'], 'data':self.removeFromDB(newRequest['column'], newRequest['query'])})
            elif newRequest['request_type'] == 'setting': # For changing settings such as the polling speed of the server
                self.__dataQ.put({'id':newRequest['id'], 'data':self._changeSettings(newRequest['column'], newRequest['changeTo'])})
            else:
                self.__dataQ.put({'id':newRequest['id'], 'data':False})

    def _pollWebsites(self):
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
        mainLoopTimerStart = 0 # We want to always poll site when the system first comes online
        while True:
            self._checkForRequests()
            mainLoopTimerEnd = time.time()
            if (mainLoopTimerEnd-mainLoopTimerStart) >= self.__pollingSpeed:
                mainLoopTimerStart = time.time()
                self._pollWebsites()

    def startServer(self):
        self.__processes['app'] = mp.Process(name ='Flask', target=app.startFlask, args=(self.__requestsQ, self.__dataQ))
        self.__processes['app'].start()
        self._mainLoop()
# end Server

def testServer():
    newServer = Server()
    #newServer._pollWebsites()
    #newServer.sendToDB('pollingData', {'website':'www.google.com', 'timestamp':time.ctime(), 'data':1035100})

if __name__ == '__main__':
    testServer()