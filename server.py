#import mysql.connector # For database, unless we use MongoDB
#import sql # For transferring data between server and client
import uuid # Universally Unique IDentifier (For User IDs and others things)
import multiprocessing # For concurrent processing (client requests, data retrival, etc.)
import pymongo

class Server(): # The main server handler class
    # Most new processes should be created as a new process
    def __init__(self):
        self._startDB()
        self.__DBconneciton = DBConnectionAgent()
    
    def __del__(self):
        pass

    def _startDB(self):
        pass

    def _setupConnection(self):
        pass
    
    def _clientListener(self):
        pass

# end Server

class DBConnectionAgent():
    def __init__(self):
        self.__client = False
        self.__db = False

    def __del__(self):
        del self.__client
        del self.__db

    def connect(self, dbAddress="localhost", port="27017"):
        """Connects to a specified server.

        Args:
            dbAddress (string): The IP Address of the server. Defaults to "localhost".
            port (string): The Port Number for the Server. Defaults to "27017".
        """
        try:
            self.__client = pymongo.MongoClient("mongodb://"+dbAddress+":"+port+"/")
        except:
            print("Could not connect to DB at: "+"mongodb://"+dbAddress+":"+port+"/")
            self.__client = False
        
    def getDBs(self):
        if self.__client != False:
            return self.__client.list_database_names()

    def useDB(self, db):
        self.__db = self.__client[db]

    def addToDB(self, column, content):
        if self.__db != False:
            self.__db[column].insert_one(content)

    def removeFromDB(self, column, content):
        pass

    def requestFromDB(self, column):
        if self.__db != False:
            pass
#end dbConnecitonAgent

def main():
    newServer = Server()
    #newServer.

if __name__ == "__main__":
    main()
#end main()