from graphics import *

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
        win = GraphWin('board',720,720)
        win.setCoords(0, 0, self.N*30, self.N*30)
        self.window = win

    def rect(self, right, top, color):
        point_1 = Point(right, top)
        point_2 = Point(right+30, top+30)
        rect_draw = Rectangle(point_1, point_2)
        rect_draw.setFill(color)
        rect_draw.draw(self.window)

    def circle(self, center_x, center_y, circle_color, radius=13):
        center = Point(center_x, center_y)
        circle_draw = Circle(center, radius)
        circle_draw.setFill(circle_color)
        circle_draw.setOutline("red")
        circle_draw.draw(self.window)

    def draw_board(self, board):
        self.set_window()
        # Draw squares
        for i in range (self.N):
            if i%2 == 0:
                board_color = self.board_color_2
            else:
                board_color = self.board_color_1
                
            for j in range (self.N):
                self.rect(j*30, i*30, board_color)

                if (board[self.N-i-1][j] == 1):
                    #player 1: white
                    self.circle( (j*30)+15, (i*30)+15, self.circle_color_1) 
                    self.circle( (j*30)+15, (i*30)+15, self.circle_color_1, radius = 10) 

                if (board[self.N-i-1][j] == -1):
                    self.circle( (j*30)+15, (i*30)+15, self.circle_color_2) 
                    self.circle( (j*30)+15, (i*30)+15, self.circle_color_2, radius=10) 
                if board_color == self.board_color_1:
                    board_color = self.board_color_2
                else:
                    board_color = self.board_color_1

        self.window.getMouse()
    