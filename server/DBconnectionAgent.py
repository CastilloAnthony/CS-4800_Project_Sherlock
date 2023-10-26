import pymongo
import time
import multiprocessing as mp

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
        self.__client.close()

    def createNewDB(self, name:str):
        return self.__client[name]['Initial'].insert_one({'name':name, 'notes':'Created a new database named '+name, 'timestamp':time.ctime()}).acknowledged
    
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
                return self.__db[column].insert_one(content).acknowledged
            except:
                return False
        else:
            return False

    def removeFromDB(self, column:str, query:dict):
        if self.__db != False:
            return self.__db[column].delete_one(query).acknowledged
        else:
            return False

    def removeManyFromDB(self, column:str, query:dict):
        if self.__db != False:
            return self.__db[column].delete_many(query).acknowledged
        else:
            return False

    def requestFromDB(self, column:str, query:dict):
        if self.__db != False:
            return self.__db[column].find_one(query)
        else:
            return False
    
    def requestManyFromDB(self, column:str, query:dict):
        if self.__db != False:
            tempData = []
            cur = self.__db[column].find(query)
            for doc in cur:
                tempData.append(doc['url'])
            return tempData
        else:
            return False

    def clearDB(self, column:str):
        if self.__db != False:
            return self.__db[column].delete_many({}).acknowledged
        else:
            return False

    def verifyCollection(self, column:str):
        try:
            self.__db.validate_collection(column)
            return True
        except pymongo.errors.OperationFailure:
            return False
#end DBConnecitonAgent
