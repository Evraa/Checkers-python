#Global imports
from collections import deque
from numpy import random
#Local imports


class Node(object):
    """
        + A node in Tree
        + Ingredients:
            + board state
            + player .. not so important as the level (odd/even) may indicate it
            + parent, a pointer to parent node, yet not used, I am just uploading
                logs with it.
            + children a list of all the children of this node.
            + cost, this state (move) cost itself
            + level same as the depth, called level cuz a node doesn't know the depth of the tree
            + cum_cost the commulitave cost from the root down to that node
            + sibling, the first right node in the same level, whether it was from the 
                same parent or not.
            + min_max_cost, the cost due to applying the min_max algorithm
            + id, every node has a unique id
    """
    def __init__ (self, board, player, cost):
        self.board = board          #at init
        self.player = player        #at init
        self.cost = cost            #at init
        self.parent = None          #at append
        self.children = []          #when appended to it
        self.level = 0              #at append
        self.cum_cost = 0           #at append
        self.sibling = None         #at append
        self.min_max_cost = None    #at min_max
        self.id = None              #at append

    def get_player(self):
        return self.player

    def print_node (self, cum = False):
        '''
            + Print the node ingredients.
        '''
        if self.parent is None:
            print (f'Level: {self.level} \tCost: {self.cum_cost} \tMy id is: {self.id} \tROOT')
        elif self.sibling is None:
            print (f'Level: {self.level} \tCost: {self.cum_cost} \tMy id is: {self.id} \tNo Direct Sibling, The Youngest! \tMy Dad id is {self.parent.id}')
        else:   
            print (f'Level: {self.level} \tCost: {self.cum_cost} \tMy id is: {self.id} \tMy Direct Sibling id is {self.sibling.id} \tMy Dad id is {self.parent.id}')
        

class Tree(object):
    """
        + Implementing a tree class for searching and pruning.
        + Ingredients:
            + root
            + depth, global variable, only incremented
            + level_ptrs: pointers to the start of each level
            + ids: just for logging, nothing important with the algorithm
            + last_sib: used for appending
    """
    
    def __init__ (self, node):
        ev = random.randint(100000) #for root
        self.root = node            #The ROOT
        self.root.id = ev           
        self.depth = 0              
        self.level_ptrs = []        
        self.level_ptrs.append(self.root)
        self.ids = []
        self.ids.append(ev)
        self.last_sib = None

    def get_children(self, node):
        if len(node.children) > 0:
            return node.children
        return None

    def append_node (self, node, parent, new_level = False):
        '''
            + Append a node to the family.
            + Check if its the first child of a generation!
            + Assign its parent and assign it to a parent
            + Assign it to a sibling and assign it to be the last sibling
        '''
        #Give it an id
        ev = random.randint(100000)
        while ev in self.ids:
            ev = random.randint(100000)
        self.ids.append(ev)
        node.id = ev
        #Am I the oldest of my siblings?
        if new_level:
            self.level_ptrs.append(node)
            self.last_sib = node
        #Assign me to a younger bro
        elif self.last_sib != None:
            self.last_sib.sibling = node
            self.last_sib = node
        #Add me to the parent's kids
        parent.children.append(node)
        #Assign me a dad
        node.parent = parent
        #my level?
        node.level = self.depth
        #my cummulitave cost?
        node.cum_cost = node.cost + parent.cum_cost
        return


    def inc_depth(self):
        self.depth += 1

    def print_tree (self, cum = False):
        Q = deque()
        Q.append(self.root)
        level = 0
        while len(Q) >= 1:
            node = Q.popleft()
            if node.level == level:
                print ("The Oldest Bro is here!")
                level += 1
            node.print_node(cum)
            for child in node.children:
                Q.append(child)

    def update_board (self, player):
        pass