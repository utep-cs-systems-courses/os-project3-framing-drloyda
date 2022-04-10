import socket
import os
import threading
from _thread import *

class thread(threading.Thread):
    def __init__(self, thread_name, thread_ID):

        threading.Thread.__init__(self)
        self.thread_name = thread_name
        self.thread_ID = thread_ID
        
    # helper function to execute the threads
    def run(self):
        print(str(self.thread_name) +" "+ str(self.thread_ID));

server_socket = socket.socket()

host = "127.0.0.1"
port = 50001

thread_count = 0

try:
    server_socket.bind((host, port))

except socket.error as e:
    print(str(e))


print("Waiting for connection.")
server_socket.listen(5)


def threaded_client(connection):
    connection.send(str.encode("Welcome to server"))
    while True:
        data = connection.recv(1024)
        reply = "Server sent back: " + data.decode()

        if not data:
            break
        connection.sendall(str.encode(reply))
    connection.close()

while True:
    Client, address = server_socket.accept()
    print("Connected as:" + address[0] + ":" + str(address[1]))
    start_new_thread(threaded_client, (Client,))
    #new_thread = thread(threaded_client,(Client,))
    #new_thread.start()
    thread_count += 1
    print("Thread number:" + str(thread_count))
server_socket.close()
    
        
