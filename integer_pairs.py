'''
Created on Dec 15, 2012

@author: Praveen Shilavantar
'''

"""
Problem:

Given a list of unique integers, and a target value, find all pairs of integers
from the list that add up to the target.

>>> sorted(integer_pairs([4, 3, 8, 1, 5], target=9))
[(4, 5), (8, 1)]

>>> numbers = list(range(100000))
>>> pairs = list(integer_pairs(numbers, target=100000))
>>> len(pairs)
49999
>>> all(a + b == 100000 for a, b in pairs)
True
"""

import itertools
import time

def timeit(func):
    """
    Decorator to calculate the time taken by the function
    """
    
    def wrapper(*args, **kwargs):
        t1 = time.clock()
        res = func(*args, **kwargs)
        t2 = time.clock()
        print t2 - t1
        return res
    return wrapper

@timeit
def integer_pairs(integers, target):
    
    # create combinations pairs of given integers
    pairs = itertools.combinations(integers, 2)
    
    # Check if the sum of each pair is equal to target
    return [i for i in pairs if i[0] + i[1] == target]
    
import unittest

class TestIntegerPairs(unittest.TestCase):
    
    def testCase1(self):
        n = 1000
        target = 1000
        output = integer_pairs(range(n), target)
        expected = all(a + b == target for a, b in output)
        self.assertEqual(expected, True)
        
        
if __name__ == '__main__':
    pairs = integer_pairs(range(1000), target=1000)
    print pairs
    print all(a + b == 1000 for a, b in pairs)
    unittest.main()