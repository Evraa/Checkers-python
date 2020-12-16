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
        line_1, line_2 = line_2, line_1
        line_1_2, line_2_2 = line_2_2, line_1_2
        
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
    return board

def sequence_of_moves (board, start, end, player):
    count = 0



def where_can_i_move_next(board, player=1):
    '''
        + Given player (1/-1) and the board settings, decide the pieces that can move next.
        + Returns: list of tuples of pieces indexes that can move next.
    '''
    #Total number of pieces a player might has
    num_pieces = (ceil(N/2) - 1) * (ceil(N/2))
    #(start, end, wining_cost), wining_cost: how many pieces I ate!
    possible_moves = []

    for i in range(N):
        for j in range (N):
            if  board[i][j] == 0 :
                continue
            
            #pos: player 1 whther it was soldier or king
            #neg: player 2 ~
            if board[i][j] >= 1 and player == 1:
                #player 1
                if (i+1 < N) and (j-1 >= 0):
                    #not out of bound
                    if (board[i+1][j-1] == 0):
                        #can move left
                        possible_moves.append( [(i,j), (i+1, j-1), 0]  )
                    elif (board[i+1][j-1] <= -1):
                        moves = sequence_of_moves (board, (board[i],board[j]),(board[i+1],board[j-1]),1)
                 
                if (i+1 < N) and (j+1 < N):
                    if (board[i+1][j+1] == 0):
                        #not out of bound, and free move "right"
                        possible_moves.append( [(i,j), (i+1, j+1), 0]  )
                    elif (board[i+1][j+1] <= -1):
                        moves = sequence_of_moves (board, (board[i],board[j]),(board[i+1],board[j+1]),1)
                
                    
            elif board[i][j] <= -1 and player == -1:
                #player 2
                if (i-1 >= 0) and (j-1 >= 0):
                    #not out of bound
                    if (board[i-1][j-1] == 0):
                        #can move left
                        possible_moves.append( [(i,j), (i-1, j-1), 0]  )
                    elif (board[i-1][j-1] >= 1):
                        moves = sequence_of_moves (board, (board[i],board[j]),(board[i-1],board[j-1]),-1)

                if (i-1 >= 0) and (j+1 < N):
                    if (board[i-1][j+1] == 0):
                        #not out of bound, and free move "right"
                        possible_moves.append( [(i,j), (i-1, j+1), 0]  )
                    elif (board[i-1][j+1] >= 1):
                        moves = sequence_of_moves (board, (board[i],board[j]),(board[i-1],board[j+1]),-1)
            #else is zero .. skip
    print (possible_moves)
board = init_board(N)
where_can_i_move_next(board, -1)