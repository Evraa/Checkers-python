from board import *
from common import *
from constants import N
from move_logic import where_can_i_move_next
# board = init_board(N)
board = rand_init(N)
print (board)
br = Board(N)

br.draw_board(board)
where_can_i_move_next(board,1,True)