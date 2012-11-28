'''
Created on Nov 23, 2012

@author: praveen
'''

class Node(object):
    '''
    Node containing a data and a pointer to the next node
    '''

    def __init__(self, value=None):
        '''
        Constructor
        '''
        self._next = None
        self._data = value
        
class LinkedList(object):
    '''
    A Linked List containing a list of nodes
    '''

    def __init__(self):
        '''
        Constructor
        '''
        self.head = Node()
        
    def insertAtFront(self, item):
        '''
        Adding a node at the beginning of the list
        '''
        node = Node(item)
        node._next = self.head._next
        self.head._next = node
        return node
        
    def listNodes(self):
        """
        Display all nodes 
        """
        
        cur_node = self.head
        nodes = ""
        while cur_node:
            # The Head node will be empty; will contain only a pointer to next node
            if cur_node._data:
                nodes += str(cur_node._data) + " "
            cur_node = cur_node._next
        if not nodes:
            print "List is empty"
        print nodes 
        
    def count(self):
        """
        Count of the nodes in the list
        """
        cur_node = self.head
        
        counter = 0
        # Traverse through the list till the end
        while cur_node._next is not None:
            cur_node = cur_node._next
            counter += 1
        return counter
    
    def insertAtEnd(self, item):
        """
        Adding a node at end of the list
        """
        cur_node = self.head
            
        # Traverse through the list till the end
        while cur_node._next is not None:
            cur_node = cur_node._next
        
        node = Node(item)
        node._next = cur_node._next
        cur_node._next = node
        
    def insertAt(self, item, loc):
        """
        Adding a node at the specified location of the list
        """
        list_len = self.count()
        
        if loc > list_len:
            return "Insertion at given location is not possible. \n"
        
        if loc == 1:
            return self.insertAtFront(item)
            
        cur_node = self.head
        
        counter = 0
        # Traverse through the list till the end
        while counter<loc:
            cur_node = cur_node._next
            counter += 1
            
        node = Node(item)
        node._next = cur_node._next
        cur_node._next = node

    def deleteNodeByValue(self, item):
        """
        Delete a node for a given value
        """
        cur_node = self.head
        #import pdb; pdb.set_trace()
        if not cur_node._next:
            return 0
        
        if cur_node._next._data == item:
            self.head._next = cur_node._next._next
            del cur_node
            return 1
                
        while cur_node:
            if cur_node._next and cur_node._next._data == item:
                cur_node._next = cur_node._next._next;
                del cur_node
                return 1
            cur_node = cur_node._next
            
        print "Item not found"
            
    def deleteNode(self, node):
        """
        Delete a node from the list
        """
        cur_node = self.head
                
        while cur_node:
            if cur_node._next and cur_node._next == node:
                cur_node._next = cur_node._next._next;
                del cur_node
                return 1
            cur_node = cur_node._next
            
        print "Node not found"
        
    def deleteAllNodes(self):
        """
        Delete all nodes from the list
        """
        cur_node = self.head
                
        while cur_node:
            self.head._next = cur_node._next
            del cur_node
            cur_node = self.head._next
            
    def reverse(self, new_list):
        """
        Reverse List using new linked list
        """
        cur_node = self.head
        
        while cur_node:
            if cur_node._data:
                new_list.insertAtFront(cur_node._data)
            cur_node = cur_node._next
        return new_list
                    
class Stack(LinkedList):
    """ Stack implementation using Linked List """
    
    def __init__(self):
        LinkedList.__init__(self)

    def push(self, item):
        """
        Push operation
        """
        self.insertAtFront(item)
        
    def pop(self):
        """
        Pop operation
        """
        temp = self.head
        if temp._next:
            data = self.head._next._data
            self.head._next = temp._next._next
            del temp
            return data
        return -1
    
class Queue(LinkedList):
    """ Queue implementation using Linked List """
            
    def __init__(self):
        LinkedList.__init__(self)
        
    def insert(self, item):
        """
        Inserting an item at the end of queue
        """
        self.insertAtEnd(item)
        
    def remove(self):
        """
        Removing an item from the beginning of queue
        """
        temp = self.head
        if temp._next:
            data = self.head._next._data
            self.head._next = temp._next._next
            del temp
            return data
        return -1
        
if __name__ == '__main__':
    l1 = LinkedList()
    
    
    print "reverse a list with new logic"
    l1.insertAtFront('A')
    l1.insertAtFront('B')
    l1.listNodes()
    print l1.count()
    
    print "Checking empty lists"
    l1.deleteNodeByValue('A')
    l1.insertAtFront('Z')
    l1.listNodes()
    l1.deleteNodeByValue('Z')
    l1.listNodes()
    
    print "Adding nodes"
    #for i in range(10):
    #    l1.insertAtFront(i)
    l1.insertAtFront('A')
    l1.insertAtFront('B')
    l1.insertAtFront('C')
    l1.listNodes()
    print l1.count()
    l1.insertAtEnd('D')
    l1.listNodes()
    print l1.count()
    l1.insertAt('E', 3)
    l1.listNodes()
    print l1.count()
   
    print "Deleting nodes"
    l1.deleteNodeByValue('D')
    l1.listNodes()
    print l1.count()
    l1.deleteNodeByValue('C')
    l1.listNodes()
    print l1.count()
    l1.deleteNodeByValue('F')
    node = l1.insertAtFront('F')
    l1.listNodes()
    print l1.count()    
    l1.deleteNode(node)
    l1.listNodes()
    print l1.count()
    l1.deleteNode(node)
    
    print "Reverse a list"
    l2 = LinkedList()
    l1.reverse(l2)
    l2.listNodes()
    print l2.count()
    
    print "Deleting all nodes"
    l1.deleteAllNodes()
    l1.listNodes()
    print l1.count()
    
    print "Stack Operations"
    s1 = Stack()
    s1.push('P')
    s1.push('R')
    s1.push('A')
    s1.push('Z')
    s1.listNodes()
    print s1.pop()
    s1.listNodes()
    
    print "Queue Operations"
    q1 = Queue()
    q1.insert('P')
    q1.insert('R')
    q1.insert('A')
    q1.insert('Z')
    q1.listNodes()
    print q1.remove()
    q1.listNodes()
    print q1.remove()
    print q1.remove()
    print q1.remove()
    q1.listNodes()
    print q1.remove()'''
Created on Nov 23, 2012

@author: praveen
'''

