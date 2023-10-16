from server import Server

def main():
    newServer = Server()
    newServer.startDB()
    newServer.setupConnection()
#end main

if __name__ == "__main__":
    main()
