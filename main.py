from classes import Window, Line, Point, Cell, Maze


    
def main():
    win = Window(800, 600)
    maze = Maze(0, 0, 15, 10, 30, 30, win)
    win.wait_for_close()
    

main()