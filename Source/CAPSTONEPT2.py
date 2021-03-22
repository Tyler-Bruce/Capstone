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
data = text_file.readlines()
chunks = [data[x:x+cpus] for x in range(0, len(data), cpus)]
text_file.close()


def encrypt(data, list):
    for line in data:
        list.append(hashlib.sha256(line.encode()))

def encrypt_parallel(data):
    for chunk in data:
        for line in chunk:
            hashvalues.append(hashlib.sha256(line.encode()))

    '''
def encrypt_futures(line):  #not in use
    hashvalues.append(hashlib.sha256(line.encode()))
    '''        
def showValues():
    for hash in hashvalues:
        print(hash.digest())

if __name__ == "__main__":
#xxxxxxxxSERIALxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
    '''
    startTime = time.time() 
    encrypt(data)
    stopTime = time.time()
    serialTime = stopTime - startTime
    '''
#xxxxxxxxMULTITHREADING USING THREAD POOLxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
    '''
    startTime = time.time()
    with concurrent.futures.ThreadPoolExecutor(max_workers=cpus) as \
    executor:
        for line in data:
            executor.submit(encrypt_parallel, line)
    stopTime = time.time()
    mt_time = stopTime - startTime
    showValues()
    '''
#xxxxxxxxMULTITHREADING USING THREAD OBJECTxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
    '''
    startTime = time.time()
    for thread in range(cpus):
        thread = Thread(target=encrypt_parallel, args=[chunks,])
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()
    
    stopTime = time.time()
    thread_time = stopTime - startTime
    '''
#xxxxxxxxMULTIPROCESSINGxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
    
    startTime = time.time()
    
    for process in range(cpus):
        process = mp.Process(target=encrypt, args=(data,hashvalues))
        process.start()
        processes.append(process)
        
    for process in processes:
        process.join()
    
    '''
    with concurrent.futures.ProcessPoolExecutor(max_workers=cpus) as \
    executor:
        for line in data:
            executor.submit(encrypt_parallel, line)
    '''        
    stopTime = time.time()
         
    mp_time = stopTime - startTime
    
    showValues()

    #print(f'Serial time to encode: {(serialTime)}')
    #print(f'Multithreading(thread-pool) time to encode: {(mt_time)}')
    #print(f'Multithreading(using thread objects) time to encode: {(thread_time)}') 
    
    print(f'Multiprocessing time to encode: {(mp_time)}')


