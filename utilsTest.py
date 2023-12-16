from utils import *
from time import perf_counter
import random
import numpy as np


def benchmarkArrayFunc(size, n, funcs):
    testList = np.asarray([x + random.random() for x in range(size)])
    elements = [0 for x in range(n)]
    resultList = [[] for x in range(len(funcs))]
    tSum = [0 for x in funcs]
    for iteration in range(n):
        element = random.randint(0,size-1) + random.random()
        elements[iteration] = element
        for i, func in enumerate(funcs):
            t1 = perf_counter()
            result = func(testList, element)
            t2 = perf_counter()
            resultList[i].append(result)
            tSum[i] += t2 - t1
    for i, func in enumerate(funcs):
        print(f"{func.__name__}: {tSum[i]*1000/n}ms")


def test(size):
    print(interpolationSearch([x + random.random() for x in range(size)], random.randint(0,size-1) + random.random()))

benchmarkArrayFunc(65000, 10000, [binarySearch, np.searchsorted, interpolationSearch])