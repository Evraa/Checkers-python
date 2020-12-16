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
    for i in range (N):
        if i%2 == 0 and i < (N/2)-1:
            board.append(line_2)
        elif i%2 == 1 and i< (N/2)-1: 
            board.append(line_1)

        elif i%2 == 0 and i >= (N/2)+1:
            board.append(line_2_2)
        elif i%2 == 1 and i>= (N/2)+1: 
            board.append(line_1_2)
        else:
            board.append(zeros)
    
    return board

    
init_board(8)