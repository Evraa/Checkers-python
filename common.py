from constants import N
from math import ceil, floor

def init_board(N):
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
        tmp = line_1
        line_1 = line_2
        line_2 = tmp
        tmp = line_1_2
        line_1_2 = line_2_2
        line_2_2 = tmp
    for i in range (N):
        if i%2 == 0 and i < ceil(N/2)-1:
            board.append(line_2)
        elif i%2 == 1 and i< ceil(N/2)-1: 
            board.append(line_1)

        elif i%2 == 0 and i > floor(N/2):
            board.append(line_2_2)
        elif i%2 == 1 and i > floor(N/2): 
            board.append(line_1_2)
        else:
            board.append(zeros)
    print(board)
    return board

def where_can_i_move_next(board, player=1):
    '''
        + Given player (1/-1) and the board settings, decide the pieces that can move next.
        + Returns: list of tuples of pieces indexes that can move next.
    '''
    #Total number of pieces a player might has
    num_pieces = (ceil(N/2) - 1) * (ceil(N/2))
    print(num_pieces)
