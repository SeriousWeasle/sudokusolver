import curses, math, time

#Load the help page from a seperate file as a constant
with open("./helppage.txt", "r") as hp:
    PROGRAM_HELPPAGE = hp.read()

#Constant for checking if characters that are to be parsed to ints are valid for input into the grid
VALID_CHARS = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]

#Class for handling cell-level logic and data storage
class Cell:
    def __init__(this):
        this.value = 0
        this.possibilities = []
    
    def __str__(this):
        return f"[{this.value}]"
    
    def CompleteStr(this):
        return f"val: {this.value}; pencil:{this.possibilities}"

class CellCollection:
    #Code for generic operations on collections of cells
    def __init__(this, cells):
        this.contents = cells
    
    def Contains(this, num):
        for cell in this.contents:
            if cell.value == num: return True
        return False

class Box(CellCollection):
    #Code specific for stuff to handle box-related stuff
    def __str__(this):
        returnstr = ""
        for i, cell in enumerate(this.contents):
            returnstr += str(cell)
            if(i % 3 == 2 and i < len(this.contents) - 1):
                returnstr += "\n"
        return returnstr

class Row(CellCollection):
    #Class for row-related operations
    def __str__(this):
        returnstr = ""
        for x, cell in enumerate(this.contents):
            returnstr += str(cell)
            if (x % 3 == 2 and x < len(this.contents) - 1): returnstr += " "
        return returnstr

class Col(CellCollection):
    #Class for column-related operations
    def __str__(this):
        returnstr = ""
        for y, cell in enumerate(this.contents):
            returnstr += str(cell)
            if (y < len(this.contents) - 1):
                returnstr += "\n"
                if (y % 3 == 2): returnstr += "\n"
        return returnstr

class SudokuGrid:
    #The actual sudoku grid, made up of an array of arrays of cells
    def __init__(this):
        this.grid = this.InitGrid()
        
    def InitGrid(this): #function for initializing the grid
        grid = []
        for y in range(9):
            row = []
            for x in range(9): row.append(Cell())
            grid.append(row)
        return grid
    
    def GetCell(this, x, y):
        return this.grid[y][x]
    
    def SetCell(this, x, y, val):
        this.grid[y][x].value = val
    
    def GetRow(this, y):
        return Row(this.grid[y])
    
    def GetCol(this, x):
        col = []
        for y in range(9): col.append(this.GetCell(x, y))
        return Col(col)
    
    def GetBox(this, bx, by):
        cells = []
        for y in range(3):
            for x in range(3):
                cells.append(this.grid[(by * 3) + y][(bx * 3) + x])
        return Box(cells)
    
    def GetBoxFromCell(this, x, y):
        return this.GetBox(math.floor(x / 3), math.floor(y / 3))
    
    def IsSolved(this):
        for row in this.grid:
            for cell in row:
                if cell.value == 0: return False
        return True
        
    def __str__(this):
        returnstr = ""
        for y, row in enumerate(this.grid):
            for x, cell in enumerate(row):
                returnstr += str(cell)
                if(x % 3 == 2 and x < len(row) - 1): returnstr += " "
            if (y < len(this.grid) - 1):
                returnstr += "\n"
                if (y % 3 == 2): returnstr += "\n"
        return returnstr

#class for setting colors of blocks and drawing a fancy grid to the terminal
class Render:
    #store a states grid for all numbers and a list of all cells being drawn as checked
    def __init__(this):
        pass

    def Draw(this, grid):
        print(grid)

class Solver:
    #Class for game logic and actual solving
    def __init__(this):
        this.sudoku = SudokuGrid()
        this.render = Render()

    def DoUserInput(this):
        doing_setup = True

        while(doing_setup):
            #Get the user input and split at spaces for args
            print("Enter command:")
            user_input = input("> ").lower()
            args = user_input.split(" ")

            if(len(args) == 1): #single argument commands
                this.HandleSingleArgs(args)
            
            elif(len(args) == 2): #two argument commands
                this.HandleTwoArgs(args)

            elif(len(args) == 4): #four argument commands -> only setting specific cells to a value
                this.HandleFourArgs(args)
                
            else:
                print("Command not recognised; type 'help' for available commands")

    def HandleSingleArgs(this, args):
        if(args[0] == "exit" or args[0] == "quit"):
            exit(0)

        elif (args[0] == "help"):
            print(PROGRAM_HELPPAGE)

        elif(args[0] == "start"):
            doing_setup = False
            
        elif(args[0] == "lines"):
            this.ParseLinesToGrid(this.InputByLines())

        else:
            print("Command not recognised; type 'help' for available commands")
    
    def HandleTwoArgs(this, args):
        if(args[0] == "load"):
            this.ParseLinesToGrid(this.LoadFromFile(args[1]))

        elif(args[0] == "save"):
            this.WriteGridToFile(args[1])

        else:
            print("Command not recognised; type 'help' for available commands")

    def HandleFourArgs(this, args):
        if(args[0] == "set"):
            try:
                x = int(args[1])
                y = int(args[2])
                val = int(args[3])

            except:
                print("Could not parse x, y and value to integers")
                
            if(y < 9 and x < 9 and val > -1 and val < 10):
                this.sudoku.SetCell(x, y, val)
                print(f"Current gamestate:\n{this.sudoku}")
            else: print(f"Specified coordinates out of range.\nRange xy=[0,8] val=[0,9]; got x:{x}, y:{y}, val:{val}")
        else:
            print("Command not recognised; type 'help' for available commands")

    def WriteGridToFile(this, filename):
        writestr = ""
        for y, row in enumerate(this.sudoku.grid):
            for cell in row:
                writestr += str(cell.value)
            if(y < 8): writestr += "\n"
        with open(f"./{filename}", "w") as wf:
            wf.write(writestr)

    def InputByLines(this):
        #Get puzzle in line-by-line mode
        print("Enter puzzle line by line. Use zeros or spaces for empty cells.")
        lines = []
        for i in range(9):
            line_ok = False
            while(not line_ok):
                line = input(f"Line {i + 1}: >")
                
                if("stop" in line.lower()): return ""
                if(line.lower() == "quit" or line.lower() == "exit"): exit(0)

                line_ok = len(line) == 9
                if(not line_ok): print(f"Expected 9 characters, got {len(line)}")
            lines.append(line)
        return lines
    
    def LoadFromFile(this, filename):
        with open(f"./{filename}", "r") as infile:
            lines = infile.readlines()
            for i, line in enumerate(lines): lines[i] = line.replace("\n", "")
            return lines

    def ParseLinesToGrid(this, lines):
        for y, line in enumerate(lines):
            for x, chr in enumerate(line):
                if (chr in VALID_CHARS):
                    this.sudoku.SetCell(x, y, int(chr))
        print(f"Current gamestate:\n{this.sudoku}")

    def RunSolver(this):
        while(not this.sudoku.IsSolved()):
            print("Doing solving step")
            time.sleep(0.1) #prevents code from running too fast incase of shenanigans

if __name__ == "__main__":
    solver = Solver()
    solver.DoUserInput()
    solver.RunSolver()