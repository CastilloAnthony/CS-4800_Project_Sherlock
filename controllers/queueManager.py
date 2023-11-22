# Created by Anthony Castillo
import time
from multiprocessing import Queue as mpQ

def requestData(request, requestQ:mpQ, dataQ:mpQ):
    """_summary_: in order to get the correct data and check for wrong insertions

    Args:
        request (dict): uuid, request_type, column, query, changeTo

    Returns:
        dict: uuid, id?,data
    """
    requestQ.put(request)
    #initialDataID = False
    while dataQ.empty() != True:
        time.sleep(0.1)
    while True:
        newData = dataQ.get()
        '''
        if newData['id'] == initialDataID:
            #requestQ.put(request)
            time.sleep(0.1) #import time
            initialDataID = False
        elif initialDataID == False:
            initialDataID = newData['id']
        '''
        if newData['id'] == request['id']:
            if newData['data'] is None:
                print(str(time.time())+' - Recieved Nonetype response using this request: '+str(request))
                requestQ.put(request)
            #elif newData['data'] is False:
            #    return newData
            else:
                return newData
        else:
            dataQ.put(newData)