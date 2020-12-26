#Global imports
from collections import deque
from numpy import random
from copy import deepcopy
#Local imports
from constants import MAX_POS, MAX_NEG


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
        self.v = None               #a-b algo
        self.alpha = None           #a-b algo
        self.beta = None            #a-b algo
        self.pruned = False         #a-b algo

    def get_player(self):
        return self.player

    def print_node (self, cum = False):
        '''
            + Print the node ingredients.
        '''
        if self.parent is None:
            print (f'Level: {self.level} \tCost: {self.cum_cost} \tMy id is: {self.id} \tROOT\t P: {self.pruned}')
        elif self.sibling is None:
            print (f'Level: {self.level} \tCost: {self.cum_cost} \tMy id is: {self.id} \tNo Direct Sibling, The Youngest! \tMy Dad id is {self.parent.id}\t P: {self.pruned}')
        else:   
            print (f'Level: {self.level} \tCost: {self.cum_cost} \tMy id is: {self.id} \tMy Direct Sibling id is {self.sibling.id} \tMy Dad id is {self.parent.id}\t P: {self.pruned}')
    
    def get_children_cost(self):
        '''
            + Get children's cost values in a list, to compare easily
        '''
        costs = []
        for child in self.children:
            cost = [child.cost, child.board]
            costs.append(cost)
        return costs
    
    def update_cost(self, cost):
        self.cost = cost


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

    def min_max(self):
        '''
            + The min max algorithm.
            + starting from nodes at the level previous to the last one. (depth - 1)
            + and going upwards, update each node according to its player (max/min)
            + go up, and repeat, until the roor is present, then return its next move.

            +Output: Next best move
        '''
        for i in reversed(range(len(self.level_ptrs)-1)):
            head = self.level_ptrs[i]

            while head.sibling != None or head.parent == None:
                if head.player == -1:
                    if len(head.children) == 0:
                        head.cost = MAX_NEG #this move guarantee win
                    else:
                        miny = min(head.get_children_cost(), key=lambda x: x[0])
                        head.cost += miny[0]
                    if i == 0:
                        return miny[1]
                else:
                    if len(head.children) == 0:
                        head.cost = MAX_POS #this move guarantee win
                    else:
                        maxy = max(head.get_children_cost(), key=lambda x: x[0])
                        head.cost += maxy[0]
                    if i == 0:
                        return maxy[1]
                head = head.sibling
                
                    

    def update_board (self):
        '''
            + It calls the min_max algorithm, and just checks if root can easily pick without going deeper.
        '''
        if len(self.root.children) == 0:
            return self.root.board, True
        elif len(self.root.children) == 1:
            return self.root.children[0].board, False
        return  self.min_max(), False

    def reset_nodes (self):
        '''
            + In order to re-prune the tree.
            + One gotta delete previous values of v,alpha, and beta.
        '''
        for start_point in self.level_ptrs[:-1]:
            while start_point != None:
                start_point.v = None
                start_point.alpha = None
                start_point.beta = None
                start_point = start_point.sibling

    def prune(self):
        '''
            + a-b pruning algorithm
            + starting from level (depth-1)
            + update current value and direct parent
            + and if that parent is the last child, then update its parent, and so on.
            + and if root is reached, then terminate.
        '''
        self.reset_nodes()
        head_least_level = self.level_ptrs[-2]
        player = head_least_level.player
        while head_least_level != None:
            if head_least_level.pruned:
                head_least_level = head_least_level.sibling
                continue
            prune_my_kids = False
            for child in (head_least_level.children):
                #prune the upcoming child?
                if prune_my_kids:
                    child.pruned = True
                    continue
                if player == 1:
                    #Update V
                    if head_least_level.v == None or\
                        head_least_level.v < child.cost: #look to maxi
                        head_least_level.v = child.cost
                    #update alpha ~ Max
                    head_least_level.alpha = head_least_level.v
                    #should we prune?
                    if head_least_level.beta != None and\
                        head_least_level.alpha != None and\
                        head_least_level.alpha > head_least_level.beta:
                        #PRUNE
                        prune_my_kids = True

                if player == -1:
                    #Update V
                    if head_least_level.v == None or\
                        head_least_level.v > child.cost: #look to mini
                        head_least_level.v = child.cost
                    #update beta ~ Min
                    head_least_level.beta = head_least_level.v
                    #should we prune?
                    if head_least_level.beta != None and \
                        head_least_level.alpha != None and\
                        head_least_level.alpha > head_least_level.beta:
                        #PRUNE
                        prune_my_kids = True
                
            direct_child =head_least_level
            next_sib = head_least_level.sibling

            while True:
                direct_dad = direct_child.parent
                if direct_dad == None: #this is a root, terminate
                    return

                #update dad's v and beta
                if (direct_dad.v == None and direct_dad.player == -1)\
                    or (direct_dad.v != None and direct_child.v != None\
                        and direct_dad.v > direct_child.v and direct_dad.player == -1): #he sure wants to mini
                    direct_dad.v = direct_child.v
                    direct_dad.beta = direct_dad.v
                    
                if (direct_dad.v == None and direct_dad.player == 1)\
                    or (direct_dad.v != None and direct_child.v != None\
                    and direct_dad.v < direct_child.v and direct_dad.player == 1):
                    direct_dad.v = direct_child.v
                    direct_dad.alpha = direct_dad.v
                        
                #update children's alpha/beta
                if direct_dad.alpha != None or direct_dad.beta != None:
                    for child in direct_dad.children:
                        if direct_dad.alpha != None: child.alpha = direct_dad.alpha 
                        if direct_dad.beta  != None: child.beta = direct_dad.beta 

                #check if dad can prune!
                if direct_dad.alpha != None and direct_dad.beta != None and direct_dad.alpha > direct_dad.beta\
                    and direct_child != direct_dad.children[-1]:
                    prune_now = False
                    for child in direct_dad.children:
                        if prune_now:
                            child.pruned = True
                            continue
                        if child == direct_child:
                            prune_now = True

                #update direct dad!
                if direct_child != direct_child.parent.children[-1]:
                    break #don't inform its dad
                else:
                    direct_child = direct_dad #let's dig further


            head_least_level = next_sib