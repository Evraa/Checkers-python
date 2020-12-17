from math import ceil, floor
from copy import deepcopy
from constants import N

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



def append_this(results, seq):
    for result in results:
        if result.find(seq) != -1:
            return
    results.append(seq)

from board import *
def sequence_of_moves (board, start, end, player,ultimate_start,results = [],seq=""):
    
    if player == 1:
        if end[0] < N and (end[1] >= 0 and end[1] < N):
            #not out of bound
            # if board[end[0]][end[1]] == 0: 
            if end[0]+2 < N and end[1]-2 >= 0 and board[end[0]+1][end[1]-1] <= -1 and board[end[0]+2][end[1]-2]==0:
                #it can move left
                board[end[0]+1][end[1]-1] = 0
                board[end[0]][end[1]] = 0
                board[end[0]+2][end[1]-2] = 1
                seqq = seq + 'L'
                seqq+= sequence_of_moves(board, end, (end[0]+2 , end[1]-2), 1,ultimate_start, results, seqq)

            if end[0]+2 < N and end[1]+2 < N and board[end[0]+1][end[1]+1] <= -1 and board[end[0]+2][end[1]+2]==0:
                #it can move right
                board[end[0]+1][end[1]+1] = 0
                board[end[0]][end[1]] = 0
                board[end[0]+2][end[1]+2] = 1
                seqq = seq + 'R'
                seqq+= sequence_of_moves(board, end, (end[0]+2 , end[1]+2), 1,ultimate_start,results,seqq)
            #not out of bound, but no more moves allowed!
            append_this(results, seq)
            return seq+ "0"
        else:
            #out of bound
            return seq+ "0"
    
    elif player == 2:
        #player 1 king
        if end[0] < N and (end[1] >= 0 and end[1] < N):
            #not out of bound
            # if board[end[0]][end[1]] == 0 or end==ultimate_start: 
            if end[0]+2 < N and end[1]-2 >= 0 and board[end[0]+1][end[1]-1] <= -1  and board[end[0]+2][end[1]-2]==0:
                #it can move left down
                new_board = deepcopy(board)
                new_board[end[0]+1][end[1]-1] = 0
                new_board[end[0]][end[1]] = 0
                new_board[end[0]+2][end[1]-2] = 2
                seqq = seq + 'L' 
                # seq+=  'L' + sequence_of_moves(new_board, end, (end[0]+2 , end[1]-2), 2,ultimate_start,seqq)
                seqq += sequence_of_moves(new_board, end, (end[0]+2 , end[1]-2), 2,ultimate_start,results,seqq)
                
            if end[0]+2 < N and end[1]+2 < N and board[end[0]+1][end[1]+1] <= -1 and board[end[0]+2][end[1]+2]==0:
                #it can move right down
                new_board = deepcopy(board)
                new_board[end[0]+1][end[1]+1] = 0
                new_board[end[0]][end[1]] = 0
                new_board[end[0]+2][end[1]+2] = 2
                # seq+= 'R' + sequence_of_moves(new_board, end, (end[0]+2 , end[1]+2), 2,ultimate_start)
                seqq = seq + 'R' 
                seqq += sequence_of_moves(new_board, end, (end[0]+2 , end[1]+2), 2,ultimate_start,results,seqq)
            if end[0]-2 >=0 and end[1]-2 >= 0 and board[end[0]-1][end[1]-1] <= -1 and board[end[0]-2][end[1]-2]==0:
                # it can move up left
                new_board = deepcopy(board)
                new_board[end[0]-1][end[1]-1] = 0
                new_board[end[0]][end[1]] = 0
                new_board[end[0]-2][end[1]-2] = 2
                # seq+= 'l' + sequence_of_moves(new_board, end, (end[0]-2 , end[1]-2), 2,ultimate_start)
                seqq = seq + 'l' 
                seqq += sequence_of_moves(new_board, end, (end[0]-2 , end[1]-2), 2,ultimate_start,results,seqq)
            if end[0]-2 >=0 and end[1]+2 < N and board[end[0]-1][end[1]+1] <= -1 and board[end[0]-2][end[1]+2]==0:
                # it can move up right
                new_board = deepcopy(board)
                new_board[end[0]-1][end[1]+1] = 0
                new_board[end[0]][end[1]] = 0
                new_board[end[0]-2][end[1]+2] = 2
                # seq+= 'r' + sequence_of_moves(new_board, end, (end[0]-2 , end[1]+2), 2,ultimate_start)
                seqq = seq + 'r' 
                seqq += sequence_of_moves(new_board, end, (end[0]-2 , end[1]+2), 2,ultimate_start,results,seqq)

            #not out of bound, but no more moves allowed!
            # results.append(seq)
            append_this(results, seq)
            return seq+ "0"
        else:
            #out of bound
            # results.append(seq+'0')
            return seq+ "0"

    elif player == -1:
        pass
    elif player == -2:
        pass


