import pygame 
import random
pygame.init() #initialize pygame
window = pygame.display.set_mode((600, 600)) #create window(with size parameters)
pygame.display.set_caption("SUDOKU")

#colours
BLACK = (0, 0, 0) 
WHITE = (255, 255, 255)
BLUE = (170, 240, 240)  #for highlighting the selected cell
RED = (255, 182, 193)  # for error
GREEN = (144, 238, 144)  # for winning state

gridSize = 540
cellSize = gridSize // 9 
startX = (600 - gridSize) // 2  #stars for x
startY = (600 - gridSize) // 2  #start for y

#empty sudoku grid
sudokuGrid = [[0 for _ in range(9)] for _ in range(9)]
editableCells = [[True] * 9 for _ in range(9)]


"""
#start grid
initialSudokuGrid = [
    [1, 0, 7,  0, 0, 6,  4, 5, 0],
    [0, 2, 5,  3, 4, 0,  0, 0, 8],
    [0, 6, 0,  0, 0, 1,  0, 7, 0],
    
    [0, 5, 3,  0, 0, 0,  0, 2, 9],
    [6, 1, 0,  0, 0, 9,  8, 0, 0],
    [0, 0, 0,  6, 0, 2,  0, 0, 7],
    
    [0, 0, 1,  0, 9, 3,  2, 0, 0],
    [0, 0, 8,  0, 0, 0,  0, 0, 0],
    [0, 4, 0,  0, 7, 8,  5, 9, 1]
]

sudokuGrid = [row[:] for row in initialSudokuGrid] 
editableCells = [[True if cell == 0 else False for cell in row] for row in sudokuGrid]
"""


font = pygame.font.Font(None, 40) #font for numbers
winFont = pygame.font.Font(None, 70)  # font for winning text
buttonFont = pygame.font.Font(None, 50)  # font for button text

#for tracking selected cell
selectedRow = None
selectedCol = None
invalidCells = set()  #for invalid cells
gameWon = False  #tracking game status


