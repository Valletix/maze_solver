from tkinter import *
from tkinter.ttk import *


class Window:
    def __init__(self, width, height):
        self.root = Tk()
        self.root.title("Eat Pant")
        self.root.geometry(f"{width}x{height}")
        self.canvas = Canvas(height=height, width=width)
        self.canvas.pack()
        self.running = False
        self.root.protocol("WM_DELETE_WINDOW", self.close)

    def redraw(self):
        self.root.update_idletasks()
        self.root.update()

    def wait_for_close(self):
        self.running = True
        while self.running == True:
            self.redraw()
    
    def close(self):
        self.running = False
    
    def draw_line(self, line, fill_color):
        line.draw(self.canvas, fill_color)

    def draw_cell(self, cell):
        cell.draw(self.canvas)


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class Line:
    def __init__(self, point_1, point_2):
        self.p1 = point_1
        self.p2 = point_2

    
    def draw(self, win, fill_color):
        win.create_line(
            self.p1.x, self.p1.y, self.p2.x, self.p2.y, fill=fill_color, width=2
        )

class Cell:
    def __init__(self, top_left, cell_size_x, cell_size_y, win = None): 
        self._x1 = top_left.x
        self._y1 = top_left.y
        self._x2 = top_left.x + cell_size_x
        self._y2 = top_left.y + cell_size_y
        self._center_x = self._x2 - (cell_size_x / 2)
        self._center_y = self._y2 - (cell_size_y / 2)
        self.has_left_wall = True
        self.has_right_wall = True
        self.has_bottom_wall = True
        self.has_top_wall = True
        self._win = win
        self.visited = False

    def draw(self, tl, br): # tl = TopLeft | br = BottomRight
        if self._win == None:
            return

        left_wall = Line(tl, Point(tl.x, br.y))
        right_wall = Line(Point(br.x, tl.y), br)
        top_wall = Line(tl, Point(br.x, tl.y))
        bottom_wall = Line(Point(tl.x, br.y), br)

        if self.has_left_wall == True:       
            self._win.draw_line(left_wall, "black")
        else:
            self._win.draw_line(left_wall, "#d9d9d9")
            

        if self.has_right_wall == True:   
            self._win.draw_line(right_wall, "black")
        else:
            self._win.draw_line(right_wall, "#d9d9d9")
        
        if self.has_top_wall == True:      
            self._win.draw_line(top_wall, "black")
        else:
            self._win.draw_line(top_wall, "#d9d9d9")
        
        if self.has_bottom_wall == True:     
            self._win.draw_line(bottom_wall, "black")
        else:
            self._win.draw_line(bottom_wall, "#d9d9d9")
        
    def draw_move(self, to_cell, undo = False):
        if undo == False:
            fill_color = "red"
        else:
            fill_color = "grey"

        if self.is_adjacent_and_no_walls(to_cell):
            move_line = Line(Point(self._center_x, self._center_y), Point(to_cell._center_x, to_cell._center_y))
            self._win.draw_line(move_line, fill_color)
        else:
            pass
    
    def is_adjacent_and_no_walls(self, to_cell):
        return (
            (self._x2, self._y1) == (to_cell._x1, to_cell._y1) and not (self.has_right_wall or to_cell.has_left_wall) or
            (self._x2, self._y1) == (to_cell._x2, to_cell._y2) and not (self.has_top_wall or to_cell.has_bottom_wall) or
            (self._x1, self._y2) == (to_cell._x1, to_cell._y1) and not (self.has_bottom_wall or to_cell.has_top_wall) or
            (self._x1, self._y2) == (to_cell._x2, to_cell._y2) and not (self.has_left_wall or to_cell.has_right_wall)
        )

