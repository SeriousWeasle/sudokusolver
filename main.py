import curses, math

class Cell:
    def __init__(self):
        self.value = 0
        self.pencilmarks = []
    
    def __str__(self):
        return f"val: {self.value}; pencil: {self.pencilmarks}"

class Box:
    def __init__(self, cells):
        self.contents = [[], [], []]
        for idx, cell in enumerate(cells):
            self.contents[math.floor(idx / 3)].append(cell)

class SudokuGrid:
    def __init__(self):
        self.grid = self.InitGrid()
        
    def InitGrid(): #function for initializing the grid
        grid = []
        for y in range(9):
            row = []
            for x in range(9): row.append(Cell())
            grid.append(Cell())
        return grid
    
    def GetCell(self, x, y):
        return self.grid[y][x]
    
    def GetRow(self, y):
        return self.grid[y]
    
    def GetCol(self, x):
        col = []
        for y in range(9): col.append(self.GetCell(x, y))
        return col
    
    def GetBox(self, bx, by):


if __name__ == "__main__":
    cell = Cell()
    print(cell)