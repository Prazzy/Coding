'''
Created on Nov 17, 2012

@author: praveen
'''

"""
Problem:

Syntax Checking

Approach:

- Compare each char from left of the string with each char from right of the string (use corresponding syntax chars for comparison)
- if comparison fails, break
- ignore other chars except defined syntax chars 

Time Analysis:

Worst case -> O(n) for first loop and O(n/2) for second loop so total is O(n*n/2) = O(n2) i.e., Big Oh n Squared (quadratic)

"""

CHARS_DICT = {'[':']', '(':')', '{':'}'}

def checkSyntax(input_str):
    length = len(input_str)
    i = 0
    k = length - 1
    
    valid_left_chars = CHARS_DICT.keys()
    valid_right_chars = CHARS_DICT.values()
    
    while i < length:
        char = input_str[i]
        
        if char not in valid_left_chars:
            i = i + 1
            continue
        
        while k >= i:
            opp_char = CHARS_DICT[char]
            cur_char = input_str[k]
            if cur_char in valid_right_chars:
                if cur_char == opp_char:
                    i = i + 1
                    k = k -1
                    break
                else:
                    return -1
            elif cur_char in valid_left_chars:
                return -1
            else:
                k = k - 1
                continue
            
    return 1
        
if __name__ == '__main__':
    input_str = "[ { (  ) } ]"
    print checkSyntax(input_str)
