from board import *
from common import *
from constants import N

board = init_board(N)
br = Board(N)
br.draw_board(board)
where_can_i_move_next(board,-1)