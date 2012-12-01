'''
Created on Nov 13, 2012

@author: praveen
'''

"""
Problem:

Write a function that reverses the order of the words in a string. 
For instance, your function should transform the string "Do or do not, 
there is no try." to "try. no is there not, do or Do". Assume that all
words are space delimited and treat punctuation the same as letters. 
"""

import cProfile
import array

def reverseWords(input_str):
    input_arr = array.array('c', input_str)
    arr_len = len(input_str)
    start = 0
    end = 0
    reverseString(input_arr, 0, arr_len-1)
    while (end < arr_len):
        start = end
        try:
            while input_arr[end] != " ":
                end += 1
        except IndexError:
            pass
        reverseString(input_arr, start, end-1)
        end += 1
    print input_arr.tostring()
    
def reverseString(str_arr, start, end):
    temp = ""     
    while end > start:
        temp = str_arr[start]
        str_arr[start] = str_arr[end]
        str_arr[end] = temp
        start += 1
        end -= 1
        
if __name__ == '__main__':
    input_str = "Do or do not, there is no try."
    cProfile.run("reverseWords(input_str)")
    
