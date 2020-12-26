#Global imports
import random
from collections import deque
from copy import deepcopy
import time

#Local imports
from move_logic import where_can_i_move_next
from common import init_board, how_many, non_zeros_count, define_depth
from constants import N, DEPTH, MAX_NEG, MAX_POS
from board import Board
from tree import Node, Tree


def construct_full_tree(board, pl, depth):
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
    this_is_root = True
    start_time, end_time = None, None
    while len(Q) > 1:
        #LOG
        # if i % 1000 == 0:
        #     print (f'Tree depth till now: {tree.depth} \t\tGlobal depth: {depth}')
        # i += 1

        root = Q.popleft()
        if root == "switch":
            #swap players
            player = 1 if player == -1 else -1
            Q.append(switch)
            end_time = time.time()
            if start_time == None:
                tree.inc_depth()
                print("First time, inc depth")
            elif end_time - start_time < 5:
                tree.inc_depth()
                print (f'Tree depth till now: {tree.depth} \t\tTime: {end_time-start_time}')
            else:
                print (f"Time EXC depth: {tree.depth} \t\tTime: {end_time-start_time}\n")

                return tree, None, None
            start_time = time.time()
            new_gen = True
            if tree.depth == depth:
                break
            continue
        
        possible_moves = where_can_i_move_next(root.board, player)
        
        if len(possible_moves) == 0:
            new_cost = MAX_POS if player == 1 else MAX_NEG
            root.update_cost(new_cost)

        for pos in possible_moves:
                
            node = Node (pos[3], player, pos[2]*player)
            tree.append_node(node, root, new_gen)
            new_gen = False
            player_swap = 1 if player == -1 else -1
            score = how_many (pos[3],player_swap)
            if score == 0:
                new_cost = MAX_POS if player == 1 else MAX_NEG
                node.update_cost(new_cost)
            if len(possible_moves) == 1 and this_is_root:
                this_is_root = False
                continue
            else:
                Q.append(node)

    return tree, None, None


def second_main():
    board = init_board(N)
    br = Board(N)
    br.draw_board(board)
    player = 1
    start_time, end_time = None, None
    depth = DEPTH
    player_1_time = 0
    player_2_time = 0
    
    while True:
        
        # if player == 1:
        #     depth = define_depth(depth, player_1_time, player_2_time)

        # start_time = time.time()
        tree, win_node, status = construct_full_tree(board, player, depth)
        # end_time = time.time()
        # if player == 1: 
        #     player_1_time = end_time - start_time
        #     print (f'Player 1 move time: {player_1_time}')
        # if player == -1:
        #     player_2_time = end_time - start_time
        #     print (f'Player 2 move time: {player_2_time}')
        
        # if win_node is not None:
        #     tree.print_tree()
        #     print (f'Player: {win_node.get_player()} WON')
        #     print (f'Status: {status}')
        #     break

        # tree.print_tree()
        board,lost = tree.update_board()
        if lost:
            player_swap = 1 if player == -1 else -1
            print (f'Player: {player_swap} Won: No moves allowed for opponent.')
            del tree
            break
        br.draw_board(board)
        player_swap = 1 if player == -1 else -1
        score = how_many (board,player_swap)
        if score == 0:
            print (f'Player: {player} Won: All pieces are taken.')
            del tree
            break
        player = 1 if player == -1 else -1
        del tree


second_main()
