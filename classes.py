from tkinter import *
from tkinter.ttk import *
import time


class Window:
    def __init__(self, width, height):
        self.root = Tk()
        self.root.title("This is a maze solver")
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
        win.canvas.create_line(
            self.p1.x, self.p1.y, self.p2.x, self.p2.y, fill=fill_color, width=2
        )

class Cell:
    def __init__(self, top_left, cell_size_x, cell_size_y, win): 
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

    def draw(self, tl, br): # tl = TopLeft | br = BottomRight
        if self.has_left_wall == True:
            left_wall = Line(tl, Point(tl.x, br.y))
            left_wall.draw(self._win, "black")

        if self.has_right_wall == True:
            right_wall = Line(Point(br.x, tl.y), br)
            right_wall.draw(self._win, "black")
        
        if self.has_top_wall == True:
            top_wall = Line(tl, Point(br.x, tl.y))
            top_wall.draw(self._win, "black")
        
        if self.has_bottom_wall == True:
            bottom_wall = Line(Point(tl.x, br.y), br)
            bottom_wall.draw(self._win, "black") 
        
    def draw_move(self, canvas, to_cell, undo = False):
        if undo == False:
            fill_color = "red"
        else:
            fill_color = "grey"

        if self.is_adjacent_and_no_walls(to_cell):
            canvas.create_line(
                self._center_x, self._center_y, to_cell._center_x, to_cell._center_y, fill=fill_color, width = 2
            )
        else:
            pass
     
    

    
    def is_adjacent_and_no_walls(self, to_cell):
        return (
            (self._x2, self._y1) == (to_cell._x1, to_cell._y1) and not (self.has_right_wall or to_cell.has_left_wall) or
            (self._x2, self._y1) == (to_cell._x2, to_cell._y2) and not (self.has_top_wall or to_cell.has_bottom_wall) or
            (self._x1, self._y2) == (to_cell._x1, to_cell._y1) and not (self.has_bottom_wall or to_cell.has_top_wall) or
            (self._x1, self._y2) == (to_cell._x2, to_cell._y2) and not (self.has_left_wall or to_cell.has_right_wall)
        )


class Maze:
    def __init__(
            self,
            x1,
            y1,
            num_rows,
            num_cols,
            cell_size_x,
            cell_size_y,
            win):
        self.x1 = x1
        self.y1 = y1
        self.num_rows = num_rows
        self.num_cols = num_cols
        self.cell_size_x = cell_size_x
        self.cell_size_y = cell_size_y
        self.win = win

        self._create_cells()

    def _create_cells(self):
        self._cells = []
        for i in range(1, self.num_cols+1):
            cell_col = []
            for j in range(1, self.num_rows+1):
                cell_tl = Point(i*self.cell_size_x,j*self.cell_size_y)
                cell_col.append(Cell(cell_tl, self.cell_size_x, self.cell_size_y, self.win))
            self._cells.append(cell_col)

        for col in self._cells:
            for cell in col:
                self._draw_cell(cell)
        
    
    def _draw_cell(self, cell):
        cell_tl = Point(cell._x1, cell._y1)
        cell_br = Point(cell._x2, cell._y2)
        cell.draw(cell_tl, cell_br)
        self._animate()


    def _animate(self):
        self.win.redraw()
        time.sleep(0.1)