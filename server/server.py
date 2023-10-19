import time
import multiprocessing as mp
import uuid
import socket
from server.DBconnectionAgent import DBConnectionAgent
import app
#from clientListener import ClientListener

class Server(): # The main server handler class
    # Communicates with DB using DBconnection and Clients with clientManager
    def __init__(self):
        self.__DBconneciton = False
        self.__clientManager = False
        self.__columns = ['masterList', 'websiteData', 'users'] # The "columns" in our SHERLOCK mongoDB. SHERLOCK['masterList']
        self.__httpPorts = [80, 443] # [HTTP, HTTPS] ports
        self.__pollingSpeed = 3 # The seconds between each master list poll
        self.__sampleSites = ['www.google.com', 'www.instagram.com', 'www.csustan.edu', 'www.microsoft.com', 'www.nasa.gov', 'chat.openai.com', 'www.bbc.co.uk', 'www.reddit.com', 'www.wikipedia.org', 'www.amazon.com'] # The sample of sites to use
        self.__q = mp.Queue(maxsize=100)
        self.__requests = []
        print('Queue Size: '+str(self.__q.qsize()))
        self.__processes = {}
        self.__pipes = {}
        self._setupDBConnection()

    def __del__(self):
        del self.__DBconneciton
        del self.__clientManager
        time.sleep(10)
        for i in self.__pipes:
            print(self.__pipes[i].recv())
            self.__pipes[i].close()
        for i in self.__processes:
            print('Alive: '+str(self.__processes[i].is_alive()))
            #print('Terminated: '+str(self.__processes[i].terminate()))
            while not self.__q.empty():
                print('Pulled '+str(self.__q.get())+' from queue.')
                time.sleep(0.4)
            if self.__processes[i].is_alive():
                print('Terminated: '+str(self.__processes[i].terminate()))
                self.__q.close()
            print('Joined: '+str(self.__processes[i].join(timeout=3)))
            self.__processes[i].close()

    def _setupDBConnection(self, address="localhost", port="27017"):
        self.__DBconneciton = DBConnectionAgent() # Maybe setup as a Daemon
        if self.__DBconneciton.connect(address, port):
            print("Successfully connected to DB at "+"mongodb://"+address+":"+port+"/")
            if self.__DBconneciton.useDB('SHERLOCK'):
                print('Using the SHERLOCK database.')
            else:
                print('Could not connect to the SHERLOCK database. Creating new one...')
                self.__DBconneciton.createNewDB('SHERLOCK')
                if 'SHERLOCK' in self.__DBconneciton.getDBs():
                    print('Successfully created new database.')
                    if self.__DBconneciton.useDB('SHERLOCK'):
                        print('Using the SHERLOCK database.')
                        for i in self.__sampleSites:
                            self.sendToDB('masterList', {'website':i})
                    else:
                        print('Could not connect to the new SHERLOCK database.')
                else:
                    print('An Error occured while creating the new SHERLOCK database.')
        else:
            print("Unable to connect to DB at "+"mongodb://"+address+":"+port+"/")

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
        '''
        if column in self.__columns:
            newUUID = str(uuid.uuid4())
            self.__requests.append(newUUID)
            self.__processes[newUUID] = mp.Process(name ='Request'+newUUID, target=self.__DBconneciton.requestFromDBwithQ, args=[self.__q, column, query])
            self.__processes[newUUID].start()
        else:
            return False
        '''
        #self.__DBconneciton.addToDB(column, query)
    
    def requestManyFromDB(self, column:str, queries:dict):
        if column in self.__columns:
            return self.__DBconneciton.requestManyFromDB(column, queries)
        else:
                return False
        '''
        if column in self.__columns:
            newUUID = str(uuid.uuid4())
            #self.__processes[newUUID] = mp.Process(name ='Request'+newUUID, target=self.__DBconneciton.requestManyFromDBwithQ, args=[self.__q, column, queries])
            #self.__processes[newUUID].start()
        else:
            return False
        '''
        #self.__DBconneciton.addToDB(column, queries

    def _pollWebsites(self):
        #tempList = self.__DBconneciton.addToDB('masterList', {})
        #masterList = ['www.google.com', 'www.instagram.com', 'csustan.edu']
        masterList = self.requestManyFromDB('masterList', {})
        #print(masterList)
        for object in masterList:
            for port in self.__httpPorts:
                try:
                    start = time.time()
                    socket.create_connection((object['website'], port))
                    end = time.time()
                    #print('Latency to ', website+':'+str(i), str(end-start)+'ms')
                    self.sendToDB('websiteData', {'website':object['website'], 'port':port, 'timestamp':time.ctime(), 'up':True, 'latency':end-start})
                except:
                    self.sendToDB('websiteData', {'website':object['website'], 'port':port, 'timestamp':time.ctime(), 'up':False, 'latency':9999})
    
    def mainLoop(self):
        while True:
            self._pollWebsites()
            time.sleep(self.__pollingSpeed)

    def startServer(self):
        self.__processes['app'] = mp.Process(name ='Flask', target=app.startFlask)
        self.__processes['app'].start()
        self.mainLoop()
        
    def startDB(self):
        # NOT USED
        """Creates the database and/or sets up a conneciton agent to the database (Might not need)
        """
        #myclient = pymongo.MongoClient("mongodb://localhost:27017/")

    def _returnData(self):
        # Not USED
        data = self.__q.get()
        if data['ID'] in self.__requests:
            pass

    def _startClientListener(self):
        # DEPRECIATED
        #parent_ClientListenerPipe, child_ClientListenerPipe = mp.Pipe()
        self.__q = mp.Queue(3)
        #self.__pipes["ClientListener"] = parent_ClientListenerPipe
        #self.__clientManager = ClientListener(self.__q)
        self.__processes["ClientListener"] = mp.Process(name="ClientListenerProcess", target=self.__clientManager._listen)
        self.__processes["ClientListener"].start()
# end Server

def testServer():
    newServer = Server()
    #newServer._pollWebsites()
    #newServer.sendToDB('websiteData', {'website':'www.google.com', 'timestamp':time.ctime(), 'data':1035100})

if __name__ == '__main__':
    testServer()