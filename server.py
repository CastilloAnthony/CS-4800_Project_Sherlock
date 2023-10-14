import time
import random
import socket # Networking stuff
import json # For transferring data between server and client
import uuid # Universally Unique IDentifier (For User IDs and others things)
import multiprocessing as mp # For concurrent processing (client requests, data retrival, etc.)
import pymongo # For communicating with the MongoDB

class Server(): # The main server handler class
    # Communicates with DB using DBconnection and Clients with clientManager
    def __init__(self):
        self.__DBconneciton = False
        self.__clientManager = False
        self.__q = mp.Queue(maxsize=100)
        print('Queue Size: '+str(self.__q.qsize()))
        self.__processes = {}
        self.__pipes = {}

    def __del__(self):
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
        del self.__DBconneciton
        del self.__clientManager

    def startDB(self):
        """Creates the database and/or sets up a conneciton agent to the database (Might not need)
        """
        #myclient = pymongo.MongoClient("mongodb://localhost:27017/")

    def setupConnection(self, address="localhost", port="27017"):
        self.__DBconneciton = DBConnectionAgent()
        if self.__DBconneciton.connect(address, port):
            print("Successfully connected to DB at "+"mongodb://"+address+":"+port+"/")
            self._startClientListener()
        else:
            print("Unable to connect to DB at "+"mongodb://"+address+":"+port+"/")
    
    def _startClientListener(self):
        #parent_ClientListenerPipe, child_ClientListenerPipe = mp.Pipe()
        self.__q = mp.Queue(3)
        #self.__pipes["ClientListener"] = parent_ClientListenerPipe
        self.__clientManager = ClientListener(self.__q)
        self.__processes["ClientListener"] = mp.Process(name="ClientListenerProcess", target=self.__clientManager._listen)
        self.__processes["ClientListener"].start()

    def pollWebsites(self):
        pass
    
    def mainLoop(self):
        pass
# end Server

class DBConnectionAgent():
    # Communicates directly with DB and Server
    def __init__(self):
        self.__client = False
        self.__db = False

    def __del__(self):
        self.disconnect()
        del self.__client
        del self.__db

    def connect(self, address="localhost", port="27017"):
        """Connects to a specified server

        Args:
            address (string): The IP Address of the server. Defaults to "localhost"
            port (string): The Port Number for the Server. Defaults to "27017"

        Returns:
            bool: Success/Failure to connect
        """
        try:
            self.__client = pymongo.MongoClient("mongodb://"+address+":"+port+"/")
            return True
        except:
            print("Could not connect to DB at: "+"mongodb://"+address+":"+port+"/")
            self.__client = False
            return False
        
    def disconnect(self):
        pass

    def getDBs(self):
        """Returns a List of databases for the connected system

        Returns:
            list: Returns a List of databases for the connected system in the format of ["admin", "config", "local"]
        """
        if self.__client != False:
            return self.__client.list_database_names()

    def useDB(self, db):
        """Sets the target DB

        Args:
            db (string): The DB to use, must be found inside of the getDBs() function

        Returns:
            bool: Success/Failure to use the specified DB
        """
        if db in self.getDBs():
            self.__db = self.__client[db]
            return True
        else:
            return False

    def addToDB(self, column:str, content:dict):
        """Adds data into the DB at the specified column

        Args:
            column (string): The column we wish to add data into
            content (dict): The content to add into the DB

        Returns:
            bool: Success/Failure to add content to the DB
        """
        if self.__db != False:
            try:
                self.__db[column].insert_one(content)
                return True
            except:
                return False
        else:
            return False

    def removeFromDB(self, column, query:dict):
        self.__db[column].delete_one(query)

    def removeManyFromDB(self, column, query:dict):
        self.__db[column].delete_many(query)

    def requestFromDB(self, column, query:dict):
        if self.__db != False:
            return self.__db[column].find_one(query)
    
    def requestManyFromDB(self, column, query:dict):
        if self.__db != False:
            return self.__db[column].find(query)

    def clearDB(self, column):
        self.__db[column].delete_many({})

    '''
    def insertPosts(self, post:dict):
        posts = self.__db.posts
        post_id = posts.insert_one(post).inserted_id
        print(post_id)

    def getPost(self, query:dict):
        return self.posts.find_one(query)
    '''
#end DBConnecitonAgent

class ClientListener():
    # Functions should use multiprocessing for optimized response time
    def __init__(self, queue):
        self.__knownClients = {}
        self.__processList = {}
        self.__q = queue

    def __del__(self):
        del self.__knownClients
        del self.__processList
        del self.__q

    def _listen(self):
        # Listens on port 77777
        x = 0
        while True:
            x = random.randint(0,10)
            print(x)
            try:
                self.__q.put(x, timeout=1)
                print('Inserted '+str(x)+' into queue.')
            except:
                print('Queue is full.')
            time.sleep(0.5)
            pass
            #self.__pipe.send(7)
        #self.__pipe.close()
        return

    def _verifyClient(self, client):
        if client in self.__knownClients:
            return True
        else:
            return False

    def _addClient(self, client):
        if not self._verifyClient(client):
            newClient = ClientInfo()
            newClient.setName("test")
            newClient.setAddress("1.2.3.4")
            newClient.setUUID(uuid.uuid4())
            self.__knownClients.append(newClient)

    def _ServerToClient(self, client):
        pass

    def _ClientToServer(self):
        pass

    def _processManager(self):
        pass
#end CLientListener

class ClientInfo():
    def __init__(self):
        self.__name = False
        self.__address = False
        self.__uuid = False

    def __del__(self):
        pass

    def setName(self, name):
        self.__name = name

    def setAddress(self, address):
        self.__address = address

    def setUUID(self, uuid):
        self.__uuid = uuid

    def getName(self):
        return self.__name
    
    def getAddress(self):
        return self.__address
    
    def getUUID(self):
        return self.__uuid
    
    def getInfo(self):
        return {"name":self.__name, "address":self.__address, "uuid":self.__uuid}
#end Client

def main():
    newServer = Server()
    newServer.startDB()
    newServer.setupConnection()

if __name__ == "__main__":
    main()
#end main