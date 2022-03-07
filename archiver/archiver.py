#encoding file name and contents into a byte array
def get_bytes_from_file(filename):
    arr = [bin(len(filename))]
    for i in filename.encode():
        arr.append(bin(i))

    arr.append(bin(len(open(filename, "rb").read())))
    for i in open(filename, "rb").read():
        arr.append(bin(i))
    print(arr)
    lst = []
    for i in arr[int(arr[0],2) + 2:]:
        lst.append(int(i,2))
    print(bytearray(lst).decode())
    return arr

def bytes_to_file(arr):
    filename = ""
    for i in arr[1:int(arr[0],2)+1]:
        filename += chr(int(i,2))
    f = open("out.txt", "w")
    for i in arr[int(arr[0],2) + 2:]:
        f.write(chr(int(i,2)))


byte_arr = get_bytes_from_file("test.txt")
bytes_to_file(byte_arr)


