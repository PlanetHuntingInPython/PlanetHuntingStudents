from math import floor, ceil

def binarySearch(array, element):
    lb = 0
    ub = len(array) - 1
    while ub > lb + 1:
        mid = (lb + ub)>>1
        if array[mid] > element:
            ub = mid - 1
        else:
            lb = mid
    return ub if array[ub] <= element else lb

def interpolationSearch(array, element):
    if element < array[0]:
        return 0
    elif element > array[-1]:
        return len(array) - 1
    
    lb = 0
    ub = len(array) - 1
    f = 0
    while ub > lb + 1:
        mid = (ub - lb)*(element - array[f := floor(lb)])/(array[ceil(ub)] - array[f]) + lb
        if array[floor(mid)] > element:
            ub = mid - 1
        else:
            lb = mid
    return ub if array[ub := floor(ub)] <= element else floor(lb)