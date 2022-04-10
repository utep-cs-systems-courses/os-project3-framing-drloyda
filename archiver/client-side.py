import socket

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

client_socket = socket.socket()

host = "127.0.0.1"
port = 50001

print("waitin for connection")
try:
    client_socket.connect((host, port))

except socket.error as e:
    print(str(e))

response = client_socket.recv(1024)

while True:
    inp = input("Type name of file you want to transfer:")
    try:
        arch_file = archive(inp)
    except FileNotFoundError:
        print("File name does not exist")
        continue
    client_socket.send(arch_file[arch_file[0]+1:])
    response = client_socket.recv(1024)
    print(response.decode())

client_socket.close()
