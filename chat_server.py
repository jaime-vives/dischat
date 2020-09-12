import threading
import socket
import sys
from signal import signal, SIGINT
import time

ipaddr = '::1'
port = 20002

user_db = {}

# Handle control+c
def handle_controlc(sig,frame):
    print('Exiting...now...')
    exit(0)

# Figure out what the client wants and handle it.
def handle_incoming_connections(socket,client_address):
    while True:
        # Get Command (Register, Send)
        command = socket.recv(256)
        command = command.decode('utf-8','ignore')
        command = command.split('|')
        print(command[0])

        # Determine Stuff
        if command[0] == 'REGISTER':
            print(command[1])
            user_db[command[1]] = {'sock': socket, 'client_address': client_address}

        elif command[0] == 'SEND':
            print(command[1])
            print(command[2])
            user_db[command[1]]['sock'].sendall('|'.join(command).encode('utf-8'))
        else:
            print('Undefined command')
            break

# Server Daemon
def run_server(sock):
    # Accept incoming connections
    while True:
        connection, client_address = sock.accept()

        # Handle an incoming connection
        client_thread = threading.Thread(target=handle_incoming_connections,name='handle_inc_request',args=((connection,client_address)))
        client_thread.start()

# Entry point to the application
if __name__ == '__main__':
    print('Starting Server...')
    
    # Handle Control+C to allow exiting
    signal(SIGINT,handle_controlc)

    # Create server socket
    sock = socket.socket(socket.AF_INET6,socket.SOCK_STREAM)
    sock.bind((ipaddr,port))
    sock.listen()

    # Create a Server Thread and Start it
    server_thread = threading.Thread(target=run_server,name='Server_Daemon',args=((sock,)),daemon=True)
    server_thread.start()

    # Basically, just sleep
    while True:
        time.sleep(5000)

    print('All done')