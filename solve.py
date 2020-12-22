#Global imports
import random
# from copy import deepcopy
#Local imports
from move_logic import where_can_i_move_next
from common import init_board, how_many
from constants import N
from board import Board


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
    return move[3]
    return

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
    
    return best_move[3]
    return

def play_player(approach, player, board):
    '''
        + Given a certain approach, decide on the next state of the game.
        + board is updated by reference
    '''
    possible_moves = where_can_i_move_next(board=board, player=player)
    if approach == 'random':
        return random_move(possible_moves, board)
    elif approach == 'greedy':
        return greedy_move(possible_moves, board)

    else:
        print (f'What is this! {approach}')


def mian_game_loop (verbose=False):
    board = init_board(N)
    if verbose:
        br = Board(N)
        br.draw_board(board)
    
    game_end = 0
    player = 1
    while game_end == 0:
        
        board = play_player(approach='random', player=player, board=board)
        
        player = -1
        neg = how_many(board, player)
        if neg == 0:
            game_end = 1
            break
        if verbose:
            br.draw_board(board)
        board = play_player(approach='random', player=player, board=board)
        player = 1
        pos = how_many(board, player)
        if pos == 0:
            game_end = -1
            break
        if verbose:
            br.draw_board(board)
    print (f'Player: {game_end} WON')

mian_game_loop(False)