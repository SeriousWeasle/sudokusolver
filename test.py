import math
easytest = "2 1 9 3 1 3 6 1 7 9 1 6 1 2 8 3 2 7 4 2 9 7 2 2 8 2 3 9 2 4 1 3 5 4 3 6 5 3 8 9 3 9 3 4 9 4 4 1 7 4 5 2 5 1 3 5 2 4 5 5 6 5 8 8 5 7 9 5 3 1 6 3 4 6 7 5 6 6 7 6 9 8 6 2 5 7 7 6 7 1 5 8 4 7 8 1 9 8 5 4 9 2 6 9 6 7 9 3 8 9 4 9 9 7"
difftest = "2 1 5 4 1 4 9 1 2 1 2 3 7 2 7 8 2 4 9 2 5 1 4 4 6 4 2 7 4 3 9 4 8 1 5 7 3 5 3 4 5 1 7 5 4 8 5 2 3 6 8 5 6 7 9 6 1 3 7 2 6 7 1 8 7 8 9 7 4 4 8 6 5 8 4 6 8 9 6 9 7 7 9 6"

#Quick test for making the solver, more of a prototype
def main():
    grid = NewGrid()
    doing_setup = True

    #code for entering the current sudoku grid into the program
    while doing_setup:
        for g in grid:
            print(g)
        user_in = input("Please enter cell data in format\n[x, y, z]; x=x, y=y, z=cell start value\nType start to run solver\nOr enter exit to exit\n> ")
        if(user_in.lower() == "start"):
            doing_setup = False
        elif(user_in.lower() == "exit"):
            exit(0)
        elif(user_in.lower() == "easy"):
            args = easytest.split()
            if (len(args) % 3 == 0):
                for n in range(int(len(args) / 3)):
                    x = int(args[(n * 3) + 0])
                    y = int(args[(n * 3) + 1])
                    z = int(args[(n * 3) + 2])
                    grid[y - 1][x - 1] = z
        elif(user_in.lower() == "hard"):
            args = difftest.split()
            if (len(args) % 3 == 0):
                for n in range(int(len(args) / 3)):
                    x = int(args[(n * 3) + 0])
                    y = int(args[(n * 3) + 1])
                    z = int(args[(n * 3) + 2])
                    grid[y - 1][x - 1] = z
        else:
            args = user_in.split()
            if (len(args) % 3 == 0):
                for n in range(int(len(args) / 3)):
                    x = int(args[(n * 3) + 0])
                    y = int(args[(n * 3) + 1])
                    z = int(args[(n * 3) + 2])
                    grid[y - 1][x - 1] = z

    emptyCells = CountEmpty(grid)

    while emptyCells > 0:
        grid = DoSolveStep(grid)
        for g in grid: print(g)
        print()
        emptyCells = CountEmpty(grid)
        input()

def CountEmpty(grid):
    num_empty = 0
    for row in grid:
        for cell in row:
            if (cell == 0): num_empty += 1
    return num_empty

#Make 2d grid of empty arrays for storing possible numbers for each position
def NewPossibilityGrid():
    grid = []
    for n in range(9):
        row = []
        for m in range(9):
            row.append([])
        grid.append(row)
    return grid

#Make a new empty sudoku grid
def NewGrid():
    grid = []
    for n in range(9):
        grid.append([0, 0, 0, 0, 0, 0, 0, 0, 0])
    return grid

def GetPossibilityGrid(grid):
    nums_possible = NewPossibilityGrid()
    #go over every number in every cell
    for y in range(9):
        for x in range(9):

            #only check every number if cell is empty
            if (grid[y][x] == 0):
                for n in range(1, 10):
                    #go over current row
                    row_ok = n not in grid[y]

                    #go over current col
                    col = []
                    for i in range(9):
                        col.append(grid[i][x])
                        
                    col_ok = n not in col

                    #go over current block
                    block_x = math.floor(x / 3)
                    block_y = math.floor(y / 3)
                    block = []

                    for by in range(block_y * 3, (block_y * 3) + 3):
                        for bx in range(block_x * 3, (block_x * 3) + 3):
                            block.append(grid[by][bx])

                    block_ok = n not in block

                    if (row_ok and col_ok and block_ok):
                        nums_possible[y][x].append(n)
    return nums_possible

def CullPossibilities(nums_possible):
    #check if number is forced into top row
    #xxx xxx ---       xxx --- ---
    #--- xxx ---  -->  --- xxx ---
    #--- --- ---       --- --- ---
    return nums_possible

def IsOnlyOptionInCells(cellRange, num):
    count = 0
    for cell in cellRange:
        if num in cell:
            count += 1
    return count == 1

def DoSolveStep(grid):
    #get all possible fill-in locations
    nums_possible = GetPossibilityGrid(grid)
    solves = 0

    #go over grid and fill in possible cells via a naïve approach (only fill in cell if that is the only possible number)
    for y in range(9):
        for x in range(9):
            if (grid[y][x] == 0 and len(nums_possible[y][x]) == 1):
                print(f"[SIMPLE MODE] x:{x + 1}, y:{y + 1}, num:{nums_possible[y][x][0]}")
                grid[y][x] = nums_possible[y][x][0]
                nums_possible[y][x] = []
                solves += 1
    
    if(solves == 0):
        #check all rows if number only fits in cell
        for y in range(9):
            for x in range(9):
                #only check if cell is not already filled in
                if(grid[y][x] == 0 and len(nums_possible[y][x]) > 0):
                    for n in nums_possible[y][x]:
                        if(IsOnlyOptionInCells(nums_possible[y], n)):
                            print(f"[ROWS MODE] x:{x + 1}, y:{y + 1}, num:{n}")
                            grid[y][x] = n
                            nums_possible[y][x] = []
                            solves += 1

    if(solves == 0):
        #check all cols if number only fits in cell
        for y in range(9):
            for x in range(9):
                #only check if cell is not already filled in
                if(grid[y][x] == 0 and len(nums_possible[y][x]) > 0):
                    for n in nums_possible[y][x]:
                        col = []
                        for z in range(9):
                            col.append(nums_possible[z][x])
                        if(IsOnlyOptionInCells(col, n)):
                            print(f"[COLS MODE] x:{x + 1}, y:{y + 1}, num:{n}")
                            grid[y][x] = n
                            nums_possible[y][x] = []
                            solves += 1

    if (solves == 0):
        #check all blocks if number only fits in cell
        for y in range(9):
            for x in range(9):
                if(grid[y][x] == 0 and len(nums_possible[y][x]) > 0):
                    for n in nums_possible[y][x]:
                        block_x = math.floor(x / 3)
                        block_y = math.floor(y / 3)

                        block = []
                        for by in range(block_y * 3, (block_y * 3) + 3):
                            for bx in range(block_x * 3, (block_x * 3) + 3):
                                block.append(nums_possible[by][bx])
                        
                        if(IsOnlyOptionInCells(block, n)):
                            print(f"[BLOCKS MODE] x:{x + 1}, y:{y + 1}, num:{n}")
                            grid[y][x] = n
                            nums_possible[y][x] = []
                            solves += 1
    return grid

if __name__ == "__main__":
    main()