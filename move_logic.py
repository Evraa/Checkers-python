#Global imports
from copy import deepcopy
#Local imports and Global Variables
from constants import N
from board import Board



def append_this(results, seq):
    '''
        Checks for the sequence to be appended, if it's a subsequence of any existing sequence
        then discard this addition.
    '''
    for result in results:
        if result.find(seq) != -1:
            return
    results.append(seq)

def sequence_of_moves (board, start, end, player,results = [],seq=""):
    '''
        + When theres a sequence of moves due to multiple attacks allowed
        + A back-track stacking algorithm is used.
        + So that we can trace back the movement of the piece
        + More instructions are allowed for kings, thus backward movements are allowed.
        + The Algorithm is simple:
            + If player is Soldier or King, first check what will happen when moving (down-left)
            + then check what will happen when moving (down-right)
            + If this a King move, then also check backwards (up-left) and (up-right)
            + Then collect all of the deadends that occur.
            + Same goes for player 2 (-1 and -2)
        + Results are stored at the 'results' list, thus it's passed by reference through out all the recursive
            calls.
    '''
    if player == 1:
        if end[0] < N and (end[1] >= 0 and end[1] < N):
            #not out of bound
            #Can I move down-left? Is the intermidate cell an enemy? Is the terminal cell empty?
            if end[0]+2 < N and end[1]-2 >= 0 and board[end[0]+1][end[1]-1] <= -1 and board[end[0]+2][end[1]-2]==0:
                #it can move down-left
                board[end[0]+1][end[1]-1] = 0   #kill the enemy pawn
                board[end[0]][end[1]] = 0       #remove me from there
                board[end[0]+2][end[1]-2] = 1   #move me towards the new destination
                seqq = seq + 'L'                #add this move to the sequene
                #Check if there's more!
                seqq+= sequence_of_moves(board, end, (end[0]+2 , end[1]-2), 1, results, seqq)

            #Can I move down-right? Is the intermidate cell an enemy? Is the terminal cell empty?
            if end[0]+2 < N and end[1]+2 < N and board[end[0]+1][end[1]+1] <= -1 and board[end[0]+2][end[1]+2]==0:
                #it can move down-right
                board[end[0]+1][end[1]+1] = 0   #kill the enemy pawn
                board[end[0]][end[1]] = 0       #remove me from there
                board[end[0]+2][end[1]+2] = 1   #move me towards the new destination
                seqq = seq + 'R'                #add this move to the sequene
                #Check if there's more!
                seqq+= sequence_of_moves(board, end, (end[0]+2 , end[1]+2), 1,results,seqq)
            #not out of bound, but no more moves allowed!
            append_this(results, seq)
            return seq+ "0"
        else:
            #out of bound
            #no need to append anything!
            return seq+ "0"
    
    elif player == 2:
        #player 1 king (2)
        if end[0] < N and (end[1] >= 0 and end[1] < N):
            #not out of bound
            #Can I move down-left? Is the intermidate cell an enemy? Is the terminal cell empty?
            if end[0]+2 < N and end[1]-2 >= 0 and board[end[0]+1][end[1]-1] <= -1  and board[end[0]+2][end[1]-2]==0:
                #it can move left down
                new_board = deepcopy(board)         #A new copy cuz, we can turn around to the start
                new_board[end[0]+1][end[1]-1] = 0   #kill the enemy pawn
                new_board[end[0]][end[1]] = 0       #remove me from there
                new_board[end[0]+2][end[1]-2] = 2   #move me towards the new destination
                seqq = seq + 'L'                    #add this move to the sequene
                #Check if there's more!
                seqq += sequence_of_moves(new_board, end, (end[0]+2 , end[1]-2), 2,results,seqq)

            #Can I move down-right? Is the intermidate cell an enemy? Is the terminal cell empty?
            if end[0]+2 < N and end[1]+2 < N and board[end[0]+1][end[1]+1] <= -1 and board[end[0]+2][end[1]+2]==0:
                #it can move right down
                new_board = deepcopy(board)         #A new copy cuz, we can turn around to the start
                new_board[end[0]+1][end[1]+1] = 0   #kill the enemy pawn
                new_board[end[0]][end[1]] = 0       #remove me from there
                new_board[end[0]+2][end[1]+2] = 2   #move me towards the new destination
                seqq = seq + 'R'                    #add this move to the sequene
                #Check if there's more!
                seqq += sequence_of_moves(new_board, end, (end[0]+2 , end[1]+2), 2,results,seqq)
            
            #Can I move up-left? Is the intermidate cell an enemy? Is the terminal cell empty?
            if end[0]-2 >=0 and end[1]-2 >= 0 and board[end[0]-1][end[1]-1] <= -1 and board[end[0]-2][end[1]-2]==0:
                # it can move up left
                new_board = deepcopy(board)         #A new copy cuz, we can turn around to the start
                new_board[end[0]-1][end[1]-1] = 0   #kill the enemy pawn    
                new_board[end[0]][end[1]] = 0       #remove me from there
                new_board[end[0]-2][end[1]-2] = 2   #move me towards the new destination
                seqq = seq + 'l'                    #add this move to the sequene
                #Check if there's more!
                seqq += sequence_of_moves(new_board, end, (end[0]-2 , end[1]-2), 2,results,seqq)
                
            #Can I move up-right? Is the intermidate cell an enemy? Is the terminal cell empty?
            if end[0]-2 >=0 and end[1]+2 < N and board[end[0]-1][end[1]+1] <= -1 and board[end[0]-2][end[1]+2]==0:
                # it can move up right
                new_board = deepcopy(board)         #A new copy cuz, we can turn around to the start
                new_board[end[0]-1][end[1]+1] = 0   #kill the enemy pawn    
                new_board[end[0]][end[1]] = 0       #remove me from there
                new_board[end[0]-2][end[1]+2] = 2   #move me towards the new destination
                seqq = seq + 'r'                    #add this move to the sequene
                #Check if there's more!
                seqq += sequence_of_moves(new_board, end, (end[0]-2 , end[1]+2), 2,results,seqq)

            #not out of bound, but no more moves allowed!
            append_this(results, seq)
            return seq+ "0"
        else:
            #out of bound
            return seq+ "0"

    elif player == -1:
        pass
    elif player == -2:
        pass


