#Global imports
import random
from collections import deque

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

def random_move(possible_moves, board):
    '''
        + The first approach of playing, is randomly pick a move.
        + possible_moves[i] = [(start) (end) cost [new board] ]
        + Inputs:
            + A reference to the board that gets updated
        + Output:
            + None, cuz possible_moves is checked before it is sent.
    '''
    move = random.choice(possible_moves)
    return move[3], move[0], None
    

def greedy_move(possible_moves, board):
    '''
        + Second approach is greedely choose a move upon the value obtained from it,
        + if all is zero then pick randomly
    '''
    max_win = 0
    best_move = None
    for pos in possible_moves:
        if pos[2] > max_win:
            best_move = pos
    if max_win == 0:
        best_move = random.choice(possible_moves)
    
    return best_move[3], best_move[0], None
    

def play_player(approach, player, board):
    '''
        + Given a certain approach, decide on the next state of the game.
        + board is updated by reference
    '''
    possible_moves = where_can_i_move_next(board=board, player=player)
    if len(possible_moves) == 0:
        return board, None, True
    if approach == 'random':
        return random_move(possible_moves, board)
    elif approach == 'greedy':
        return greedy_move(possible_moves, board)

    else:
        print (f'What is this! {approach}')


def construct_full_tree(board):
    '''
        + The main part starts here.
        + this function constructs nodes, node represents a state.
        + state is the board after certain moves.
        + this function returns only the min_max Tree.
        + Inputs: board
        + Outputs: tree
    '''    
    player = 1
    #Crete the Root Node, add it to the tree and the Q
    root = Node(board,player,0)
    tree = Tree(root)
    tree.inc_depth()
    switch = "switch"
    Q = deque()
    Q.append(root)
    Q.append(switch)
    flag = False
    i = 0
    new_gen = True
    while len(Q) > 1:
        if i % 1000 == 0:
            print (tree.depth)
        i += 1
        # print (f'Q length: {len(Q)}\t Tree Depth: {tree.depth}')
        root = Q.popleft()
        if root == "switch":
            player = 1 if player == -1 else -1
            Q.append(switch)
            tree.inc_depth()
            new_gen = True
            if tree.depth == DEPTH and False:
                break
            continue
        
        possible_moves = where_can_i_move_next(root.board, player)
        
        for pos in possible_moves:
            # if pos[2] == 2 or pos[2]==-2:
            #     # flag = True
            #     input (f'Tree level with the first Cost occur: {tree.depth}')
            #     tree.print_tree(True)
            node = Node (pos[3], player, pos[2]*player)
            tree.append_node(node, root, new_gen)
            new_gen = False
            Q.append(node)
            player_swap = 1 if player == -1 else -1
            score = how_many (pos[3],player_swap)
            if score == 0:
                tree.print_tree()
                input("We've got a winner")

        # if flag:
        #     break
        
    return tree


def second_main():
    board = init_board(N)
    br = Board(N)
    br.draw_board(board)
    tree = construct_full_tree(board)
    tree.print_tree()
    # player = 1
    # while True:
    #     tree = construct_full_tree(board)
    #     tree.print_tree()
    #     # tree.minmax(player = player)
    #     player = 1 if player == -1 else -1

second_main()

def main_game_loop (verbose=False):
    board = init_board(N)
    if verbose:
        br = Board(N)
        br.draw_board(board)
    
    game_end = 0
    player = 1
    while game_end == 0:
        
        board,last,no_move = play_player(approach='greedy', player=player, board=board)
        if no_move:
            game_end = -2
            break
        player = -1
        neg = how_many(board, player)
        if neg == 0:
            game_end = 1
            break
        if verbose:
            board[last[0]][last[1]] = 4
            br.draw_board(board)


        board,last,no_move = play_player(approach='greedy', player=player, board=board)
        if no_move:
            game_end = 2
            break
        player = 1
        pos = how_many(board, player)
        if pos == 0:
            game_end = -1
            break
        if verbose:
            board[last[0]][last[1]] = 4
            br.draw_board(board)
    print (f'Player: {game_end} WON')

# while True:
    # if i%100 == 0:
    #     print (h.heap())
# while True:
#     main_game_loop()