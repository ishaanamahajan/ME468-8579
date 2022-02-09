from math import e

#xl - x low
#xh - x high
#xm - x half

def bisecRecursive (f, xl, xh, iteration):
    print(f(xl), f(xh))

    iteration += 1

    xm = (xl + xh)/2

    print("Iteration: " +  str(iteration) + " xl: " + str(xl) + " xm: " + str(xm) + " xh: " + str(xh) + " f(xm): " + str(f(xm)))
    
    if((xh - xl) < 10**(-6)):
        return xm

    
    if ((f(xl)<0 and f(xh) <0) or (f(xl) >=0 and f(xh) >= 0)):
      xl = xm
      return bisecRecursive(f, xl, xh, iteration)

    else:
      xh = xm
      return bisecRecursive(f, xl, xh, iteration)


    
print(10**-6)

f = lambda x: e**x - 4

out = bisecRecursive(f, 1, 4, 0)
print("output = ", out)


print("f(out) =", f(out), "which is approximately equal to 0")



    
   


