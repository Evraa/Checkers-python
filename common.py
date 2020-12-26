#Global imports
from math import ceil, floor
from numpy import random
from copy import deepcopy
#Local imports and Global Variables
from constants import N, MIN_DEPTH
# from move_logic import where_can_i_move_next
import move_logic
from board import Board

def init_board(N):
    '''
        + Initialize the NxN board with the appropriate pieces.
        + 1: player 1
        + -1: player 2
    '''
    board = []
    line_1,line_1_2 = [],[]
    line_2,line_2_2 = [],[]
    zeros = []
    for i in range (N):
        if i%2 == 0:
            line_1.append(1)
            line_1_2.append(-1)
            line_2.append(0)
            line_2_2.append(0)
        else:
            line_1.append(0)
            line_1_2.append(0)
            line_2.append(1)
            line_2_2.append(-1)
        zeros.append(0)
    if N%2 == 1:
        line_1, line_2 = line_2, line_1
        line_1_2, line_2_2 = line_2_2, line_1_2
        
    for i in range (N):
        if i%2 == 0 and i < ceil(N/2)-1:
            board.append(list(line_2))
        elif i%2 == 1 and i< ceil(N/2)-1: 
            board.append(list(line_1))

        elif i%2 == 0 and i > floor(N/2):
            board.append(list(line_2_2))
        elif i%2 == 1 and i > floor(N/2): 
            board.append(list(line_1_2))
        else:
            board.append(list(zeros))
    return board

def rand_init(N):
    '''
        + init random board of size NxN for testing purposess
    '''
    board = init_board(N)
    for i in range (0,N):
        for j in range (N):
            if((i%2) != ((j+1)%2) and N%2 == 0) or ((i%2) != (j%2) and N%2 == 1):
                continue
            # elif i%2==1:
            elif i<3 or i > 4:
                board[i][j] = 0
            else:
                ev = random.randint(3)
                if i < N//2: 
                    board[i][j] = (ev)
                else:
                    board[i][j] = -(ev)
    return board

def spec_esight():
    zeros = [0,0,0,0,0,0,0,0]

    return [ list(zeros),
            [-1,0,1,0,1,0,-1,0],
            [0,-1,0,0,0,0,0,0],
            list(zeros),
            list(zeros),
            list(zeros),
            [0,1,0,1,0,1,0,1],
            list(zeros)
    ]

def how_many (board,player):
    result = 0
    for i in range(N):
        for j in range(N):
            if player == 1:
                if board[i][j] >= player:
                    result += 1
            else:
                if board[i][j] <= player:
                    result += 1
    return result
            



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
    possible_moves = move_logic.where_can_i_move_next(board=board, player=player)
    if len(possible_moves) == 0:
        return board, None, True
    if approach == 'random':
        return random_move(possible_moves, board)
    elif approach == 'greedy':
        return greedy_move(possible_moves, board)

    else:
        print (f'What is this! {approach}')

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

def non_zeros_count(board):
    non_zeros = 0
    for i in range(N):
        for j in range(N):
            if board[i][j] != 0:
                non_zeros+=1
    return non_zeros

def define_depth(orig_depth, pl_1_time, pl_2_time):
    if pl_1_time == 0 and pl_2_time == 0:
        return orig_depth

    if pl_1_time + pl_1_time > 30:
        if orig_depth == MIN_DEPTH:
            print("Time exceeds limit, but Can Not decrease The depth")
            return
        else:
            print("Time exceeds limit, Decrease The depth")
            return orig_depth - 1
    elif pl_1_time + pl_1_time > 0.05:
        #less than 30 seconds
        print ("Time is Good. Increase the depth")
        return orig_depth+1
    else:
        print("This move is way too fast, it's not safe to increase the depth.")
        return orig_depth

def evaluate(board):
    if board == None:
        print ("Error: none board is requested for evaluation!")
        return None
    return (int)(sum(map(sum,board)))
