import hashlib
import time

hashvalues = []

text_file = open("X:\Python\sampleData.txt", 'r')
data = text_file.read() * 1000
text_file.close()

def encrypt():
    hashvalues.append(hashlib.sha256(data.encode()))
        
def showValues():
    for hash in hashvalues:
        print(hash.digest())

if __name__ == "__main__":
    #print(data)
    startTime = time.time()
    encrypt()
    stopTime = time.time()
    showValues()
    print(f'time to encode: {(stopTime- startTime)}')



