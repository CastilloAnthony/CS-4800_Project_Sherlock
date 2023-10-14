import json # For transferring data between server and client
import multiprocessing # For concurrent processing (interface handling, generation of graphs, etc.)
from controllers import Homepage, TrackWebsite

class Client():
    # Communicates with Server
    def __init__(self):
        self.__Homepage = Homepage() # Hosts 

    def __del__(self):
        pass

    def _connectToServer(self, address, port):
        pass

    def _disconnect(self):
        pass
#end ConnectionAgent

# end Client