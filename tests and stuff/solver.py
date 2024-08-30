class SudokuBoard:
    def __init__(self):
        self.board = []

        for i in range(9):
            self.board.append([0, 0, 0, 0, 0, 0, 0, 0, 0])

    #todo -> make fancier renderer
    def __str__(self):
        retstr = ""
        for r in range(9):
            retstr += str(self.board[r])
            if (r < 8): retstr += "\n"
        return retstr
    
    def GetCell(self, x, y):
        return self.board[y][x]
    
    def SetCell(self, x, y, n):
        self.board[y][x] = n

    def GetBlock(self, x, y):
        x_offset = x * 3
        y_offset = y * 3

        block = []
        for yb in range(3):
            row = []
            for xb in range(3):
                row.append(self.GetCell(x_offset + xb, y_offset + yb))
            block.append(row)
        return block
    
    def PrintBlock(self, x, y):
        printstr = ""
        block = self.GetBlock(x, y)
        for i in range(3):
            printstr += str(block[i])
            if (i < 2): printstr += "\n"
        print(printstr)
    
test = SudokuBoard()

test.SetCell(4, 0, 5)
test.SetCell(4, 1, 2)
print(test.GetCell(4, 1))

print(test)
test.PrintBlock(1, 0)