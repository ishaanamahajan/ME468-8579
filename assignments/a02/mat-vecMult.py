import matplotlib.pyplot as plt
import numpy as np
import random
from datetime import datetime
import time
import sys
import statistics


def multiplyUsingLoops(n):
    np.random.seed(int(time.time()))
    A = np.random.uniform(-1, 1, size=(n, n))
    B = np.empty(n)
    B.fill(1.0)

    times = []
    

    C = []

    for i in range(20):
        start = ((time.time()) * 1000)
        for i in range(n):
            temp = 0
            for j in range(n):
                temp +=  A[i][j] * B[j]

              
            C.append(temp)
            
        times.append(((time.time()) * 1000) - start)

    
    timeTaken = round(sum(times)/20 * 1000)
    stdTime = statistics.stdev(times)

    print(C[-1])
    print(timeTaken)
    print(stdTime)
    return timeTaken
    


def multiplyUsingFunction(n):
    np.random.seed(int(time.time()))
    A = np.random.uniform(-1, 1, size=(n, n))
    B = np.empty(n)
    B.fill(1.0)
    times = []
    for i in range(20):
        start = (time.time()) * 1000
        C = np.dot(A, B)
       
        times.append(((time.time()) * 1000) - start)

    timeTaken = round(sum(times)/20 * 1000)
    stdTime = statistics.stdev(times)

    print(C[-1])
    print(timeTaken)
    print(stdTime)
    return timeTaken

if(len(sys.argv) == 2):
    multiplyUsingLoops(int(sys.argv[1]))
    multiplyUsingFunction(int(sys.argv[1]))
else:    
 n = [2**9, 2**10, 2**11, 2**12, 2**13]
 timesLoop = []
 timesFunction = []
 for i in range(len(n)):
    timesLoop.append(multiplyUsingLoops(n[i]))
    timesFunction.append(multiplyUsingFunction(n[i]))

    



 plt.plot(n, timesLoop , 'b', label ="Using for loops")
 plt.plot(n, timesFunction , '--r' , label = "Using numpy function")
 plt.xlabel("n value")
 plt.ylabel("Time * 1e7 (ms)")
 plt.title("MacOS - Apple M1, 8GB RAM")
 plt.legend()

 plt.xlim(2**8, 2**14)
 plt.xticks([2**9, 2**10, 2**11, 2**12, 2**13])

 plt.xscale('log')    
 plt.yscale('linear')

 plt.show()




    




