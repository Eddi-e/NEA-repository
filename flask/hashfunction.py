import hashlib

def hashfunc(inputtext):
    inputencoded = inputtext.encode()
    hashfunc = hashlib.sha256()
    hashfunc.update(inputencoded)
    var1 = hashfunc.hexdigest()
    return(var1)

if __name__ == '__main__':
    print(hashfunc(input('enter text')))
