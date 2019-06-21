## THESIS FOR JAMES R HANER
## CLIENT SCRIPT

## LIBRARIES
import socket
import sys

## GLOBAL VARS
version = 0.1
port = 10000
servername = "127.0.0.1"

## FUNCTIONS
   
    #F1: CONNECT
    #CONTACTS THE SERVER

def connect():
    # Create a TCP/IP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Connect the socket to the port where the server is listening
    server_address = (servername, port)
    print >>sys.stderr, 'connecting to %s port %s' % server_address
    sock.connect(server_address) 
        
    try:
    
    # Send data
        message = raw_input("Message to Send:")
        print >>sys.stderr, 'sending "%s"' % message
        sock.sendall(message)

    
        while True:
            data = sock.recv(16)
            if data != "":
                print >>sys.stderr, 'received "%s"' % data
                break
            else:
                break

    finally:
        print >>sys.stderr, 'closing socket'
        sock.close()


## MAIN
def main():
    print("STARTUP")
    connect()

## CALL MAIN
main()