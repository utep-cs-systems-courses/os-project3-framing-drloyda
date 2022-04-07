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
        
byte_arr = archive("test.txt")
un_archive("out.txt", byte_arr)


