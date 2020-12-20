from graphics import *
from constants import WIDTH, HEIGHT, SQR_SIZE
class Board:
    """
    Drawing the board given N
    """
    def __init__(self, N):
        self.N = N
        self.board_color_1 = color_rgb(250, 220, 107)
        self.board_color_2 = color_rgb(219, 74, 14)
        self.circle_color_1 = color_rgb(222,241, 229)
        self.circle_color_2 = color_rgb(41, 26, 24)

    def set_window(self):
        win = GraphWin('board',WIDTH,HEIGHT)
        win.setCoords(0, 0, self.N*SQR_SIZE, self.N*SQR_SIZE)
        self.window = win

    def rect(self, right, top, color):
        point_1 = Point(right, top)
        point_2 = Point(right+SQR_SIZE, top+SQR_SIZE)
        rect_draw = Rectangle(point_1, point_2)
        rect_draw.setFill(color)
        rect_draw.draw(self.window)

    def circle(self, center_x, center_y, circle_color, radius=(SQR_SIZE//2)-2):
        center = Point(center_x, center_y)
        circle_draw = Circle(center, radius)
        circle_draw.setFill(circle_color)
        circle_draw.setOutline("red")
        circle_draw.draw(self.window)
    
    def crown_cross (self, center_x, center_y, color="green"):
        point_1_x = Point(center_x-5, center_y)
        point_2_x = Point(center_x+5, center_y)
        line_x = Line(point_1_x, point_2_x)
        line_x.setOutline(color)
        line_x.draw(self.window)
        point_1_x = Point(center_x, center_y-5)
        point_2_x = Point(center_x, center_y+5)
        line_x = Line(point_1_x, point_2_x)
        line_x.setOutline(color)
        line_x.draw(self.window)


    def draw_board(self, board):
        self.set_window()
        # Draw squares
        for i in range (self.N):
            if i%2 == 0:
                board_color = self.board_color_2
            else:
                board_color = self.board_color_1
                
            for j in range (self.N):
                self.rect(j*SQR_SIZE, i*SQR_SIZE, board_color)

                if (board[self.N-i-1][j] >= 1):
                    #player 1: white
                    self.circle( (j*SQR_SIZE)+(SQR_SIZE//2), (i*SQR_SIZE)+(SQR_SIZE//2), self.circle_color_1) 
                    self.circle( (j*SQR_SIZE)+(SQR_SIZE//2), (i*SQR_SIZE)+(SQR_SIZE//2), self.circle_color_1, radius = (SQR_SIZE//2)-5) 
                    if board[self.N-i-1][j] == 2:
                        self.crown_cross((j*SQR_SIZE)+(SQR_SIZE//2), (i*SQR_SIZE)+(SQR_SIZE//2))

                if (board[self.N-i-1][j] <= -1):
                    self.circle( (j*SQR_SIZE)+(SQR_SIZE//2), (i*SQR_SIZE)+(SQR_SIZE//2), self.circle_color_2) 
                    self.circle( (j*SQR_SIZE)+(SQR_SIZE//2), (i*SQR_SIZE)+(SQR_SIZE//2), self.circle_color_2, radius=(SQR_SIZE//2)-5) 
                    if (board[self.N-i-1][j] == -2):
                        self.crown_cross((j*SQR_SIZE)+(SQR_SIZE//2), (i*SQR_SIZE)+(SQR_SIZE//2))

                if board_color == self.board_color_1:
                    board_color = self.board_color_2
                else:
                    board_color = self.board_color_1
        self.window.getMouse()
    