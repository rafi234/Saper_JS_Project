from tkinter.font import *

import InputError
import tkinter as tk
import random as rand


class GameWindow:
    """"""
    root = tk.Tk()

    def __init__(self, game_window_columns, game_window_rows, number_of_mines):
        """Game window parameters initialization."""

        if 15 <= game_window_rows or 15 <= game_window_columns or game_window_rows <= 2 or game_window_columns <= 2:
            raise InputError
        else:
            self._gameWindowRows = game_window_rows
            self._gameWindowColumns = game_window_columns

        if game_window_columns * game_window_rows > number_of_mines <= 0:
            raise InputError
        else:
            self._numberOfMines = number_of_mines

        self._time = 0
        self._gameTable = []
        self._fields = []
        self._buttons = []
        self._topLevel = None
        self._columnsIV = 0
        self._rowsIV = 0
        self._minesIV = 0
        self.__entryColumns = None
        self.__entryRows = None
        self.__entryMines = None
        self._emptyFields = game_window_rows * game_window_columns - number_of_mines

    def getSizeOfNewGameWindow(self, ):

        self._topLevel = tk.Toplevel(self.root)
        self._topLevel.title('Init Game Window.')
        self._topLevel.grab_set()

        tk.Label(self._topLevel, text='Number of rows: ',
                 font=8, padx=20, pady=10) \
            .grid(row=0, column=0)
        tk.Label(self._topLevel, text='Number of column: ',
                 font=8, padx=20, pady=10) \
            .grid(row=1, column=0)
        tk.Label(self._topLevel, text='Number of mines: ',
                 font=8, padx=20, pady=10) \
            .grid(row=2, column=0)

        self._columnsIV = tk.IntVar()
        self._rowsIV = tk.IntVar()
        self._minesIV = tk.IntVar()

        self.__entryRows = tk.Entry(self._topLevel, text=self._rowsIV)
        self.__entryRows.grid(row=0, column=1)
        self.__entryColumns = tk.Entry(self._topLevel, text=self._columnsIV)
        self.__entryColumns.grid(row=1, column=1)
        self.__entryMines = tk.Entry(self._topLevel, text=self._minesIV)
        self.__entryMines.grid(row=2, column=1)

        saveButton = tk.Button(self._topLevel, text='Save')
        saveButton.bind('<Button-1>', lambda event: self.resetGame())
        saveButton.grid(row=4, column=0)

        cancelButton = tk.Button(self._topLevel, text='Cancel')
        cancelButton.bind('<Button-1>', lambda event: self._topLevel.destroy())
        cancelButton.grid(row=4, column=1)

    def initUpperGamePanel(self):
        """"""

        counterOfMines = tk.Label(self.root, bg='black', fg='red', font=('Times New Roman', 20))
        counterOfMines.grid(row=0, column=0, columnspan=7, sticky=tk.W, padx=3)
        zeros = 4 - len(str(self._numberOfMines))
        counterOfMines['text'] = zeros * '0' + str(self._numberOfMines)

        timer = tk.Label(self.root, bg='black', fg='red', font=('Times New Roman', 20))
        timer.grid(row=0, column=self._gameWindowRows, columnspan=7, sticky=tk.E, padx=3)
        self.startTimer(timer)

        resetButton = tk.Button(self.root, width=3, height=1, text='reset')
        resetButton.bind('<Button-1>', lambda event: self.getSizeOfNewGameWindow())
        resetButton.grid(row=0, column=self._gameWindowRows // 2)

        self._buttons = [counterOfMines, timer, resetButton]

    def initGameBoard(self):
        """"""

        self._fields = [[tk.Button(self.root, width=2, height=1) for _ in range(self._gameWindowColumns)]
                        for _ in range(self._gameWindowRows)]

        for i in range(self._gameWindowColumns):
            for j in range(self._gameWindowRows):
                if i == 0:
                    self._fields[j][i].grid(row=j + 2, column=i, padx=(50, 0))
                    self._fields[j][i].bind('<Button-1>',
                                            lambda event, p=self._fields[j][i], x=j, y=i: self.leftButton(p, x, y))
                    self._fields[j][i].bind('<Button-3>',
                                            lambda event, p=self._fields[j][i], x=i, y=j: self.rightButton(p, x, y))
                else:
                    self._fields[j][i].grid(row=j + 2, column=i)
                    self._fields[j][i].bind('<Button-1>',
                                            lambda event, p=self._fields[j][i], x=j, y=i: self.leftButton(p, x, y))
                    self._fields[j][i].bind('<Button-3>',
                                            lambda event, p=self._fields[j][i], x=i, y=j: self.rightButton(p, x, y))

    def initGameTable(self):

        self._gameTable = [[0 for _ in range(self._gameWindowColumns)] for _ in range(self._gameWindowRows)]

        randomFieldsForMines = self.getRandomFieldsForMines()

        for i in range(self._numberOfMines):
            y = randomFieldsForMines[i][0]
            x = randomFieldsForMines[i][1]
            self._gameTable[x][y] = -1

        self.checkNeighbours()

    def getRandomFieldsForMines(self):

        tempNumberOfMines = self._numberOfMines
        tabWithRandomFieldsForMines = []

        while tempNumberOfMines:
            randXY = [rand.randint(0, self._gameWindowColumns - 1), rand.randint(0, self._gameWindowRows - 1)]
            if randXY not in tabWithRandomFieldsForMines:
                tabWithRandomFieldsForMines.append(randXY)
                tempNumberOfMines -= 1

        return tabWithRandomFieldsForMines

    def checkNeighbours(self):

        for i in range(self._gameWindowRows):
            for j in range(self._gameWindowColumns):
                if self._gameTable[i][j] == -1:
                    self.findNeighbours(i, j)
        print(self._gameTable)

    def findNeighbours(self, i, j):

        for k in range(j - 1, j + 2):
            if self._gameWindowColumns > k >= 0:
                for m in range(i - 1, i + 2):
                    if not (m == i and k == j):
                        if 0 <= m < self._gameWindowRows and self._gameTable[m][k] != -1:
                            self._gameTable[m][k] += 1

    def rightButton(self, button, i, j):

        if button['text'] == '':
            button['text'] = 'f'
            self.checkField()
            self.checkIfGameIsOver()
        elif button['text'] == 'f':
            button['text'] = '?'
            self.checkField(False)
        else:
            button['text'] = ''

    def checkIfGameIsOver(self):
        if self._numberOfMines == 0:
            if self._emptyFields == self.countAllLabelFields():
                self.initGameOverWindow()

    def countAllLabelFields(self):

        counter = 0
        for i in range(self._gameWindowColumns):
            for j in range(self._gameWindowRows):
                if isinstance(self._fields[j][i], tk.Label):
                    counter += 1

        return counter

    def initGameOverWindow(self, condition=True):

        gameWinWindowTopLevel = tk.Toplevel(self.root)
        gameWinWindowTopLevel.grab_set()
        if condition:
            message = "YOU WON!!!"
        else:
            message = "YOU LOST!!!"

        tk.Label(gameWinWindowTopLevel,
                 text=message, font=40, padx=50, pady=30).grid(row=0, column=0, columnspan=5)

        nextGameButton = tk.Button(gameWinWindowTopLevel, text='Next Game')
        nextGameButton.bind('<Button-1>', lambda event: self.getSizeOfNewGameWindow())
        nextGameButton.grid(row=1, column=0)

        exitButton = tk.Button(gameWinWindowTopLevel, text='Exit')
        exitButton.bind('<Button-1>', lambda event: self.closeGame(gameWinWindowTopLevel))
        exitButton.grid(row=1, column=1)

    def closeGame(self, gameWinWindowTopLevel):
        gameWinWindowTopLevel.destroy()
        self.root.destroy()

    def checkField(self, condition=True):

        if condition:
            self._numberOfMines -= 1
        else:
            self._numberOfMines += 1

        if self._numberOfMines >= 0:
            zerosLeft = 4 - len(str(self._numberOfMines))
            self._buttons[0]['text'] = zerosLeft * '0' + str(self._numberOfMines)

    def leftButton(self, button, i, j):

        if self._gameTable[i][j] == -1:
            for i in range(self._gameWindowRows):
                for j in range(self._gameWindowColumns):
                    if self._gameTable[i][j] == -1:
                        self._fields[i][j]['text'] = 'X'
            self.initGameOverWindow(False)
        else:
            self.updateButton(button, i, j)

        self.checkIfGameIsOver()

    def updateButton(self, button, i, j):

        if isinstance(button, tk.Button) and button['state'] != 'disabled':
            self.disableButton(i, j)
            if self._gameTable[i][j] > 0:
                self.displayButton(i, j)
            else:
                self.findAllZeroFieldsRecursion(i, j)

    def findAllZeroFieldsRecursion(self, i, j):
        for x in range(i - 1, i + 2):
            if self._gameWindowRows > x >= 0:
                for y in range(j - 1, j + 2):
                    if self._gameWindowColumns > y >= 0 and not (i == x and j == y):
                        self.updateButton(self._fields[x][y], x, y)

    def displayButton(self, i, j):

        if j == 0:
            self._fields[i][j].grid(row=i + 2, column=j, padx=(50, 0))
        else:
            self._fields[i][j].grid(row=i + 2, column=j)

    def disableButton(self, i, j):

        self._fields[i][j].configure(state='disabled', border=1)
        self._fields[i][j].unbind('<Button-1>')
        self._fields[i][j].unbind('<Button-3>')

        number = self._gameTable[i][j]
        myFont = Font(self.root, size=10, weight=BOLD)
        if number == 1:
            self._fields[i][j] = tk.Label(self.root,
                                          text=str(number),
                                          foreground='blue',
                                          font=myFont)
        elif number == 2:
            self._fields[i][j] = tk.Label(self.root,
                                          text=str(number),
                                          foreground='green',
                                          font=myFont)
        elif number == 3:
            self._fields[i][j] = tk.Label(self.root,
                                          text=str(number),
                                          foreground='red',
                                          font=myFont)
        elif number == 4:
            self._fields[i][j] = tk.Label(self.root,
                                          text=str(number),
                                          foreground='#000066',
                                          font=myFont)
        elif number == 5:
            self._fields[i][j] = tk.Label(self.root,
                                          text=str(number),
                                          foreground='#FFEBEE',
                                          font=myFont)
        elif number == 6:
            self._fields[i][j] = tk.Label(self.root,
                                          text=str(number),
                                          foreground='#455A64',
                                          font=myFont)
        elif number == 7:
            self._fields[i][j] = tk.Label(self.root,
                                          text=str(number),
                                          foreground='#FFD740',
                                          font=myFont)
        elif number == 8:
            self._fields[i][j] = tk.Label(self.root,
                                          text=str(number),
                                          foreground='#E9C2A6',
                                          font=myFont)
        else:
            self._fields[i][j] = tk.Label(self.root)

    def startTimer(self, timer):

        zerosLeft = 4 - len(str(self._time))
        timer['text'] = zerosLeft * '0' + str(self._time)
        self._time += 1
        self.root.after(1000, self.startTimer, timer)

    def resetGame(self):

        self.setGameWindowRows(self._rowsIV.get())
        self.setGameWindowColumn(self._columnsIV.get())
        self.setNumberOfMines(self._minesIV.get())
        self._topLevel.destroy()
        self.root.destroy()
        self._time = 0
        self.root = tk.Tk()
        self.initUpperGamePanel()
        self.initGameBoard()
        self.initGameTable()

    def setGameWindowColumn(self, new):
        if 15 > new > 2:
            self._gameWindowColumns = new
        else:
            raise InputError

    def setGameWindowRows(self, new):
        if 15 > new > 2:
            self._gameWindowRows = new
        else:
            raise InputError

    def setNumberOfMines(self, new):
        if self._gameWindowColumns * self._gameWindowRows >= new > 0:
            self._numberOfMines = new
        else:
            raise InputError


if __name__ == '__main__':
    gw = GameWindow(4, 5, 2)
    gw.getSizeOfNewGameWindow()
    gw.initUpperGamePanel()
    gw.getRandomFieldsForMines()
    gw.initGameBoard()
    gw.initGameTable()
    gw.root.mainloop()
