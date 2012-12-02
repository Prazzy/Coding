'''
Created on Dec 1, 2012

@author: praveen
'''

COUNT = 0

class Node(object):
    """
    Binary Tree Node representation
    """

    def __init__(self, data=None):
        self.left = None
        self.right = None
        self.data = data
        self.items = []
        
    def insert(self, data):
        """ Insert a node into a binary tree """
        if data < self.data:
            if self.left is None:
                self.left = Node(data)
                print self.left, data
            else:
                self.left.insert(data)
        else:
            if self.right is None:
                self.right = Node(data)
                print self.right, data
            else:
                self.right.insert(data)
                
    def printTree(self):
        """ Display a tree in an in-order fashion (Left nodes first, root node next and then right node)"""
        if self.left:
            self.left.printTree()
        print self.data,
        if self.right:
            self.right.printTree()
            
    def printTreePreOrder(self):
        """ Display a tree in an in-order fashion (Left nodes first, root node next and then right node)"""
        print self.data,
        if self.left:
            self.left.printTreePreOrder()
        if self.right:
            self.right.printTreePreOrder()
            
    def getItems(self, root):
        if root is None:
            return 
        self.items.append(root.data)
        if self.left:
            self.getItems(root.left)
        if self.right:
            self.getItems(root.right)
            
    def count(self):
        self.items = []
        root = self
        self.getItems(root)
        return len(self.items), self.items
    
    def printTreePostOrder(self):
        """ Display a tree in an in-order fashion (Left nodes first, root node next and then right node)"""
        if self.left:
            self.left.printTreePostOrder()
        if self.right:
            self.right.printTreePostOrder()
        print self.data,
            
    def findNode(self, data, parent=None):
        """ Lookup a node """
        if data == self.data:
            return self, self.data, parent
        if data < self.data:
            if self.left is None:
                return None, -1, None
            return self.left.findNode(data, self)
        else:
            if self.right is None:
                return None, -1, None
            return self.right.findNode(data, self)
            
    def replaceNodeInParent(self, parent, new_value=None):
        if parent.left == self:
            parent.left = new_value
        elif parent.right == self:
            parent.right = new_value
            
    def deleteNode(self, data, parent=None):
        
        if data < self.data:
            self.left.deleteNode(data, self)
        elif data > self.data:
            self.right.deleteNode(data, self)
        else:
            if self.left and self.right:
                parent = self
                successor = self.right
                while successor.left:
                    parent = successor
                    successor = successor.left
                self.data = successor.data
                if parent.left == successor:
                    parent.left = successor.left
                else:
                    parent.right = successor.right
                
                
                self.replaceNodeInParent(parent, self.left)
            if self.left or self.right:
                self.replaceNodeInParent(parent, self.left or self.right)
            else:
                self.replaceNodeInParent(parent, None)
                
    def getHeight(self, node=-1):
        if node == -1:
            node = self
        if node is None:
            return 0
        return 1 +  max(self.getHeight(node.left), self.getHeight(node.right))
            

if __name__ == '__main__':
    root = Node(8)
    print root, 8
    root.insert(3)
    root.insert(10)
    print "\n Size of a tree"
    print root.count()
    print root.findNode(10)
    root.insert(1)
    root.insert(6)
    root.insert(4)
    root.insert(7)
    root.insert(14)
    root.insert(13)
    root.printTree()
    print "\n Size of a tree"
    print root.count()
    print root.findNode(6)
    print "\nDeleting node having a single child node"
    root.deleteNode(14)
    root.printTree()
    print "\nDeleting node having both left and right nodes"
    root.deleteNode(3)
    root.printTree()
    print "\nDeleting leaf node"
    root.deleteNode(1)
    root.printTree()
    print "\nPreorder traversal"
    root.printTreePreOrder()
    print "\nPostorder traversal"
    root.printTreePostOrder()
    print "\nHeight of teh tree"
    print root.getHeight()
    
