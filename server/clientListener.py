import time
import uuid
import random # Not Needed
from clientInfo import ClientInfo

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