def add_results(results, possible_moves, start, orig_board):
    for result in results:
        possible_move = [start]
        # chars = result.split(' ')
        # chars = result.split('')
        board = deepcopy(orig_board)
        cost = 0
        i,j = start[0],start[1]
        for char in result:
            if char == '' or char == ' ':
                continue
            if char == 'R':
                board[i+1][j+1] = 0 #kill it
                board[i+2][j+2] = board[i][j]   #move me
                board[i][j] =0      #from there
                cost += 1
                i += 2
                j += 2
            elif char == 'L':
                board[i+1][j-1] = 0 #kill it
                board[i+2][j-2] = board[i][j]   #move me
                board[i][j] =0      #from there
                cost += 1
                i += 2
                j -= 2
            elif char == 'r':
                board[i-1][j+1] = 0 #kill it
                board[i-2][j+2] = board[i][j]   #move me
                board[i][j] =0      #from there
                cost += 1
                i -= 2
                j += 2
            elif char == 'l':
                board[i-1][j-1] = 0 #kill it
                board[i-2][j-2] = board[i][j]   #move me
                board[i][j] =0      #from there
                cost += 1
                i -= 2
                j -= 2

        possible_move.append((i,j))    
        possible_move.append(cost)
        possible_move.append(board)
        possible_moves.append(possible_move)