def add_results(results, possible_moves, start, orig_board):
    '''
        + Given a sequence like this RrlL, this function interpret this sequence into actual moves and kills.
        + R: down Right
        + r: up Right
        + l: up Left
        + L: down Left
        + Inputs:
            + results: list of one or multiple sequence(s)
            + possible_moves: where we update (append) new possible moves
            + start: this piece's initail place
            + orig_board: the original board, useful and necessary for king moves tracking
        + Outputs: None, just appending to possible_moves variable reference

        + Logic is simple, updat the start and the board with the sequence char (R,r,L,l)
    '''
    for result in results:
        possible_move = [start]
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


def where_can_i_move_next(board, player=1, verbose=False):
    '''
        + Given player (1/-1) and the board settings, decide the pieces that can move next.
        + Returns: list of possible moves
            + Possible_move: [typle of start, tuple of end, how_many_killed, new_board]

        + Logic is divided into groups:
        + Group 1: for player 1, divided into two sections
            + section 1: for soldiers and kings, check if they can move down-left or down-right
                + checks if they can have multiple moves and kills
            + section 2: for kings only, check if the can move up-left or up-right
                + checks if they can have multiple moves also.
        + Group 2: same for player 2 
    '''
    #where the moves are stored at
    possible_moves = []
    #loop throught the entire board for player 1/-1
    for i in range(N):
        for j in range (N):
            #no pawns are here from the start.
            if  board[i][j] == 0 :
                continue
            
            #pos: player 1 whther it was soldier or king
            if board[i][j] >= 1 and player == 1:
                #player 1 soldier or king
                if (i+1 < N) and (j-1 >= 0):
                    #not out of bound
                    if (board[i+1][j-1] == 0):
                        #can move left down
                        new_board = deepcopy(board)
                        new_board[i+1][j-1] = 0             #killed it
                        new_board[i][j] = 0                 #move me
                        new_board[i+1][j-1] = board[i][j]   #there
                        possible_moves.append( [(i,j), (i+1, j-1), 0, new_board]  )

                    #sequence of moves may occur
                    elif (board[i+1][j-1] <= -1) and (i+2<N and j-2 >=0) and board[i+2][j-2] == 0:
                        new_board = deepcopy(board)
                        new_board[i+1][j-1] = 0             #killed it
                        new_board[i][j] = 0                 #move me
                        new_board[i+2][j-2] = board[i][j]   #there
                        results = []
                        sequence_of_moves (new_board, (i,j),(i+2,j-2),board[i][j],results,'L')
                        new_board = deepcopy(board)
                        add_results(results, possible_moves,(i,j),new_board)

                if (i+1 < N) and (j+1 < N):
                    if (board[i+1][j+1] == 0):
                        #not out of bound, and free move "right" down
                        new_board = deepcopy(board)
                        new_board[i+1][j+1] = 0             #killed it
                        new_board[i][j] = 0                 #move me
                        new_board[i+1][j+1] = board[i][j]   #there
                        possible_moves.append( [(i,j), (i+1, j+1), 0, new_board]  )

                    elif (board[i+1][j+1] <= -1) and (i+2<N and j+2 <N) and board[i+2][j+2] == 0:
                        new_board = deepcopy(board)
                        new_board[i+1][j+1] = 0             #killed it
                        new_board[i][j] = 0                 #move me
                        new_board[i+2][j+2] = board[i][j]   #there
                        results = []
                        sequence_of_moves (new_board, (i,j),(i+2,j+2),board[i][j],results,'R')
                        new_board = deepcopy(board)
                        add_results(results, possible_moves,(i,j),new_board)

            if board[i][j] == 2 and player == 1:
                ######### player 1 king ONLY#######
                #check if it can go up! 
                if (i-1 >= 0) and (j-1 >= 0):
                    #not out of bound
                    if (board[i-1][j-1] == 0):
                        #can move left
                        new_board = deepcopy(board)
                        new_board[i-1][j-1] = 0             #killed it
                        new_board[i][j] = 0                 #move me
                        new_board[i-1][j-1] = board[i][j]   #there
                        possible_moves.append( [(i,j), (i-1, j-1), 0, new_board]  )

                    #sequence of moves may occur
                    elif (board[i-1][j-1] <= -1) and (i-2>=0 and j-2 >=0) and board[i-2][j-2] == 0:
                        new_board = deepcopy(board)
                        new_board[i-1][j-1] = 0             #killed it
                        new_board[i][j] = 0                 #move me
                        new_board[i-2][j-2] = board[i][j]   #there    
                        results = []
                        sequence_of_moves (new_board, (i,j),(i-2,j-2),board[i][j],results, 'l')
                        new_board = deepcopy(board)
                        add_results(results, possible_moves,(i,j),new_board)

                if (i-1 >= 0) and (j+1 < N):
                    if (board[i-1][j+1] == 0):
                        #not out of bound, and free move "right" up
                        new_board = deepcopy(board)
                        new_board[i-1][j+1] = 0             #killed it
                        new_board[i][j] = 0                 #move me
                        new_board[i-1][j+1] = board[i][j]   #there
                        possible_moves.append( [(i,j), (i-1, j+1), 0, new_board]  )

                    elif (board[i-1][j+1] <= -1) and (i-2>=0 and j+2<N) and board[i-2][j+2] == 0:
                        new_board = deepcopy(board)
                        new_board[i-1][j+1] = 0             #killed it
                        new_board[i][j] = 0                 #move me
                        new_board[i-2][j+2] = board[i][j]   #there
                        results = []
                        sequence_of_moves (new_board, (i,j),(i-2,j+2),board[i][j],results,'r')
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
    forced = False
    possible_moves_forced = []
    for pos in possible_moves:
        if pos[2] >= 1:
            possible_moves_forced.append(pos)
            forced = True
            
    if forced:
        del possible_moves
        possible_moves = possible_moves_forced

    if verbose:
        for poss in possible_moves:
            br = Board(N)
            br.draw_board(poss[3])
    
    return possible_moves

# board = init_board(N)
# zeros = [0,0,0,0,0,0,0,0]
# test_board = [  [0,0,0,0,0,0,0,0],
#                 [0,0,-1,0,-1,0,0,0],
#                 [0,0,0,0,0,0,0,0],
#                 [-1,0,-1,0,-1,0,-1,0],
#                 [0,0,0,2,0,0,0,0],
#                 [-1,0,-1,0,-1,0,-1,0],
#                 [0,0,0,0,0,0,0,0],
#                 [-1,0,-1,0,-1,0,-1,0]
#             ]

# print (where_can_i_move_next(test_board))