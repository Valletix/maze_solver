from classes import Window, Line, Point, Cell
from maze import Maze


    
def main():
    win = Window(800, 600)
    maze = Maze(0, 0, 15, 15, 30, 30, win)
    maze.solve()
    win.wait_for_close()
    

main()