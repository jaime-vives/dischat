import threading
import socket
import sys
from signal import signal, SIGINT
import time

received_messages = []
ipaddr = '::1'
port = 20002

def display_received_messages(sock):
    while True:
        resp = sock.recv(256)
        resp = resp.decode('utf-8','ignore')
        resp = resp.split('|')

        if resp[0] == 'SEND':
            msg = "\n"+resp[1]+" said: " + resp[2]+"\n"
            print(msg)

def register(sock,user):
    command = "REGISTER|"
    command = command + user
    sock.sendall(command.encode('utf-8'))

def send_message(sock,touser,msg):
    command = "SEND|"
    command = command + touser + "|" + msg
    sock.sendall(command.encode('utf-8'))

def main():
    sock = socket.socket(socket.AF_INET6,socket.SOCK_STREAM)
    sock.connect((ipaddr,port))

    # Register myself
    user = input('Username: ')
    register(sock,user)

    display_thread = threading.Thread(target=display_received_messages,name="Display_Thread",args=((sock,)))
    display_thread.start()

    while True:
        touser = input("Who do you want to send a message to? ")
        msg = input('Message: ')
        send_message(sock,touser,msg)

main()
