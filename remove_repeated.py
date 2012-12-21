'''
Created on Dec 15, 2012

@author: Praveen Shilavantar
'''

"""
Problem:

Write a function to remove repeated letters from a string, ignoring whitespace
and letter case.

>>> remove_repeated('abc')
'abc'
>>> remove_repeated('abbc')
'abc'
>>> remove_repeated('aAbc')
'abc'
>>> remove_repeated('aBbc')
'aBc'
>>> remove_repeated('abBc')
'abc'
>>> remove_repeated('ab cd')
'ab cd'
>>> remove_repeated('ab  cd')
'ab  cd'
>>> remove_repeated('ab  ccd')
'ab  cd'
>>> remove_repeated('abc cdd')
'abc cd'

This algorithm has linear running time O(n).

"""

def remove_repeated(input_str):
    """
    Remove repeated letters from a string
    """
    str_len = len(input_str) # Length of the string
    start = 0 
    end = 0
    output_str = ''
    while end < str_len:
        start = end
        # Create substring
        while end < str_len and input_str[end] != ' ':
            end += 1
        # Remove repeated chars from substring
        out = remove_duplicate_chars(input_str, start, end)
        output_str += out
        end += 1
    return output_str
    
    
def remove_duplicate_chars(input_str, start, end):
    """
    Remove duplicate chars from the word
    """
    output = ''
    for i in input_str[start:end+1]:
        # Ignore letter case
        if not (i.lower() in output or i.upper() in output):
            output += i
    return output


"""
Unit Test Cases
"""

import unittest

class TestRemoveRepeated(unittest.TestCase):
    
    def testCase1(self):
        """
        >>> remove_repeated('abc')
        'abc'
        """
        input = 'abc'
        output = remove_repeated(input)
        expected = 'abc'
        self.assertEqual(output, expected)

    def testCase2(self):
        """
        >>> remove_repeated('abbc')
        'abc'
        """
        input = 'abbc'
        output = remove_repeated(input)
        expected = 'abc'
        self.assertEqual(output, expected)
        
    def testCase3(self):
        """
        >>> remove_repeated('aAbc')
        'abc'
        """
        input = 'aAbc'
        output = remove_repeated(input)
        expected = 'abc'
        self.assertEqual(output, expected)

    def testCase4(self):
        """
        >>> remove_repeated('aBbc')
        'aBc'
        """
        input = 'aBbc'
        output = remove_repeated(input)
        expected = 'aBc'
        self.assertEqual(output, expected)
        
    def testCase5(self):
        """
        >>> remove_repeated('abBc')
        'abc'
        """
        input = 'abBc'
        output = remove_repeated(input)
        expected = 'abc'
        self.assertEqual(output, expected)
        
    def testCase6(self):
        """
        >>> remove_repeated('ab cd')
        'ab cd'
        """
        input = 'ab cd'
        output = remove_repeated(input)
        expected = 'ab cd'
        self.assertEqual(output, expected)
        
    def testCase7(self):
        """
        >>> remove_repeated('ab  cd')
        'ab  cd'
        """
        input = 'ab  cd'
        output = remove_repeated(input)
        expected = 'ab  cd'
        self.assertEqual(output, expected)
        
    def testCase8(self):
        """
        >>> remove_repeated('ab  ccd')
        'ab  cd'
        """
        input = 'ab  ccd'
        output = remove_repeated(input)
        expected = 'ab  cd'
        self.assertEqual(output, expected)
        
    def testCase9(self):
        """
        >>> remove_repeated('abc cdd')
        'abc cd'
        """
        input = 'abc cdd'
        output = remove_repeated(input)
        expected = 'abc cd'
        self.assertEqual(output, expected)

if __name__ == '__main__':
    text = 'abc cDdd'
    print remove_repeated(text)
    unittest.main()