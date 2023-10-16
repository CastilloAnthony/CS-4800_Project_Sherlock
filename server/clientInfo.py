import uuid

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