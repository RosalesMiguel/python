from typing import List

#accepts an int and return the double of that int
def doubledInt(x: int) -> int: return x*2

#accepts two floats and returns the larger value
def largest(x: float,y: float) -> float: return x if x >= y  else y

#accepts two (float,float) tuples which represent two points in a cartesian plane and returns true if the points describe a vertical line and false otherwise
def isVertical(a: tuple,b: tuple) -> bool: return True if a[0] == b[0] else False

#accepts an integer n and returns the first n primes
def primes(n: int) -> List[int]:
    primes_list = []
    c = 2
    while n!=0:
        for i in range(2,c):
            if c%i==0:
                break
        else:  
            primes_list.append(c)  
            n-=1
        c+=1  
    return primes_list


#accepts an integer n and returns a list containing the first n elements of fibonacci sequence (starting with 0 and 1)
def fibonacciSequence(n:int) -> List[int]:
    fib_list = []
    for i in range(n):
        if i == 0 or i == 1:
            fib_list.append(1)
        else:
            fib_list.append(fib_list[i-1]+fib_list[i-2])
    return fib_list

#accepts a list of integers and returns a list with the same integers sorted from smallest to highest
def sortedIntegers(l:List[int]) -> List[int]:
    for i in range(len(l)-1):
        for j in range(len(l)-i-1):
            if l[j] > l[j + 1] :
                l[j], l[j + 1] = l[j + 1], l[j]
    return l

#accepts a list of integers and returns all the sublists of the list. Sublists are contiguous chunks of a list (including an empty list and the list itself). [1,2], [2], [], [2,3,4], and [1,2,3,4,5] are sublists of [1,2,3,4,5] but [3,5] and [1,2,3,4,6] are not.
def sublists(l:List[int]) -> List[List[int]]:  
    list_sublists = [[]]  
    for i in range(len(l) + 1): 
        for j in range(i + 1, len(l) + 1): 
            sub = l[i:j] 
            list_sublists.append(sub) 
    return list_sublists 