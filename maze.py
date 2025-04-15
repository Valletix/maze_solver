from classes import Point, Line, Cell
import time, random

class Maze:
    def __init__(
            self,
            x1,
            y1,
            num_rows,
            num_cols,
            cell_size_x,
            cell_size_y,
            win = None,
            seed = None):
        self.x1 = x1
        self.y1 = y1
        self.num_rows = num_rows
        self.num_cols = num_cols
        self.cell_size_x = cell_size_x
        self.cell_size_y = cell_size_y
        self.win = win

        if seed != None:
            random.seed(seed)

        self._create_cells()
        self._break_entrance_and_exit()
        self._break_walls_r(0,0)
        self._reset_cells_visited()

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
        if self.win is None:
            return
        
        cell_tl = Point(cell._x1, cell._y1)
        cell_br = Point(cell._x2, cell._y2)
        cell.draw(cell_tl, cell_br)
        self._animate()


    def _animate(self):
        if self.win is None:
            return

        self.win.redraw()
        time.sleep(0.02)

    def _break_entrance_and_exit(self):
        top_left_cell = self._cells[0][0]
        top_left_cell.has_top_wall = False
        self._draw_cell(top_left_cell)
        bottom_right_cell = self._cells[self.num_cols-1][self.num_rows-1]
        bottom_right_cell.has_bottom_wall = False
        self._draw_cell(bottom_right_cell)
    
    def _break_walls_r(self, i, j):
        current_cell = self._cells[i][j]
        self._cells[i][j].visited = True
        while True:
            to_visit = []
            if i != 0:
                if self._cells[i-1][j].visited == False:
                    to_visit.append((i-1, j))
            if j != 0:
                if self._cells[i][j-1].visited == False:
                    to_visit.append((i, j-1))
            if i != self.num_cols -1:
                if self._cells[i+1][j].visited == False:
                    to_visit.append((i+1, j))
            if j != self.num_rows -1:
                if self._cells[i][j+1].visited == False:
                    to_visit.append((i, j+1))
            
            if len(to_visit) == 0:
                self._draw_cell(current_cell)
                return
            else:
                direction = to_visit[random.randrange(0, len(to_visit))]
                to_i = direction[0]
                to_j = direction[1]
                cell_to_visit = self._cells[to_i][to_j]
                if to_i > i:
                    current_cell.has_right_wall = False
                    cell_to_visit.has_left_wall = False
                if to_i < i:
                    current_cell.has_left_wall = False
                    cell_to_visit.has_right_wall = False
                if to_j > j:
                    current_cell.has_bottom_wall = False
                    cell_to_visit.has_top_wall = False
                if to_j < j:
                    current_cell.has_top_wall = False
                    cell_to_visit.has_bottom_wall = False
                self._draw_cell(current_cell)
                self._draw_cell(cell_to_visit)
                self._break_walls_r(to_i, to_j)

    def _reset_cells_visited(self):
        for i in self._cells:
            for j in i:
                j.visited = False

        
    def solve(self):
        return self._solve_r(0,0)

    def _solve_r(self, i, j):
        self._animate()
        current_cell = self._cells[i][j]
        current_cell.visited = True
        if current_cell == self._cells[self.num_cols-1][self.num_rows-1]:
            return True
        directions = []
        if not current_cell.has_right_wall:
            directions.append((i+1, j))
        if not current_cell.has_bottom_wall:
            directions.append((i, j+1))
        if not current_cell.has_left_wall:
            directions.append((i-1, j))
        if not current_cell.has_top_wall:
            directions.append((i, j-1))
        for direction in directions:
            to_i = direction[0]
            to_j = direction[1]
            cell_to_visit = self._cells[to_i][to_j]
            if not cell_to_visit.visited:
                current_cell.draw_move(cell_to_visit)
                if self._solve_r(to_i, to_j):
                    return True
                else:
                    current_cell.draw_move(cell_to_visit, undo = True)
        return False


        