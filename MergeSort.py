import multiprocessing
import logging

def main():
    import sys
    from random import randint
    if len(sys.argv) == 2:
        N = int(sys.argv[1])
    else:
        N = 8
    aList = [randint(1, N*N) for i in range(N)]
    print(aList)
    a, b = multiprocessing.Pipe()
    p = multiprocessing.Process(target=mergeSort, args=(b,))

    a.send(aList)
    p.start()
    p.join()
    bList = a.recv()
    print(bList)
    
def mergeSort(connect):
    array = connect.recv()
    if len(array)<=1:
        connect.send(array)
        return
    
    mid = len(array) // 2
    a, b = multiprocessing.Pipe()
    procLeft = multiprocessing.Process(target=mergeSort, args=(b,))
    a.send(array[:mid])
    procLeft.start()
    arrayLeft = a.recv()
    
    c, d = multiprocessing.Pipe()
    procRight = multiprocessing.Process(target=mergeSort, args=(d,))
    c.send(array[mid:])
    procRight.start()
    arrayRight = c.recv()
    
    connect.send( merge(arrayLeft, arrayRight) )
    
    
def merge(arrayLeft, arrayRight):
    result = []
    while arrayLeft and arrayRight:
        if arrayLeft[0] <= arrayRight[0]:
            result.append(arrayLeft.pop(0))
        else:
            result.append(arrayRight.pop(0))
    if arrayLeft:
        result += arrayLeft
    if arrayRight:
        result += arrayRight
    return result
    
if __name__ == '__main__':
    multiprocessing.log_to_stderr(logging.ERROR)
    main()