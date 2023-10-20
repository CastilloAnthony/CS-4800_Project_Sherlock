import socket # Networking stuff
import json # For transferring data between server and client
import multiprocessing # For concurrent processing (interface handling, generation of graphs, etc.)
from controllers.homepage import Homepage
from controllers.trackWebsite import TrackWebsite
from controllers.deleteWebsite import DeleteWebsite
from controllers.addPreset import AddPreset
from controllers.editPreset import EditPreset
from controllers.deletePreset import DeletePreset

class Client():
    # Communicates with Server
    def __init__(self):
        self.__Homepage = Homepage() # Hosts
        self.__trackWebsite = TrackWebsite() # Controller
        self.__deleteWebsite = DeleteWebsite() # Controller
        self.__addPreset = AddPreset() # Controller
        self.__editPreset = EditPreset() # Controller
        self.__deletePreset = DeletePreset() # Controller

    def __del__(self):
        pass

    def _connectToServer(self, address, port):
        pass

    def _disconnect(self):
        pass
# end Client