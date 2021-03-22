import time
import multiprocessing as mp

numProcesses = mp.cpu_count()
processes = []

max = 500

'''Prime Number finder'''
def is_prime(n):
    if n <=1:
        return False
    for i in range(2, n): 
        if n %  i == 0:
            return False
    return True

'''Get Prime Numbers'''
def get_primes(range_min, range_max):
    primes = []
    for n in range(range_min, range_max):
        if is_prime(n):
            primes.append(n)
    return primes

'''Store Prime Numbers into Message Queue'''
def queue_primes(msgQueue, processNum):
    print("Child process ", mp.current_process().pid," starting")

    myprimes = get_primes(int(processNum * max/numProcesses), int((processNum + 1)*max/numProcesses))

    for prime in myprimes:
        msgQueue.put("Child process " + str(processNum) + " with process id " + 
        str(mp.current_process().pid) + " calculated" + "\n" + str(prime))

    print("Child process ", mp.current_process().pid," closing")

'''Main Function'''
def main():

    print("Main process started")
    mp.set_start_method('spawn')

    #Begin start time
    startTime = time.time()

    #Create message queue for processes
    messageQueue = mp.Queue()

    #Create and start processes
    for p in range(numProcesses):
        process = mp.Process(target=queue_primes, args=(messageQueue,p))
        processes.append(process)
        process.start()

    #Join processes
    for process in processes:
        process.join()

   #print results
    while not messageQueue.empty():
        print(messageQueue.get())

    #Stop time
    stopTime = time.time()

    print("Main process Exiting")
    duration = stopTime - startTime
    print("\nTime to complete: ", "{:.2f}".format(duration), "seconds")

if __name__ == "__main__":
    main()