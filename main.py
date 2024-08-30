import curses, math

#Class for containing board and getting/setting cells on it
class SudokuBoard:
    def __init__(self):
        #make the board an array of 9 arrays, each containing 9 zero's. Each array is a row and each item in array is a cell
        self.board = []

        for i in range(9):
            self.board.append([0, 0, 0, 0, 0, 0, 0, 0, 0])
    
    #Get the value of a cell at position x, y on the board
    def GetCell(self, x, y):
        return self.board[y][x]
    
    #set the value of a cell at position x, y on the board
    def SetCell(self, x, y, n):
        self.board[y][x] = n

#Class for rendering the board to the terminal
class Render:
    def __init__(self):
        pass
    
    def ColorCheck(self):
        for i in range(0, min(255, curses.COLORS)):
            try:
                for i in range(0, 256):
                    x = (i % 16) * 4
                    y = math.floor(i / 16)
                    stdscr.addstr(y, x, str(i).rjust(4), curses.color_pair(i))
            except curses.ERR:
                pass
        stdscr.getch()

#Main program
if __name__ == "__main__":
    stdscr = curses.initscr()
    curses.start_color()
    stdscr.clear()
    stdscr.refresh()
    curses.use_default_colors()
    for i in range(0, min(255, curses.COLORS)):
        curses.init_pair(i + 1, i, -1)

    board = SudokuBoard()
    render = Render()

    render.ColorCheck()