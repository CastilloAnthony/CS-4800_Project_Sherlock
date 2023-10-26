import uuid
import time
class AddPreset(): # Controller
    def __init__(self):
        pass
    def __del__(self):
        pass
    def query(self, requestQ):
        #ASKING
        masterListRequest = {
            'id': uuid.uuid4(),
            'request_type': 'request',
            'column': 'masterList',
            'query': {}
        }
        requestQ.put(masterListRequest)
        time.sleep(1) 
        #GRABBING
        return super().checkForData(masterListRequest)

    
#end AddPreset