'''
Created on Dec 3, 2012

@author: praveen
'''

def binary_search_rec(lst, val, low, high):
    """ Binary search implementation using recursive method """
    
    if low == high:
        return -1
    
    med = (high - low)/2 + low
    
    if lst[med] == val:
        return med
    if lst[med] < val:
        return binary_search_rec(lst, val, med+1, high)
    if lst[med] > val:
        return binary_search_rec(lst, val, low, med-1)

def binary_search_iter(lst, val, low, high):
    """ Binary search implementation using iterative method """
    
    while low <= high:
        med = (high - low)/2 + low
        if lst[med] == val:
            return med
        if lst[med] < val:
            low = med+1
        if lst[med] > val:
            high = med-1

if __name__ == '__main__':
    lst = [2, 5, 7, 9, 12, 25]
    print binary_search_rec(lst, 25, 0, len(lst))
    print binary_search_iter(lst, 25, 0, len(lst))
