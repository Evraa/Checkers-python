
WIDTH, HEIGHT, SQR_SIZE = 720, 720, 30
N = 7
DEPTH = 6 if N%2==0 else 100
MIN_DEPTH = 6
close_window = 0
MAX_POS = pow(N,2)
MAX_NEG = -MAX_POS

'''
4 -> 5 and end
6 -> 8 and dead
8 -> 6 and dead
10 -> 5 and dead

5 -> 9 and end
7 -> 10 and dead
9 -> 8 and dead
11 -> 8 and dead
'''