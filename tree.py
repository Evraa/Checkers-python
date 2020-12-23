#Global imports
from collections import deque

#Local imports


class Node(object):
    """
        + A node in Tree
    """
    def __init__ (self, board, player, cost):
        self.board = board
        self.player = player
        self.parent = None
        self.children = []
        self.cost = cost
        self.level = 0
        self.cum_cost = 0

    def print_node (self, cum = False):
        if cum:
            if self.cum_cost > 1 or self.cum_cost <-1: 
                print ("HERE YA EEEEEEEEEEEEv")
            print (f'Level: {self.level} \tCost: {self.cum_cost}')
        else:
            print (f'Level: {self.level} \tCost: {self.cost}')
            

class Tree(object):
    """
        + Implementing a tree class for searching and pruning.
    """
    def __init__ (self, node):
        self.root = node
        self.depth = 0
        
    def get_children(self, node):
        if len(node.children) > 0:
            return node.children
        return None

    def append_node (self,node,parent):
        parent.children.append(node)
        node.parent = parent
        node.level = self.depth
        node.cum_cost = node.cost + parent.cost
        return

    def inc_depth(self):
        self.depth += 1

    def print_tree (self, cum = False):
        Q = deque()
        Q.append(self.root)
        while len(Q) >= 1:
            node = Q.popleft()
            node.print_node(cum)
            for child in node.children:
                Q.append(child)

    def minmax (self, player):
        