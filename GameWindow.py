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

    def getSizeOfGameWindow(self):
        self._topLevel = tk.Toplevel(self.root)
        self._topLevel.title('Init Game Window.')
        self._topLevel.grab_set()

        labelRows = tk.Label(self._topLevel, text='Number of rows: ',
                             font=8, padx=20, pady=10) \
            .grid(row=0, column=0)
        labelColumns = tk.Label(self._topLevel, text='Number of column: ',
                                font=8, padx=20, pady=10) \
            .grid(row=1, column=0)
        labelMines = tk.Label(self._topLevel, text='Number of mines: ',
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
        resetButton.bind('<Button-1>', lambda event: self.getSizeOfGameWindow())
        resetButton.grid(row=0, column=self._gameWindowRows // 2)

        self._buttons = [counterOfMines, timer, resetButton]

    def initGameBoard(self):
        """"""

        # self._fields = [[0] * self._gameWindowRows] * self._gameWindowColumns
        self._fields = [[tk.Button(self.root, width=2, height=1) for _ in range(self._gameWindowColumns)]
                        for _ in range(self._gameWindowRows)]

        for i in range(self._gameWindowRows):
            for j in range(self._gameWindowColumns):
                if i == 0:
                    # self._fields[i][j] = tk.Button(self.root, width=2, height=1)
                    self._fields[i][j].grid(row=j + 2, column=i, padx=(50, 0))
                    self._fields[i][j].bind('<Button-1>',
                                            lambda event, p=self._fields[i][j], x=i, y=j: self.leftButton(p, x, y))
                    self._fields[i][j].bind('<Button-3>', lambda event, p=self._fields[i][j]: self.rightButton(p))
                else:
                    # self._fields[i][j] = tk.Button(self.root, width=2, height=1)
                    self._fields[i][j].grid(row=j + 2, column=i)
                    self._fields[i][j].bind('<Button-1>',
                                            lambda event, p=self._fields[i][j], x=i, y=j: self.leftButton(p, x, y))
                    self._fields[i][j].bind('<Button-3>', lambda event, p=self._fields[i][j]: self.rightButton(p))
        print(self._fields)

    def initGameTable(self):
        self._gameTable = [[0 for _ in range(self._gameWindowRows)] for _ in range(self._gameWindowColumns)]

        randomFieldsForMines = self.getRandomFieldsForMines()

        for i in range(self._numberOfMines):
            y = randomFieldsForMines[i][0]
            x = randomFieldsForMines[i][1]
            self._gameTable[y][x] = -1

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

        for i in range(self._gameWindowColumns):
            for j in range(self._gameWindowRows):
                if self._gameTable[i][j] == -1:
                    self.findNeighbours(i, j)
        print(self._gameTable)

    def findNeighbours(self, i, j):
        for k in range(i - 1, i + 2):
            if self._gameWindowColumns > k >= 0:
                for m in range(j - 1, j + 2):
                    if not (m == j and k == i):
                        if 0 <= m < self._gameWindowRows and self._gameTable[k][m] != -1:
                            self._gameTable[k][m] += 1

    def rightButton(self, button):

        if button['text'] == '':
            button['text'] = 'f'
            self.checkField()
        elif button['text'] == 'f':
            button['text'] = '?'
            self.checkField(False)
        else:
            button['text'] = ''

    def leftButton(self, button, i, j):

        if self._gameTable[j][i] == -1:
            button['text'] = 'X'
            # koniec gry
        else:
            # self.updateButton(button, i, j)
            pass

    def updateButton(self, button, i, j):

        self.disableButton(button, i, j)

        if self._gameTable[i][j] > 0:
            button['text'] = self._gameTable[j][i]
        else:
            for x in range(i - 1, i + 2):
                if self._gameWindowColumns > x >= 0:
                    for y in range(j - 1, j + 2):
                        if self._gameWindowRows > y >= 0 and not (i == x and j == y):
                            if isinstance(self._fields[y][x], tk.Button) and self._gameTable[y][x] != -1:
                                self.updateButton(self._fields[y][x], y, x)

    def disableButton(self, button, i, j):
        button.configure(state='disable', border=1)
        button.unbind('<Button-1>')
        button.unbind('<Button-3>')

        button = tk.Label(self.root)

        if i == 0:
            button.grid(row=j + 2, column=i, padx=(50, 0))
        else:
            button.grid(row=j + 2, column=i)

    def startTimer(self, timer):

        zerosLeft = 4 - len(str(self._time))
        timer['text'] = zerosLeft * '0' + str(self._time)
        self._time += 1
        self.root.after(1000, self.startTimer, timer)

    def checkField(self, condition=True):

        if condition:
            self._numberOfMines -= 1
        else:
            self._numberOfMines += 1

        if self._numberOfMines >= 0:
            zerosLeft = 4 - len(str(self._numberOfMines))
            self._buttons[0]['text'] = zerosLeft * '0' + str(self._numberOfMines)

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
    gw.getSizeOfGameWindow()
    gw.initUpperGamePanel()
    gw.getRandomFieldsForMines()
    gw.initGameBoard()
    gw.initGameTable()
    gw.root.mainloop()
