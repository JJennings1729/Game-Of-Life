import tkinter as tk
import numpy as np
import pickle
import time

BoardSelection = "Board Choices/R Pentomino"
SquareSize = 8
LiveColor = "#46e825"
Wait = 0.1

root = tk.Tk()
root.attributes('-fullscreen', True)
root.update()
Width = int(root.winfo_width() / SquareSize)
Height = int(root.winfo_height() / SquareSize)
canvas = tk.Canvas(root, width=Width*SquareSize, height=Height*SquareSize, bg='black')
canvas.pack()

class Board ():

    def __init__ (self, board):
        with open (board, 'rb') as file:
            self.board = pickle.load(file)   # Records whether cell is living/dead.

    def SetupBoard (self, event):
        x = int(event.x/SquareSize)
        y = int(event.y/SquareSize)
        cell = y * Width + x
        self.board[cell] = int(not self.board[cell])
        self.DrawSquare(cell)

    def LivingNeighbors (self, cell):   # Returns the total living neighbors of a cell. 
        A = bool(cell > Width-1)      # Off the top row true/false
        B = bool(cell < (Height-1)*Width)  # Off the bottom row true/false
        C = bool(cell % Width > 0)   # Off the left edge true/false
        D = bool(cell % Width < Width-1)   # Off the right edge true/false

        FindNeighbors = [-Width-1, -Width, -Width+1, -1, 0, 1, Width-1, Width, Width+1]
        FindBoundaries = [A&C, A, A&D, C, 0, D, B&C, B, B&D]
        Neighbors = 0
        for x in range(len(FindNeighbors)):
            if (FindBoundaries[x]):
                Neighbors += self.board[cell+FindNeighbors[x]]
        return Neighbors
    
    def DrawSquare (self, square):
        color = "black"
        if (self.board[square]):
            color = LiveColor
        x = square % Width
        y = np.floor(square/Width)
        canvas.create_rectangle(x*SquareSize, y*SquareSize, (x+1)*SquareSize, (y+1)*SquareSize, fill=color, outline="#606263")

    def DrawBoard (self):
        for square in range(len(self.board)):
            self.DrawSquare(square)

    def UpdateBoard (self):
        WillChange = []
        for cell in range(len(self.board)):
            NumNeighbors = self.LivingNeighbors(cell)
            if ((self.board[cell] == 0 and NumNeighbors == 3) or (self.board[cell] == 1 and not 1 < NumNeighbors < 4)):
                WillChange.append(cell)
        for cell in WillChange:
            self.board[cell] = int(not self.board[cell])
            self.DrawSquare(cell)

global MouseListen, GameRunning
MouseListen = True
GameRunning = True

def StartSimulation(event=None):
    print("Simulation Started")
    global MouseListen
    MouseListen = False

def Close(event=None):
    print("SHUTTING DOWN")
    root.quit()
    root.destroy()
    global GameRunning
    GameRunning = False
root.protocol("WM_DELETE_WINDOW", Close)

GameBoard = Board(BoardSelection)
GameBoard.DrawBoard()

def ExportBoard(event=None):
    with open('Board Choices/AAAAA New Save', 'wb') as file:
        pickle.dump(GameBoard.board, file)

while (MouseListen):
    root.bind("<Button-1>", GameBoard.SetupBoard)
    root.bind("s", ExportBoard)
    root.bind("<Return>", StartSimulation)
    root.update()

while (GameRunning):
    GameBoard.UpdateBoard()
    root.bind("<Return>", Close)
    root.update()
    time.sleep(Wait)