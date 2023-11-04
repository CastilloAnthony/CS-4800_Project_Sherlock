# Created by Anthony Castillo
from server.server import Server

def main():
    """Creates a new instance of the server and calls its startServer function.
    """
    newServer = Server()
    newServer.startServer()
#end main

if __name__ == "__main__":
    main()
