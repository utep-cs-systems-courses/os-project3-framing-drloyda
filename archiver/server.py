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

        
def un_archive(filename, b):
    b = b[b[0] + 1:]
    with open(filename, "wb") as f:
        f.write(b)

files = set()

#setting up server info
server_socket = socket.socket()
host = "127.0.0.1"
port = 50001

#trying to connect with the port
try:
    server_socket.bind((host, port))

except socket.error as e:
    print(str(e))

#listen for client connections
print("Waiting for connection.")
server_socket.listen(5)

#method that recieves file from client and uploads it
def client_thread(server):
    while True:
        data = server.recv(1024)

        filename = "upload-"+ data[1:data[0]+1].decode()
    
        
        if filename in files:
            print("failed!")
            server.send(str.encode("failed"))
            name = "upload-" + server.recv(1024).decode()
            un_archive(name, data)
            continue
        
        files.add(filename)     
        un_archive(filename, data)
        
        if not data:
            break
        
        server.send(str.encode("success"))
    server.close()

#creates a new thread to run whenever a client connects
while True:
    Client, address = server_socket.accept()
    print("Connected as:" + address[0] + ":" + str(address[1]))
    start_new_thread(client_thread, (Client,))
                    
server_socket.close()
        
