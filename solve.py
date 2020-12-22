#Global imports
import random
from copy import deepcopy
#Local imports
from move_logic import where_can_i_move_next
from common import rand_init, init_board, spec_esight
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
    board = deepcopy(move[3])
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
    
    board = deepcopy(best_move[3])
    return

def play_player(approach, player, board, verbose=False):
    '''
        + Given a certain approach, decide on the next state of the game.
        + board is updated by reference
    '''
    possible_moves = where_can_i_move_next(board=board, player=player, verbose=verbose)
    if approach == 'random':
        random_move(possible_moves, board)
    elif approach == 'greedy':
        greedy_move(possible_moves, board)

    else:
        print (f'What is this! {approach}')


def mian_game_loop (verbose=False):
    board = init_board(N)
    if verbose:
        br = Board(N)
        br.draw_board(board)
    
    game_end = -1
    while game_end == -1:
        player = 1
        play_player(approach='greedy', player=player, board=board, verbose=verbose)
        player = -1
        play_player(approach='random', player=player, board=board, verbose=verbose)
        