def where_can_i_move_next(board, player=1):
    '''
        + Given player (1/-1) and the board settings, decide the pieces that can move next.
        + Returns: list of possible moves
            + Possible_move: [typle of start, tuple of end, how_many_killed, new_board]
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
                #player 1 soldier or king
                if (i+1 < N) and (j-1 >= 0):
                    #not out of bound
                    if (board[i+1][j-1] == 0):
                        #can move left down
                        new_board = deepcopy(board)
                        new_board[i+1][j-1] = 0 #killed it
                        new_board[i][j] = 0     #move me
                        new_board[i+2][j-2] = board[i][j] #there
                        possible_moves.append( [(i,j), (i+1, j-1), 0, new_board]  )

                    #sequence of moves may occur
                    elif (board[i+1][j-1] <= -1) and (i+2<N and j-2 >=0) and board[i+2][j-2] == 0:
                        new_board = deepcopy(board)
                        new_board[i+1][j-1] = 0
                        new_board[i][j] = 0
                        new_board[i+2][j-2] = board[i][j] #2
                        results = []
                        sequence_of_moves (new_board, (i,j),(i+2,j-2),board[i][j],(i,j),results,'L')
                        new_board = deepcopy(board)
                        add_results(results, possible_moves,(i,j),new_board)

                if (i+1 < N) and (j+1 < N):
                    if (board[i+1][j+1] == 0):
                        #not out of bound, and free move "right" down
                        new_board = deepcopy(board)
                        new_board[i+1][j+1] = 0 #killed it
                        new_board[i][j] = 0     #move me
                        new_board[i+2][j+2] = board[i][j] #there
                        possible_moves.append( [(i,j), (i+1, j+1), 0, new_board]  )

                    elif (board[i+1][j+1] <= -1) and (i+2<N and j+2 <N) and board[i+2][j+2] == 0:
                        new_board = deepcopy(board)
                        new_board[i+1][j+1] = 0
                        new_board[i][j] = 0
                        new_board[i+2][j+2] = board[i][j]
                        results = []
                        sequence_of_moves (new_board, (i,j),(i+2,j+2),board[i][j],(i,j),results,'R')
                        new_board = deepcopy(board)
                        add_results(results, possible_moves,(i,j),new_board)

            if board[i][j] == 2 and player == 1:
                ######### player 1 king #######
                #check if it can go up! 
                if (i-1 >= 0) and (j-1 >= 0):
                    #not out of bound
                    if (board[i-1][j-1] == 0):
                        #can move left
                        new_board = deepcopy(board)
                        new_board[i-1][j-1] = 0 #killed it
                        new_board[i][j] = 0     #move me
                        new_board[i-2][j-2] = board[i][j] #there
                        possible_moves.append( [(i,j), (i-1, j-1), 0, new_board]  )

                    #sequence of moves may occur
                    elif (board[i-1][j-1] <= -1) and (i-2>=0 and j-2 >=0) and board[i-2][j-2] == 0:
                        new_board = deepcopy(board)
                        new_board[i-1][j-1] = 0
                        new_board[i][j] = 0
                        new_board[i-2][j-2] = board[i][j]
                        results = []
                        sequence_of_moves (new_board, (i,j),(i-2,j-2),board[i][j],(i,j),results, 'l')
                        new_board = deepcopy(board)
                        add_results(results, possible_moves,(i,j),new_board)

                if (i-1 >= 0) and (j+1 < N):
                    if (board[i-1][j+1] == 0):
                        #not out of bound, and free move "right" up
                        new_board = deepcopy(board)
                        new_board[i-1][j+1] = 0 #killed it
                        new_board[i][j] = 0     #move me
                        new_board[i-2][j+2] = board[i][j] #there
                        possible_moves.append( [(i,j), (i-1, j+1), 0, new_board]  )

                    elif (board[i-1][j+1] <= -1) and (i-2>=0 and j+2<N) and board[i-2][j+2] == 0:
                        new_board = deepcopy(board)
                        new_board[i-1][j+1] = 0
                        new_board[i][j] = 0
                        new_board[i-2][j+2] = board[i][j]
                        results = []
                        sequence_of_moves (new_board, (i,j),(i-2,j+2),board[i][j],(i,j),results,'r')
                        new_board = deepcopy(board)
                        add_results(results, possible_moves,(i,j),new_board)


            elif board[i][j] <= -1 and player == -1:
                #player 2
                if (i-1 >= 0) and (j-1 >= 0):
                    #not out of bound
                    if (board[i-1][j-1] == 0):
                        #can move left
                        possible_moves.append( [(i,j), (i-1, j-1), 0]  )
                    elif (board[i-1][j-1] >= 1):
                        moves = sequence_of_moves (board, (i,j),(i-2,j-2),-1,(i,j))

                if (i-1 >= 0) and (j+1 < N):
                    if (board[i-1][j+1] == 0):
                        #not out of bound, and free move "right"
                        possible_moves.append( [(i,j), (i-1, j+1), 0]  )
                    elif (board[i-1][j+1] >= 1):
                        moves = sequence_of_moves (board, (i,j),(i-2,j+2),-1,(i,j))

            #else is zero .. skip .. no elses btw.
    for poss in possible_moves:
        br = Board(N)

        br.draw_board(poss[3])


    return (possible_moves)

# board = init_board(N)
zeros = [0,0,0,0,0,0,0,0]
test_board = [  [0,0,0,0,0,0,0,0],
                [0,0,-1,0,-1,0,0,0],
                [0,0,0,0,0,0,0,0],
                [-1,0,-1,0,-1,0,-1,0],
                [0,0,0,2,0,0,0,0],
                [-1,0,-1,0,-1,0,-1,0],
                [0,0,0,0,0,0,0,0],
                [-1,0,-1,0,-1,0,-1,0]
            ]

where_can_i_move_next(test_board)