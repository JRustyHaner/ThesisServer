## THESIS FOR JAMES R HANER
## SERVER SCRIPT

## LIBRARIES
import socket
import sys

## GLOBAL VARS
version = 0.1
port = 10000
hostname = "localhost"

## FUNCTIONS
   
    #F1: LISTEN
    #CREATES THE SOCKET SERVER AND LISTENS FOR INCOMING TRANSMISSIONS

def listen():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = (hostname, port)
    sock.bind(server_address)
    print >>sys.stderr, 'Starting up on up on %s port %s' % sock.getsockname()
    sock.listen(1)
    active = True
    while active == True:
        print >>sys.stderr, 'Waiting for a connection'
        connection, client_address = sock.accept()
        try:
            print >>sys.stderr, 'client connected:', client_address
            while True:
                data = connection.recv(16)
                print >>sys.stderr, 'received "%s"' % data
                if data != "Bye.":
                    data = command(data)
                    connection.sendall(data)
                else:
                    active = False
        finally:
            connection.close()    
        
def command(arg):
    out = arg + " " + "return."
    return out

## MAIN
def main():
    print("STARTUP")
    listen()

## CALL MAIN
main()