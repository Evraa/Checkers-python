#Global imports
import random
from collections import deque
from copy import deepcopy
# from guppy import hpy
# from memory_profiler import profile
# h = hpy()
# from copy import deepcopy
#Local imports
from move_logic import where_can_i_move_next
from common import init_board, how_many
from constants import N, DEPTH
from board import Board
from tree import Node, Tree


def construct_full_tree(board, pl):
    '''
        + The main part starts here.
        + this function constructs nodes, node represents a state.
        + state is the board after certain moves.
        + this function returns only the min_max Tree.
        + Inputs: board and a player
        + Outputs: tree
    '''    

    #Crete the Root Node, add it to the tree and the Q
    player = deepcopy(pl)       #just to make sure, no shallow copy occurs
    root = Node(board,player,0)
    tree = Tree(root)
    tree.inc_depth()
    switch = "switch"
    Q = deque()                 #Q for adding nodes to be spanned later
    Q.append(root)              #append the root of course
    Q.append(switch)            #switch: new generation is comming. ie. new level, new depth.
    i = 0                       #for loggs
    new_gen = True              #for tree construction
    
    while len(Q) > 1:
        #LOG
        if i % 1000 == 0:
            print (tree.depth)
        i += 1

        root = Q.popleft()
        if root == "switch":
            #swap players
            player = 1 if player == -1 else -1
            Q.append(switch)
            tree.inc_depth()
            new_gen = True
            if tree.depth == DEPTH:
                break
            continue
        
        possible_moves = where_can_i_move_next(root.board, player)
        
        for pos in possible_moves:
            node = Node (pos[3], player, pos[2]*player)
            tree.append_node(node, root, new_gen)
            new_gen = False
            Q.append(node)
            player_swap = 1 if player == -1 else -1
            score = how_many (pos[3],player_swap)
            if score == 0:
                return tree, node

    return tree, None


def second_main():
    board = init_board(N)
    br = Board(N)
    br.draw_board(board)
    player = 1
    while True:
        tree, win_node = construct_full_tree(board, player)
        if win_node is not None:
            tree.print_tree()
            print (f'Player: {win_node.get_player()} WON')
            break
        tree.print_tree()
        board = tree.update_board(player)
        br.draw_board(board)
        player = 1 if player == -1 else -1
        del tree


second_main()
