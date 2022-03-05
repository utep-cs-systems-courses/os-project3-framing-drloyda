#encoding file name and contents into a byte array
def get_bytes_from_file(filename):
    arr = [len(filename)]
    arr.extend(filename.encode())

    arr.append(len(open(filename, "rb").read()))
    arr.extend(open(filename, "rb").read())
    return arr

def bytes_to_file(arr):
    filename = bytearray(arr[1:arr[0]+1]).decode()
    f = open("out.txt", "w")
    f.write(bytearray(arr[arr[0]+2:]).decode())


byte_arr = get_bytes_from_file("test.txt")
bytes_to_file(byte_arr)
byte = bytearray([116, 101, 115, 116, 46, 116, 120, 116])
lst = [1,2,3,4,5,6,7,8,9]
print(lst[3+1:])


