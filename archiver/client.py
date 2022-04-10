import socket, sys, re
#encoding file name and contents into a byte array
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


server_host = "127.0.0.1"
server_port= 50001

s = None
for res in socket.getaddrinfo(server_host, server_port, socket.AF_UNSPEC, socket.SOCK_STREAM):
    af, socktype, proto, canonname, sa = res
    try:
        s = socket.socket(af, socktype, proto)
    except socket.error as msg:
        print(msg)
        s = None
        continue
    try:
        s.connect(sa)
    except socket.error as msg:
        print(msg)
        s.close()
        s = None
        continue
    break

if s is None:
    print('could not open socket')
    sys.exit(1)

#archiving the file as a byte array
byte_arr = archive("test.txt")
#sending contents of the file
outMessage = byte_arr[byte_arr[0]+1:]
#while outMessage:
print("sending '%s'" % outMessage.decode())
bytesSent = s.send(outMessage)
 #   outMessage = outMessage[bytesSent:]

data = s.recv(1024).decode()
print("Received '%s'" % data)
s.shutdown(socket.SHUT_WR)      # no more output
#while 1:
 #   data = s.recv(1024).decode()
  #  print("Received '%s'" % data)
   # if len(data) == 0:
    #    break;    
s.close()

    
    
