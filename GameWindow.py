import InputError
import tkinter as tk
import random as rand


class GameWindow:
    """"""

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

        self.root = tk.Tk()

        self._time = 0
        self._gameTable = []
        self._fields = []
        self._buttons = []
        self._howManyTimesRightButtonWasClicked = 0

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
        resetButton.grid(row=0, column=self._gameWindowRows // 2, )

        self._buttons = [counterOfMines, timer, resetButton]

    def initGameBoard(self):
        """"""

        self._fields = [[0] * self._gameWindowColumns] * self._gameWindowRows

        for i in range(self._gameWindowRows):
            for j in range(self._gameWindowColumns):
                if i == 0:
                    self._fields[i][j] = tk.Button(self.root, width=2, height=1)
                    self._fields[i][j].grid(row=j + 2, column=i, padx=(50, 0))
                    self._fields[i][j].bind('<Button-1>', )
                    self._fields[i][j].bind('<Button-3>', lambda event, p=self._fields[i][j]: self.rightButton(p))
                else:
                    self._fields[i][j] = tk.Button(self.root, width=2, height=1)
                    self._fields[i][j].grid(row=j + 2, column=i)
                    self._fields[i][j].bind('<Button-1>', )
                    self._fields[i][j].bind('<Button-3>', lambda event, p=self._fields[i][j]: self.rightButton(p))

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
                    for k in range(i - 1, i + 2):
                        if self._gameWindowColumns > k >= 0:
                            for m in range(j - 1, j + 2):
                                if 0 <= m < self._gameWindowRows and self._gameTable[k][m] != -1:
                                    self._gameTable[k][m] += 1

    def rightButton(self, button):

        if button['text'] == '':
            button['text'] = 'f'
            self._howManyTimesRightButtonWasClicked += 1
            self.checkField()
        elif button['text'] == 'f':
            button['text'] = '?'
            self._howManyTimesRightButtonWasClicked += 1
            self.checkField(False)
        else:
            button['text'] = ''
            self._howManyTimesRightButtonWasClicked = 0

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


if __name__ == '__main__':
    gw = GameWindow(4, 12, 20)
    gw.initUpperGamePanel()
    gw.getRandomFieldsForMines()
    gw.initGameBoard()
    gw.initGameTable()
    gw.root.mainloop()
