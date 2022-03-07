#! /usr/bin/env python3

# Echo client program
import socket, sys, re
sys.path.append("../lib")       # for params
import params

#encoding file name and contents into a byte array
def get_bytes_from_file(filename):
    arr = [bin(len(filename))]
    for i in filename.encode():
        arr.append(bin(i))

    arr.append(bin(len(open(filename, "rb").read())))
    for i in open(filename, "rb").read():
        arr.append(bin(i))
    return arr

def bytes_to_file(arr):
    filename = ""
    for i in arr[1:int(arr[0],2)+1]:
        filename += chr(int(i,2))
    f = open("out.txt", "w")
    for i in arr[int(arr[0],2) + 2:]:
        f.write(chr(int(i,2)))

switchesVarDefaults = (
    (('-s', '--server'), 'server', "127.0.0.1:50001"),
    (('-?', '--usage'), "usage", False), # boolean (set if present)
    )


progname = "framedClient"
paramMap = params.parseParams(switchesVarDefaults)

server, usage  = paramMap["server"], paramMap["usage"]

if usage:
    params.usage()

try:
    serverHost, serverPort = re.split(":", server)
    serverPort = int(serverPort)
except:
    print("Can't parse server:port from '%s'" % server)
    sys.exit(1)

s = None
for res in socket.getaddrinfo(serverHost, serverPort, socket.AF_UNSPEC, socket.SOCK_STREAM):
    af, socktype, proto, canonname, sa = res
    try:
        print("creating sock: af=%d, type=%d, proto=%d" % (af, socktype, proto))
        s = socket.socket(af, socktype, proto)
    except socket.error as msg:
        print(" error: %s" % msg)
        s = None
        continue
    try:
        print(" attempting to connect to %s" % repr(sa))
        s.connect(sa)
    except socket.error as msg:
        print(" error: %s" % msg)
        s.close()
        s = None
        continue
    break

if s is None:
    print('could not open socket')
    sys.exit(1)

byte_arr = get_bytes_from_file("test.txt")


message = []
for i in byte_arr[int(byte_arr[0],2) + 2:]:
    message.append(int(i,2))
outMessage = bytearray(message).decode()
while outMessage:
    print("sending '%s'" % outMessage)
    bytesSent = s.send(outMessage)
    outMessage = outMessage[bytesSent:]

data = s.recv(1024).decode()
print("Received '%s'" % data)

s.shutdown(socket.SHUT_WR)      # no more output

while 1:
    data = s.recv(1024).decode()
    print("Received '%s'" % data)
    if len(data) == 0:
        break
print("Zero length read.  Closing")
s.close()
