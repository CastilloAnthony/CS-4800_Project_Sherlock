#ANTHONY
import time
from controllers.queueManager import requestData

class ViewPreset():
    def __init__(self, requestQ, dataQ):
        self.__requestQ, self.__dataQ = requestQ, dataQ

    def __del__(self):
        del self.__requestQ, self.__dataQ

    '''
    def requestData(self, request):
        self.__requestQ.put(request)
        time.sleep(0.1)
        initialDataID = False
        while self.__dataQ.empty() != True:
            newData = self.__dataQ.get()
            if newData['id'] == initialDataID:
                self.__requestQ.put(request)
                time.sleep(0.1) #import time
                initialDataID = False
            elif initialDataID == False:
                initialDataID = newData['id']
            if newData['id'] == request['id']:
                if newData['data'] is not False:
                    return newData
            else:
                self.__dataQ.put(newData)
    '''

    def query(self):
        pass

    def viewPreset(self):
        pass