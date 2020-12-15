from graphics import *

class Board:
    """
    Drawing the board given N
    """
    def __init__(self, N):
        if (N%2 != 0):
            print (f"Error 201: N: {N} must be Even")
            return
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

    def circle(self, center_x, center_y, circle_color):
        center = Point(center_x, center_y)
        circle_draw = Circle(center, 13)
        circle_draw.setFill(circle_color)
        circle_draw.draw(self.window)

    def draw_board(self):
        self.set_window()
        # Draw squares
        for i in range (self.N):
            if i%2 == 0:
                board_color = self.board_color_2
                toggle = 0
            else:
                board_color = self.board_color_1
                toggle = 1
                
            for j in range (self.N):
                self.rect(j*30, i*30, board_color)
                if (i < self.N/2 and i < (self.N/2)-1 and j%2 == toggle):
                    self.circle( (j*30)+15, (i*30)+15, self.circle_color_1) 

                if (i > self.N/2 and i >=(self.N/2)+1 and j%2 == toggle):
                    self.circle( (j*30)+15, (i*30)+15, self.circle_color_2) 

                if board_color == self.board_color_1:
                    board_color = self.board_color_2
                else:
                    board_color = self.board_color_1

        self.window.getMouse()
