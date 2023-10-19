# DEPRECIATED, NOT NEEDED
import time
import uuid
import socketserver
import socket
import random # Not Needed
from clientInfo import ClientInfo

class ClientListener():
    # Functions should use multiprocessing for optimized response time
    def __init__(self, queue=None, address='127.0.0.1', port=7777):
        self.__socketServer = False
        self.__requestHandler = False
        #self.__socket = False
        self.__knownClients = {}
        self.__processList = {}
        self.__q = queue
        self.__address = address
        self.__port = port

    def __del__(self):
        del self.__knownClients
        del self.__processList
        del self.__q

    def setAddress(self, address):
        self.__address = address

    def setPort(self, port):
        self.__port = port

    def _setupConnection(self):
        #self.__socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #self.__requestHandler = socketserver.StreamRequestHandler(self.__socket, (self.__address, self.__port), )
        self.__requestHandler = socketserver.StreamRequestHandler
        self.__socketServer = socketserver.TCPServer((self.__address, self.__port), self.__requestHandler)
        #self.__socketServer.server_bind()
        return self._checkConnection()
        
    def _checkConnection(self):
        if self.__socketServer.server_address == (self.__address, self.__port):
            return True
        else:
            return False
    
    def _listen(self):
        # Listens on port 77777
        x = 0
        while True:
            self._checkConnection()
            self.__socketServer.serve
            conn, addr = self.__socketServer.serve_forever()
            self._verifyClient(conn, addr)
            pass
            #self.__pipe.send(7)
        #self.__pipe.close()
        return

    def _practiceMultiprocessing(self):
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

    def start(self):
        if self._setupConnection():
            print('Server successfully bound to ', self.__address, self.__port)
        else:
            print('Could not bind server at ', self.__address, self.__port)
#end CLientListener

'''
def main():
    newListener = ClientListener()
    newListener.start()

main()
'''