#check, if the number follows sudoku's rules
def isValidMove(grid, row, col, number):
    for c in range(9):
        if grid[row][c] == number and c != col:
            return False
    
    for r in range(9):
        if grid[r][col] == number and r != row:
            return False
    
    start_row, start_col = 3 * (row // 3), 3 * (col // 3)
    for r in range(start_row, start_row + 3):
        for c in range(start_col, start_col + 3):
            if grid[r][c] == number and (r, c) != (row, col):
                return False

    return True



#backtracking algorithm to generate a complete Sudoku grid
def fillGrid(grid):
    empty = findEmpty(grid)
    if not empty:
        return True  

    row, col = empty

    numbers = list(range(1, 10))
    random.shuffle(numbers)

    for number in numbers:
        if isValidMove(grid, row, col, number):
            grid[row][col] = number

            if fillGrid(grid):
                return True

            grid[row][col] = 0  

    return False

#find an empty cell
def findEmpty(grid):
    for row in range(9):
        for col in range(9):
            if grid[row][col] == 0:
                return (row, col)
    return None

#removing random numbers from a complete grid
def removeNumbers(grid, difficulty=40):
    cells_to_remove = difficulty  
    attempts = 0 
    while cells_to_remove > 0 and attempts < 1000:
        row, col = random.randint(0, 8), random.randint(0, 8)
        if grid[row][col] != 0:
            grid[row][col] = 0
            cells_to_remove -= 1
        attempts += 1

#generate start sudoku grid
def generateSudoku():
    global sudokuGrid, editableCells
    sudokuGrid = [[0 for _ in range(9)] for _ in range(9)]  
    editableCells = [[True] * 9 for _ in range(9)]

    fillGrid(sudokuGrid)

    removeNumbers(sudokuGrid)

    editableCells = [[True if sudokuGrid[row][col] == 0 else False for col in range(9)] for row in range(9)]


#checking game status(cells status)
def checkWin(grid):
    for row in range(9):
        for col in range(9):
            num = grid[row][col]
            if num == 0 or not isValidMove(grid, row, col, num):
                return False
    return True


#draw buttun
def drawButton(x, y, w, h, text):
    pygame.draw.rect(window, GREEN, (x, y, w, h))
    textSurface = buttonFont.render(text, True, BLACK)
    textRect = textSurface.get_rect(center=(x + w // 2, y + h // 2))
    window.blit(textSurface, textRect)


#game loop
running = True
generateSudoku()
while running:
    window.fill(WHITE)  #white background

    if gameWon:
        for row in range(9):
            for col in range(9):
                pygame.draw.rect(window, GREEN, (
                    startX + col * cellSize, startY + row * cellSize, cellSize, cellSize))

        #display the message
        winText = winFont.render("You Win!", True, BLACK)
        winTextRect = winText.get_rect(center=(300, 300))
        window.blit(winText, winTextRect)

        #draw the button
        drawButton(200, 450, 200, 50, "New Game")
    else:
        #draw the grid
        for i in range(10):
            lineWidth = 1 if i % 3 != 0 else 3

            #draw vertical lines
            pygame.draw.line(window, BLACK,
                             (startX + i * cellSize, startY),
                             (startX + i * cellSize, startY + gridSize),
                             lineWidth)

            #draw horizontal lines
            pygame.draw.line(window, BLACK,
                             (startX, startY + i * cellSize),
                             (startX + gridSize, startY + i * cellSize),
                             lineWidth)
        

        #draw the numbers
        for row in range(9):
            for col in range(9):
                num = sudokuGrid[row][col]
                if num != 0: 
                    text_color = BLACK 

                    #highlight invalid cells
                    if (row, col) in invalidCells:
                        pygame.draw.rect(window, RED, 
                                        (startX + col * cellSize, startY + row * cellSize, cellSize, cellSize))

                    text = font.render(str(num), True, text_color) #render the numbers  (str, colour)
                    #center the number
                    text_rect = text.get_rect(center=( 
                        startX + col * cellSize + cellSize // 2, 
                        startY + row * cellSize + cellSize // 2
                    ))

                    window.blit(text, text_rect) #draw number in cell

        #highlight the selected cell
        if selectedRow is not None and selectedCol is not None:
            pygame.draw.rect(window, BLUE, (
                startX + selectedCol * cellSize, 
                startY + selectedRow * cellSize, 
                cellSize, cellSize), 3)
        

    for event in pygame.event.get(): #keep the window open
        if event.type == pygame.QUIT:
            running = False


        #handle mouse click
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouseX, mouseY = pygame.mouse.get_pos()
            if gameWon:
                #check if the button was clicked
                if 200 <= mouseX <= 400 and 450 <= mouseY <= 500:
                    #reset the game state
                    gameWon = False
                    generateSudoku()
                    invalidCells.clear()
                    selectedRow, selectedCol = None, None
            else:
                #check if a cell is clicked
                if startX <= mouseX <= startX + gridSize and startY <= mouseY <= startY + gridSize:
                    selectedCol = (mouseX - startX) // cellSize
                    selectedRow = (mouseY - startY) // cellSize


        #handle key press
        if event.type == pygame.KEYDOWN and selectedRow is not None and selectedCol is not None:

            #checking number and cell and print the number
            if editableCells[selectedRow][selectedCol]:
                if event.key in range(pygame.K_1, pygame.K_9 + 1):
                    number = event.key - pygame.K_0
                    sudokuGrid[selectedRow][selectedCol] = number

                    #check for validity
                    if isValidMove(sudokuGrid, selectedRow, selectedCol, number):
                        invalidCells.discard((selectedRow, selectedCol))  
                    else:
                        invalidCells.add((selectedRow, selectedCol))  

                #clean the cell 
                elif event.key == pygame.K_DELETE or event.key == pygame.K_BACKSPACE:
                    sudokuGrid[selectedRow][selectedCol] = 0
                    invalidCells.discard((selectedRow, selectedCol))

            # Check if the game has been won
            if checkWin(sudokuGrid):
                gameWon = True

    pygame.display.flip()  #update the display

pygame.quit() #quit pygame

