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

    print(times)
    return times
    


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

   
    return times

n = [2**9, 2**10, 2**11, 2**12, 2**13]
timesLoop = []
timesFunction = []
for i in range(len(n)):
    timesLoop.extend(multiplyUsingLoops(n[i]))
    
  
    timesFunction.extend(multiplyUsingFunction(n[i]))
    

#plotting using a scatter plot
for i in range(len(n)):
    for j in range(20*i, 20+(20*i)):
        plt.scatter(n[i], timesLoop[j], color = 'blue', label = "Using loops")
        plt.scatter(n[i],timesFunction[j], color = 'red',label = "Using function")


        
    

plt.legend()
plt.title("Matrix-vector Multiply for 100 time points")

plt.xlim(2**8,2**14)

handles, labels = plt.gca().get_legend_handles_labels()
by_label = dict(zip(labels, handles))
plt.legend(by_label.values(), by_label.keys(), loc = 'upper left')

plt.ylabel('Time in ms')
plt.xlabel("n values")
plt.xscale('log')    
plt.yscale('linear')



plt.show()



# plotting using a line plot


#for i in range(len(n)):
for i in range(len(n)):
        plt.plot([i] * 20, timesLoop[20*i:20+(20*i)], color = 'b', label = "Using loops")
        plt.plot([i] * 20, timesFunction[20*i:20+(20*i)], color = 'r',label = "Using function")



plt.ylabel('Time in ms')
plt.xlabel("n values")
#plt.yticks(fontsize=12, alpha=.7)
plt.title("Matrix-vector Multiply for 100 time points")
#plt.grid(axis='y', alpha=.3)


handles, labels = plt.gca().get_legend_handles_labels()
by_label = dict(zip(labels, handles))
plt.legend(by_label.values(), by_label.keys(), loc = 'upper left')

plt.xscale('log')    
plt.yscale('linear')
plt.show()