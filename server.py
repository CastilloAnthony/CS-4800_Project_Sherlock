import mysql.connector # For database, unless we use MongoDB
import sql # For transferring data between server and client
import uuid # Universally Unique IDentifier (For User IDs and others things)
import multiprocessing # For concurrent processing (client requests, data retrival, etc.)

class Server(): # The main server handler class
    # Most new processes should be created as a new process
    def __init__(self):
        self._startDB()
        pass
    
    def __del__(self):
        pass

    def _startDB(self):
        pass

    def _setupConnection(self):
        pass
    
    def _clientListener(self):
        pass

# end Server