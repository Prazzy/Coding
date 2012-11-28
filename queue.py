'''
Created on Nov 27, 2012

@author: praveen
'''

class Queue(object):
    """ Queue Implementation Using Python List"""

    def __init__(self):
        self._list = []
        
    def insert(self, item):
        """ Insert an item into queue """
        self._list.insert(0, item)
        
    def remove(self):
        """ Remove an item from the queue """
        if not self.isEmpty():
            return -1
        return self._list.pop()
    
    def isEmpty(self):
        """ Check if the queue is empty """
        if not len(self._list):
            return False
        return True
        
if __name__ == '__main__':
    q1 = Queue()
    q1.insert('P')
    q1.insert('R')
    q1.insert('A')
    q1.insert('Z')
    print q1.remove()
    print q1.remove()
    print q1.remove()
    print q1.remove()
    print q1.remove()
    
    
