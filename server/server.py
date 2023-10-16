import time
import multiprocessing as mp
from DBconnectionAgent import DBConnectionAgent
from clientListener import ClientListener

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