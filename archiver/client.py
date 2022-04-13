import socket

#functions to archive and unarchive files
def archive(filename):
    arr = bytearray()
    arr.append((len(filename)))
    arr.extend(bytearray(filename.encode()))

    with open(filename, "rb") as image:
        b = bytearray(image.read())
        arr.extend(b)
        return arr

def un_archive(filename, b):
    b = b[b[0] + 1:]
    with open(filename, "wb") as f:
        f.write(b)

#setting up client-host info
client_socket = socket.socket()
host = "127.0.0.1"
port = 50001

#trying to connect to server
print("waiting for connection")
try:
    client_socket.connect((host, port))

except socket.error as e:
    print(str(e))

#prompt user to transfer a file
while True:
    inp = input("Type name of file you want to transfer:")
    try:
        arch_file = archive(inp)

    #invalid file name
    except FileNotFoundError:
        print("File name does not exist")
        continue

    #send archived file to server
    client_socket.send(arch_file)
    response = client_socket.recv(1024)

    #if server sent back that file already exists
    #ask user to rename file
    if response.decode() == "failed":
        name = inp
        while name == inp:
            print("This filename already exists.")
            name = input("Please rename the file: ")
        client_socket.send(str.encode(name))

        
    print("File:" + inp + " Transferred sucessfully!")
client_socket.close()
