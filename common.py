#Global imports
from math import ceil, floor
from numpy import random
#Local imports and Global Variables
from constants import N

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
    for i in range (N):
        for j in range (N):
            if((i%2) != ((j+1)%2) and N%2 == 0) or ((i%2) != (j%2) and N%2 == 1):
                continue
            else:
                ev = random.randint(3)
                if i < N//2: 
                    board[i][j] = ev
                else:
                    board[i][j] = -ev
    return board


print (rand_init(8))