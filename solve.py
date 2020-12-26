#Global imports
import random
from collections import deque
from copy import deepcopy
import time

#Local imports
from move_logic import where_can_i_move_next
from common import init_board, how_many, non_zeros_count, define_depth,evaluate
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
    root = Node(board,player,evaluate(board))
    tree = Tree(root)
    tree.inc_depth()
    switch = "switch"
    Q = deque()                 #Q for adding nodes to be spanned later
    Q.append(root)              #append the root of course
    Q.append(switch)            #switch: new generation is comming. ie. new level, new depth.
    # i = 0                       #for loggs
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
                # print("First time, inc depth")
            elif end_time - start_time < 0.5:
                tree.inc_depth()
                # print (f'Tree depth till now: {tree.depth} \t\tTime: {end_time-start_time}')
            else:
                print (f"Time EXC depth: {tree.depth} \t\tTime: {end_time-start_time}\n")

                return tree
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
                
            node = Node (pos[3], player, pos[2])
            tree.append_node(node, root, new_gen)
            new_gen = False
            player_swap = 1 if player == -1 else -1
            score = how_many (pos[3],player_swap)
            if score == 0:
                new_cost = MAX_POS if player == 1 else MAX_NEG
                node.update_cost(new_cost)
            if len(possible_moves) == 1 and this_is_root:
                Q.append(node)
                return tree
            else:
                Q.append(node)
        this_is_root = False

    return tree


def go_greedy(board, player):
    print("Repeated! GO GREEDY \n")
    possible_moves = where_can_i_move_next(board, player)
    max_win = 0
    best_move = None
    for pos in possible_moves:
        if abs(pos[2]) > max_win:
            best_move = pos
    if max_win == 0:
        best_move = random.choice(possible_moves)
    
    return best_move[3]

def second_main():
    board = init_board(N)
    br = Board(N)
    br.draw_board(board)
    player = 1
    depth = DEPTH
    pl_1_prev_move,pl_2_prev_move = None, None
    pl_1_prev_prev_move, pl_2_prev_prev_move = None, None
    
    while True:
        
        
        tree = construct_full_tree(board, player, depth)
        
        
        board, lost = tree.update_board()

        if player == 1:
            if pl_1_prev_prev_move == None and pl_1_prev_move != None:
                pl_1_prev_prev_move = pl_1_prev_move
            if pl_1_prev_move == None:
                pl_1_prev_move = board

            if pl_1_prev_move != None and pl_1_prev_prev_move != None:
                if board == pl_1_prev_prev_move:
                    #GO GREEDY
                    board = go_greedy(pl_1_prev_move, player)
                pl_1_prev_prev_move = pl_1_prev_move
                pl_1_prev_move = board

        if player == -1:
            if pl_2_prev_prev_move == None and pl_2_prev_move != None:
                pl_2_prev_prev_move = pl_2_prev_move
            if pl_2_prev_move == None:
                pl_2_prev_move = board

            if pl_2_prev_move != None and pl_2_prev_prev_move != None:
                if board == pl_2_prev_prev_move:
                    #GO GREEDY
                    board = go_greedy(pl_2_prev_move, player)
                pl_2_prev_prev_move = pl_2_prev_move
                pl_2_prev_move = board
        
        # tree.print_tree()
        
        if lost:
            player_swap = 1 if player == -1 else -1
            print (f'Player: {player_swap} Won: No moves allowed for opponent.')
            del tree
            break
        # br.draw_board(board)
        player_swap = 1 if player == -1 else -1
        score = how_many (board,player_swap)
        if score == 0:
            print (board)
            print (f'Player: {player} Won: All pieces are taken.')
            del tree
            break
        player = 1 if player == -1 else -1
        del tree


second_main()