class Node(object):
    '''
    Node containing a data and a pointer to the next node
    '''

    def __init__(self, value=None):
        '''
        Constructor
        '''
        self._next = None
        self._data = value
        
class LinkedList(object):
    '''
    A Linked List containing a list of nodes
    '''

    def __init__(self):
        '''
        Constructor
        '''
        self.head = Node()
        
    def insertAtFront(self, item):
        '''
        Adding a node at the beginning of the list
        '''
        node = Node(item)
        node._next = self.head._next
        self.head._next = node
        return node
        
    def listNodes(self):
        """
        Display all nodes 
        """
        cur_node = self.head
        nodes = ""
        while cur_node:
            # The Head node will be empty; will contain only a pointer to next node
            if cur_node._data:
                nodes += str(cur_node._data) + " "
            cur_node = cur_node._next
        if not nodes:
            print "List is empty"
        print nodes 
        
    def count(self):
        """
        Count of the nodes in the list
        """
        cur_node = self.head
        
        counter = 0
        # Traverse through the list till the end
        while cur_node._next is not None:
            cur_node = cur_node._next
            counter += 1
        return counter
    
    def insertAtEnd(self, item):
        """
        Adding a node at end of the list
        """
        cur_node = self.head
            
        # Traverse through the list till the end
        while cur_node._next is not None:
            cur_node = cur_node._next
        
        node = Node(item)
        node._next = cur_node._next
        cur_node._next = node
        
    def insertAt(self, item, loc):
        """
        Adding a node at the specified location of the list
        """
        list_len = self.count()
        
        if loc > list_len:
            return "Insertion at given location is not possible. \n"
        
        if loc == 1:
            return self.insertAtFront(item)
            
        cur_node = self.head
        
        counter = 0
        # Traverse through the list till the end
        while counter<loc:
            cur_node = cur_node._next
            counter += 1
            
        node = Node(item)
        node._next = cur_node._next
        cur_node._next = node

    def deleteNodeByValue(self, item):
        """
        Delete a node for a given value
        """
        cur_node = self.head
                
        while cur_node:
            if cur_node._next and cur_node._next._data == item:
                cur_node._next = cur_node._next._next;
                del cur_node
                return 1
            cur_node = cur_node._next
            
        print "Item not found"
            
    def deleteNode(self, node):
        """
        Delete a node from the list
        """
        cur_node = self.head
                
        while cur_node:
            if cur_node._next and cur_node._next == node:
                cur_node._next = cur_node._next._next;
                del cur_node
                return 1
            cur_node = cur_node._next
            
        print "Node not found"
        
    def deleteAllNodes(self):
        """
        Delete all nodes from the list
        """
        cur_node = self.head
                
        while cur_node:
            self.head._next = cur_node._next
            del cur_node
            cur_node = self.head._next
            
    def reverse(self, new_list):
        """
        Reverse List using new linked list
        """
        cur_node = self.head
        
        while cur_node:
            if cur_node._data:
                new_list.insertAtFront(cur_node._data)
            cur_node = cur_node._next
        return new_list
            
if __name__ == '__main__':
    l1 = LinkedList()
    
    print "Adding nodes"
    #for i in range(10):
    #    l1.insertAtFront(i)
    l1.insertAtFront('A')
    l1.insertAtFront('B')
    l1.insertAtFront('C')
    l1.listNodes()
    print l1.count()
    l1.insertAtEnd('D')
    l1.listNodes()
    print l1.count()
    l1.insertAt('E', 3)
    l1.listNodes()
    print l1.count()
   
    print "Deleting nodes"
    l1.deleteNodeByValue('B')
    l1.listNodes()
    print l1.count()
    l1.deleteNodeByValue('C')
    l1.listNodes()
    print l1.count()
    l1.deleteNodeByValue('F')
    node = l1.insertAtFront('F')
    l1.listNodes()
    print l1.count()    
    l1.deleteNode(node)
    l1.listNodes()
    print l1.count()
    l1.deleteNode(node)
    
    print "Reverse a list"
    l2 = LinkedList()
    l1.reverse(l2)
    l2.listNodes()
    print l2.count()
    
    print "Deleting all nodes"
    l1.deleteAllNodes()
    l1.listNodes()
    print l1.count()
