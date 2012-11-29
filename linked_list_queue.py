'''
Created on Nov 28, 2012

@author: praveen
'''


class Node(object):
    """A class to represent a queue element """

    def __init__(self, item=None):
        self.data = item
        self.next = None

class LinkedListQueue(object):
    """ Queue implementation using Linked List """

    def __init__(self):
        self.head = Node()
        self.tail = Node()
        
    def insert(self, item):
        """ Insert an item into a queue """
        node = Node(item)
        if self.head.next == None:
            self.head.next = node
        else:
            self.tail.next.next = node
        self.tail.next = node
    
    def remove(self):
        """ Remove an item from a queue """
        
        temp = self.head
        if temp.next == None:
            return -1
        
        if temp.next == self.tail.next:
            data = temp.next.data
            self.head.next = self.tail.next = None
            del temp
            return data
        data = temp.next.data
        self.head.next = self.head.next.next
        del temp
        return data

if __name__ == '__main__':
    l1 = LinkedListQueue()
    print l1.remove()
    l1.insert('P')
    l1.insert('R')
    l1.insert('A')
    l1.insert('Z')
    print l1.remove()
    print l1.remove()
    print l1.remove()
    print l1.remove()
    print l1.remove()
