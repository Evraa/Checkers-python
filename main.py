from board import *
from common import *
from constants import N
N =9
board = init_board(N)
br = Board(N)
br.draw_board(board)
where_can_i_move_next(board)