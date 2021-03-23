import hashlib
import time
import os
import multiprocessing as mp
import concurrent.futures
from threading import Thread

hashvalues = []
threads = []
processes = []
cpus = os.cpu_count()
textfile = "sampleData.txt"
currentDir = os.getcwd()
text_file = open(os.path.join(currentDir, textfile), 'r')
text = text_file.readlines() * 10
chunks = [text[x:x+cpus] for x in range(0, len(text), cpus)]
max = len(chunks)
text_file.close()


def encrypt(data):
    for line in data:
        hashvalues.append(hashlib.sha256(line.encode()))

def encrypt_parallel(data):
    for chunk in data:
        for line in chunk:
            hashvalues.append(hashlib.sha256(line.encode()))
       
def showValues():
    for hash in hashvalues:
        print(hash.digest())

if __name__ == "__main__":
#xxxxxxxxSERIALxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
    '''
    startTime = time.time() 
    encrypt(text)
    stopTime = time.time()
    serialTime = stopTime - startTime
    #showValues()
    hashvalues = []
    
#xxxxxxxxMULTITHREADING USING THREAD POOLxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
    
    startTime = time.time()
    with concurrent.futures.ThreadPoolExecutor(max_workers=cpus) as \
    executor:
        for chunk in chunks:
            executor.submit(encrypt, chunk)
    stopTime = time.time()
    mt_time = stopTime - startTime
    showValues()
    hashvalues = []
    '''
#xxxxxxxxMULTITHREADING USING THREAD OBJECTxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
    
    startTime = time.time()
    i = 0
    for thread in range(cpus):
        thread = Thread(target=encrypt_parallel, args=[chunks[int(i*max/cpus):(int((i+ 1)*max/cpus)) ],])
        thread.start()
        threads.append(thread)
        i += 1
        
    for thread in threads:
        thread.join()
    
    stopTime = time.time()
    thread_time = stopTime - startTime
    
    showValues()

    '''
    print(f'Serial time to encode: {(serialTime)}')
    print(f'Multithreading(thread-pool) time to encode: {(mt_time)}')
    '''
    print(f'Multithreading(using thread objects) time to encode: {(thread_time)}') 


