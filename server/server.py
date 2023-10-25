import time
import multiprocessing as mp
#import uuid
import socket
from server.DBconnectionAgent import DBConnectionAgent
import app
#from clientListener import ClientListener

class Server(): # The main server handler class
    # Communicates with DB using DBconnection and Clients with clientManager
    def __init__(self):
        self.__DBconneciton = False # The connection agent
        self.__columns = ['masterList', 'websiteData', 'presets', 'users'] # The "columns" in our SHERLOCK mongoDB. SHERLOCK['masterList']
        self.__requestTypes = ['insert', 'remove', 'request'] # Types of requests the server can handle
        self.__httpPorts = [80, 443] # [HTTP, HTTPS] ports
        self.__pollingSpeed = 60*1 # The seconds between each master list poll
        self.__sampleSites = ['www.google.com', 'www.instagram.com', 'www.csustan.edu', 'www.microsoft.com', 'www.nasa.gov', 'chat.openai.com', 'www.bbc.co.uk', 'www.reddit.com', 'www.wikipedia.org', 'www.amazon.com'] # The sample of sites to use
        self.__requestsQ = mp.Queue(maxsize=1000) # The request queue, only a clinet will put to this queue
        self.__dataQ = mp.Queue(maxsize=1000) # The request queue, only the server will put to this queue
        self.__processes = {}
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
                print('An unexpected error occured.')

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
                        # for i in self.__sampleSites:
                        #     self.sendToDB('masterList', {'url':i})
                    else:
                        print('Could not connect to the new SHERLOCK database.')
                else:
                    print('An Error occured while creating the new SHERLOCK database.')
        else:
            print("Unable to connect to DB at "+"mongodb://"+address+":"+port+"/")

    def setPollingSpeed(self, speed:int):
        self.__pollingSpeed = speed

    def getPollingSpeed(self):
        return self.__pollingSpeed
    
    def sendToDB(self, column:str, content:dict):
        if column in self.__columns:
            self.__DBconneciton.addToDB(column, content)
        else:
            return False
            #newUUID = str(uuid.uuid4())
            #self.__processes[newUUID] = mp.Process(name ='SHERLOCK_Insert'+newUUID, target=self.__DBconneciton.addToDB, args=[column, content])
            #self.__processes[newUUID].start()
            #self.__DBconneciton.addToDB(column, content)

    def sendManyToDB(self, column:str, contents:dict): # What would the format of 'contents' be for multiple inserts?
        pass

    def requestFromDB(self, column:str, query:dict):
        if column in self.__columns:
            return self.__DBconneciton.requestFromDB(column, query)
        else:
            return False
        # if column in self.__columns:
        #     newUUID = str(uuid.uuid4())
        #     self.__requests.append(newUUID)
        #     self.__processes[newUUID] = mp.Process(name ='Request'+newUUID, target=self.__DBconneciton.requestFromDBwithQ, args=[self.__q, column, query])
        #     self.__processes[newUUID].start()
        # else:
        #     return False
        #self.__DBconneciton.addToDB(column, query)
    
    def requestManyFromDB(self, column:str, queries:dict):
        if column in self.__columns:
            return self.__DBconneciton.requestManyFromDB(column, queries)
        else:
                return False
        # if column in self.__columns:
        #     newUUID = str(uuid.uuid4())
        #     #self.__processes[newUUID] = mp.Process(name ='Request'+newUUID, target=self.__DBconneciton.requestManyFromDBwithQ, args=[self.__q, column, queries])
        #     #self.__processes[newUUID].start()
        # else:
        #     return False
        #self.__DBconneciton.addToDB(column, queries

    def _changeSettings(self, setting, changeTo):
        if setting == 'pollingSpeed':
            if isinstance(changeTo, int):
                self.__pollingSpeed = changeTo
                return True
            else:
                return False
        else:
            return False

    def _checkForRequests(self):
        #{'id':uuid.uuid4(), 'request_type':'insert', 'column':'masterList', 'query':'wwww.google.com'}
        while self.__requestsQ.empty() != True:
            newRequest = self.__requestsQ.get()
            if newRequest['request_type'] == 'request':
                if newRequest['column'] in self.__columns:
                    self.__dataQ.put({'id':newRequest['id'], 'data':self.__DBconneciton.requestFromDB(newRequest['column'], newRequest['query'])})
            elif newRequest['request_type'] == 'insert':
                if newRequest['column'] in self.__columns:
                    self.__dataQ.put({'id':newRequest['id'], 'data':self.__DBconneciton.addToDB(newRequest['column'], newRequest['query'])})
                    #self.__dataQ.put({'uuid':newRequest['id'], 'data':self.__DBconneciton.removeFromDB(newRequest['column'], newRequest['query'])})
            elif newRequest['request_type'] == 'remove':
                if newRequest['column'] in self.__columns:
                    self.__dataQ.put({'id':newRequest['id'], 'data':self.__DBconneciton.removeFromDB(newRequest['column'], newRequest['query'])})
                    #self.__dataQ.put({'uuid':newRequest['id'], 'data':self.__DBconneciton.removeFromDB(newRequest['column'], newRequest['query'])})
            elif newRequest['request_type'] == 'setting': #WIP
                self.__dataQ.put({'id':newRequest['id'], 'data':self._changeSettings(newRequest['setting'], newRequest['changeTo'])})
            else:
                self.__dataQ.put({'id':newRequest['id'], 'data':False})
            #self.sendToDB('masterList', {'url':self.__newSitesQ.get()})

    def _pollWebsites(self):
        print(str(time.ctime())+' - Polling sites...')
        #tempList = self.__DBconneciton.addToDB('masterList', {})
        #masterList = ['www.google.com', 'www.instagram.com', 'csustan.edu']
        #self._checkForRequests()
        masterList = self.requestManyFromDB('masterList', {})
        #print(masterList)
        for object in masterList:
            for port in self.__httpPorts:
                try:
                    latencyTimerStart = time.time()
                    temp = socket.create_connection((object['url'], port))
                    temp.close()
                    latencyTimerEnd = time.time()
                    #print('Latency to ', website+':'+str(i), str(end-start)+'ms')
                    self.sendToDB('websiteData', {'url':object['url'], 'port':port, 'timestamp':time.time(), 'up':True, 'latency':latencyTimerEnd-latencyTimerStart})
                except:
                    self.sendToDB('websiteData', {'url':object['url'], 'port':port, 'timestamp':time.time(), 'up':False, 'latency':9999})
    
    def _mainLoop(self):
        mainLoopTimerStart = 0 # We want to always poll site when the system first comes online
        while True:
            self._checkForRequests()
            mainLoopTimerEnd = time.time()
            if (mainLoopTimerEnd-mainLoopTimerStart) >= self.__pollingSpeed:
                mainLoopTimerStart = time.time()
                self._pollWebsites()
            #else:
                #time.sleep((self.__pollingSpeed)-(end-start))
            # addNewWebsites to DB

    def startServer(self):
        self.__processes['app'] = mp.Process(name ='Flask', target=app.startFlask, args=(self.__requestsQ, self.__dataQ))
        self.__processes['app'].start()
        self._mainLoop()
# end Server

def testServer():
    newServer = Server()
    #newServer._pollWebsites()
    #newServer.sendToDB('websiteData', {'website':'www.google.com', 'timestamp':time.ctime(), 'data':1035100})

if __name__ == '__main__':
    testServer()