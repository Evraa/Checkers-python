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
    seq = ""
    if player == 1:
        if end[0] < N and (end[1] >= 0 and end[1] < N):
            #not out of bound
            if board[end[0]][end[1]] == 0: 
                if end[0]+2 < N and end[1]-2 >= 0 and board[end[0]+1][end[1]-1] <= -1:
                    #it can move left
                    seq+= 'L' + sequence_of_moves(board, end, (end[0]+2 , end[1]-2), 1)
                if end[0]+2 < N and end[1]+2 < N and board[end[0]+1][end[1]+1] <= -1:
                    #it can move right
                    seq+= 'R' + sequence_of_moves(board, end, (end[0]+2 , end[1]+2), 1)
                #not out of bound, but no more moves allowed!
                return seq+ "0"
        else:
            #out of bound
            return seq+ "0"
    
    elif player == -1:
        pass


def interpret_moves(moves):
    sequences = []
    sequences.append(moves[0]+moves[1])
    i = 1
    for move in (moves[2:]):
        if len(move) > 0:
            sequences.append(sequences[i-1])
            L = len(move)
            sequences[i] = sequences[i][0:-L] + move
            i += 1
    print (sequences)



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
                    elif (board[i+1][j-1] <= -1) and (i+2<N and j-2 >=0):
                        moves = "L0" + sequence_of_moves (board, (i,j),(i+2,j-2),1)
                        print (moves.split("0"))
                        interpret_moves(moves.split("0"))

                if (i+1 < N) and (j+1 < N):
                    if (board[i+1][j+1] == 0):
                        #not out of bound, and free move "right"
                        possible_moves.append( [(i,j), (i+1, j+1), 0]  )
                    elif (board[i+1][j+1] <= -1):
                        moves = 'R0' + sequence_of_moves (board, (i,j),(i+2,j+2),1)
                        print (moves.split("0"))
                        interpret_moves(moves.split("0"))

            elif board[i][j] <= -1 and player == -1:
                #player 2
                if (i-1 >= 0) and (j-1 >= 0):
                    #not out of bound
                    if (board[i-1][j-1] == 0):
                        #can move left
                        possible_moves.append( [(i,j), (i-1, j-1), 0]  )
                    elif (board[i-1][j-1] >= 1):
                        moves = sequence_of_moves (board, (i,j),(i-2,j-2),-1)

                if (i-1 >= 0) and (j+1 < N):
                    if (board[i-1][j+1] == 0):
                        #not out of bound, and free move "right"
                        possible_moves.append( [(i,j), (i-1, j+1), 0]  )
                    elif (board[i-1][j+1] >= 1):
                        moves = sequence_of_moves (board, (i,j),(i-2,j+2),-1)

            #else is zero .. skip .. no elses btw.
    return (possible_moves)

# board = init_board(N)
zeros = [0,0,0,0,0,0,0,0]
test_board = [  [0,0,0,1,0,0,0,0],
                [0,0,-1,0,-1,0,0,0],
                [0,0,0,0,0,0,0,0],
                [-1,0,-1,0,-1,0,-1,0],
                [0,0,0,0,0,0,0,0],
                [-1,0,-1,0,-1,0,-1,0],
                [0,0,0,0,0,0,0,0],
                [-1,0,-1,0,-1,0,-1,0]
            ]
(where_can_i_move_next(test_board))