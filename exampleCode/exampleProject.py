class ThisIsAClass(): # An example class for how all other classes should look like.
    def __init__(self): # Initialize the class
        pass

    def __del__(self): # Delete the variables of the class
        pass

    def __str__(self): # Print the data of the class
        pass

    def _aPrivateFunction(self): # A private function to be accessed only by this class itself
        pass
        
    def aPublicFunction(self): # A public function meant to be called from outside of the class 
        pass
# end ThisIsAClass

class Server():
    # Connects to the database, polls servers for information, handles client connections and requests.
    # Should store client information for future use. (i.e., identifiers, ip addresses, names, guid, etc.) (temporary? expiration?)
    def __init__(self): # Initialize the class
        pass

    def __del__(self): # Delete the variables of the class
        pass

    def _initializeNetwork(self): # CORE
        # What Networking Adapters are available on this device? Networking Adapters (i.e., ethernet, wireless adapter, bluetooth?, etc.)
        # Which do we want to use?
        # What ports are we going to use? 5555? 7777?
        # Need to consider the local device's firewall (Windows 10, Mac, Linux) if we want to allow other devices to connect to the server.
        pass

    def _initializeDatabase(self): # CORE
        # Starts the database server.
        # SQL? MySQL? MongoDB? CSV? TXT? Excel Spreadsheet?
        pass

    def _connectToDatabase(self): # CORE
        # Connects to the database.
        pass

    def _pollServers(self): # CORE
        # What polling rate do we want to use?
        # Needs to be able to continuously poll servers regardless of anything else happening (i.e., use multiprocessing or threads).
        pass

    def _scrapeSocialMedia(self): # SECONDARY
        # Scrapes twitter/x and similar sites for information on planned maintenance, estimated recovery times, etc.
        pass

    def _makePredictions(self): # SECONDARY
        # Uses the history of currently monitored addresses and sites to make a prediction for when a site will go down, or how soon it will recover.
        pass

    def _addDataToDatabase(self): # CORE
        # Takes data gathered from _pollServers() and sends it into the database.
        pass

    def _checkClientMessages(self): # CORE
        # Should be able to continuously check for messages from clients regardless of anything else happening (i.e., use multiprocessing or threads).
        # Calls _getDataFromDatabase() whenever a client requests data.
        pass

    def _addNewClient(self): # CORE
        # Assigns a new client a guid and adds that client to the list of identified clients.
        # Are we using private/public key authentication?
        # newClient = {'guid':'6B29FC40-CA47-1067-B31D-00DD010662DA', 'ip':'10.0.0.30', 'name':'Anthony's Phone', 'MAC':'A1:B2:C3:D4:E5:F6', 'key':'randomDigits'}
        # clientList.append(newClient)
        # etc.
        pass

    def _getDataFromDatabase(self): # CORE
        # As a reaction to any clients requesting data.
        pass

    def _sendDataToClient(self, clientIp): # CORE
        pass

    def start(self):
        pass
# end Server

class Client():
    # Connects to, and requests data from, the server. Displays data.
    def __init__(self): # Initialize the class
        pass

    def __del__(self): # Delete the variables of the class.
        pass

    def _initializeNetwork(self): # CORE
        # What Networking Adapters are available on this device? (i.e., ethernet, wireless adapter, bluetooth?, etc.).
        # Which do we want to use?
        pass
    
    def _generatePrivatePublicKey(self): # CORE
        # Generates private key then generates public key for authentication purposes.
        pass

    def _connectToServer(self, serverIp): # CORE
        # Performs an authentication handshake with the server.
        # Sends some identifier information to the server (name of device, public key, MAC address).
        pass

    def _requestDataFromServer(self, serverIp): # CORE
        # Request a Snapshot of the last 3 hours? 24 hours? 7 days? 1 month?
        pass
    
    def _gui(self): # CORE
        # Displays the data retrieved from _requestDataFromServer().
        pass

    def start(self):
        pass
# end Client