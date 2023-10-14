#import mysql.connector # For database, unless we use MongoDB
#import sql # For transferring data between server and client
import uuid # Universally Unique IDentifier (For User IDs and others things)
import multiprocessing # For concurrent processing (client requests, data retrival, etc.)
import pymongo

class Server(): # The main server handler class
    # Communicates with DB using DBconnection and Clients with clientManager
    def __init__(self):
        self.__DBconneciton = False
        self.__clientManager = False

    def __del__(self):
        del self.__DBconneciton
        del self.__clientManager

    def startDB(self):
        """Creates the database and then sets up a conneciton agent
        """
        myclient = pymongo.MongoClient("mongodb://localhost:27017/")

    def setupConnection(self, address="localhost", port="27017"):
        self.__DBconneciton = DBConnectionAgent()
        if self.__DBconneciton.connect(address, port):
            print("Successfully connected to DB at "+"mongodb://"+address+":"+port+"/")
            self.__clientManager = ClientListener()
        else:
            print("Unable to connect to DB at "+"mongodb://"+address+":"+port+"/")
    
    def _clientListener(self):
        pass

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
            pass
    
    def clearDB(self, column):
        self.__db[column].delete_many({})

    def insertPosts(self, post:dict):
        posts = self.__db.posts
        post_id = posts.insert_one(post).inserted_id
        print(post_id)

    def getPost(self, query:dict):
        return self.posts.find_one(query)
    
#end DBConnecitonAgent

class ClientListener():
    # Functions should use multiprocessing for optimized response time
    def __init__(self):
        self.__knownClients = {}
        self.__processList = {}

    def __del__(self):
        pass

    def _listen(self):
        # Listens on port 77777
        while True:
            break

    def _verifyClient(self, client):
        if client in self.__knownClients:
            return True
        else:
            return False

    def _addClient(self, client):
        if not self._verifyClient(client):
            newClient = Client()
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

class Client():
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