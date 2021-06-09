from tkinter.font import *

from saper.saperMyException import InputError
import tkinter as tk
import random as rand


class GameWindow:
    """This class has been made to implement mini game \"Saper\""""

    root = tk.Tk()
    CHEAT_CODE = 'xyzzy'

    def __init__(self):
        """Game window parameters initialization.

        Parameters:
            _gameWindowRows, _gameWindowColumns - size of game board,
            _numberOfMines - number of mines,
            _time - stores number of seconds player is playing on current game table,
            _gameTable - 2D list which stores whole game logic
                        (where mines are, empty fields and fields which numbers),
            _gameButtons - 2D list stores all buttons on game board,
            _upperPanelButtons - list of buttons on upper panel,
            _topLevel - if needed, are used to display window where player can resize game board
            _columnsIV, _rowsIV, _minesIV - stores new size of game board and number of mines,
            _emptyFields - number of fields without mines.
        """

        self._gameWindowRows = 0
        self._gameWindowColumns = 0
        self._numberOfMines = 0
        self._time = 0
        self._gameTable = []
        self._gameButtons = []
        self._upperPanelButtons = []
        self._topLevel = None
        self._columnsIV = 0
        self._rowsIV = 0
        self._minesIV = 0
        self._emptyFields = 0
        self._writtenCodeToCheats = ''

    def __repr__(self):
        return 'GameWindow' \
               '(_gameWindowRows = {},\n' \
               '_gameWindowColumns = {},\n' \
               '_numberOfMines = {},\n' \
               '_time = {},\n' \
               '_gameTable = {},\n' \
               '_gameButtons = {},\n' \
               '_upperPanelButtons = {},\n' \
               '_topLevel = {},\n' \
               '_columnsIV = {},\n' \
               '_rowsIV = {},\n' \
               '_minesIV = {},\n' \
               '_emptyFields = {},\n' \
               '_writtenCodeToCheats = {}\n' \
               ')' \
            .format(self._gameWindowRows,
                    self._gameWindowColumns,
                    self._numberOfMines,
                    self._time,
                    self._gameTable,
                    self._gameButtons,
                    self._upperPanelButtons,
                    self._topLevel,
                    self._columnsIV,
                    self._rowsIV,
                    self._minesIV,
                    self._emptyFields,
                    self._writtenCodeToCheats
                    )

    def startGame(self):
        """This method set up new game Window and starts the game."""
        self.getSizeOfNewGameWindow()

    def resetGame(self, newRows, newColumns, newMines):
        """This method restarts game."""

        self.gameWindowRows = newRows
        self.gameWindowColumns = newColumns
        self.numberOfMines = newMines

        self.setEmptyFields()
        self._topLevel.destroy()
        self.root.destroy()
        self._time = 0
        self.root = tk.Tk()
        self.cheatsXYZZY()
        self.initUpperGamePanel()
        self.initGameBoardWithButtons()
        self.initGameTable()

    def getSizeOfNewGameWindow(self):
        """ This method is used to reset all Saper fields """

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

        entryRows = tk.Entry(self._topLevel, text=self._rowsIV)
        entryRows.grid(row=0, column=1)
        entryColumns = tk.Entry(self._topLevel, text=self._columnsIV)
        entryColumns.grid(row=1, column=1)
        entryMines = tk.Entry(self._topLevel, text=self._minesIV)
        entryMines.grid(row=2, column=1)

        saveButton = tk.Button(self._topLevel, text='Save')
        saveButton.bind('<Button-1>',
                        lambda event: self.resetGame(self._rowsIV.get(), self._columnsIV.get(), self._minesIV.get()))
        saveButton.grid(row=4, column=0)

        cancelButton = tk.Button(self._topLevel, text='Cancel')
        cancelButton.bind('<Button-1>', lambda event: self._topLevel.destroy())
        cancelButton.grid(row=4, column=1)

    def initUpperGamePanel(self):
        """
        Initialization on upper panel:
            - clock,
            - counter of mines,
            - button to reset game.
        """

        counterOfMines = tk.Label(self.root, bg='black', fg='red', font=('Times New Roman', 20))
        counterOfMines.grid(row=0, column=0, columnspan=10, sticky=tk.W, padx=3)
        zeros = 4 - len(str(self._numberOfMines))
        counterOfMines['text'] = zeros * '0' + str(self._numberOfMines)

        timer = tk.Label(self.root, bg='black', fg='red', font=('Times New Roman', 20))
        timer.grid(row=0, column=self._gameWindowRows, columnspan=10, sticky=tk.E, padx=3)
        self.startTimer(timer)

        resetButton = tk.Button(self.root, width=3, height=1, text='reset')
        resetButton.bind('<Button-1>', lambda event: self.getSizeOfNewGameWindow())
        resetButton.grid(row=0, column=self._gameWindowRows // 2)

        self._upperPanelButtons = [counterOfMines, timer, resetButton]

    def initGameBoardWithButtons(self):
        """This method fill whole game board with buttons and connect them with proper function."""

        self._gameButtons = [[tk.Button(self.root, width=2, height=1, border=3) for _ in range(self._gameWindowColumns)]
                             for _ in range(self._gameWindowRows)]

        for i in range(self._gameWindowColumns):
            for j in range(self._gameWindowRows):
                if i == 0:
                    self._gameButtons[j][i].grid(row=j + 2, column=i, padx=(50, 0))

                    self._gameButtons[j][i].bind('<Button-1>',
                                                 lambda event, p=self._gameButtons[j][i], x=j, y=i:
                                                 self.leftButton(p, x, y))

                    self._gameButtons[j][i].bind('<Button-3>',
                                                 lambda event, p=self._gameButtons[j][i]:
                                                 self.rightButton(p))
                else:
                    self._gameButtons[j][i].grid(row=j + 2, column=i)

                    self._gameButtons[j][i].bind('<Button-1>',
                                                 lambda event, p=self._gameButtons[j][i], x=j, y=i:
                                                 self.leftButton(p, x, y))

                    self._gameButtons[j][i].bind('<Button-3>',
                                                 lambda event, p=self._gameButtons[j][i]:
                                                 self.rightButton(p))

    def initGameTable(self):
        """
        Initialization of 2D list with size of game table which will be used for:
        - remember where all mines are,
        - remember how many mines are in neighbourhood of every single field.
        """

        self._gameTable = [[0 for _ in range(self._gameWindowColumns)] for _ in range(self._gameWindowRows)]

        randomFieldsForMines = self.getRandomFieldsForMines()

        for i in range(self._numberOfMines):
            y = randomFieldsForMines[i][0]
            x = randomFieldsForMines[i][1]
            self._gameTable[x][y] = -1

        self.checkNeighbours()

    def getRandomFieldsForMines(self):
        """This method draws random co-ordinates for mines."""

        tempNumberOfMines = self._numberOfMines
        tabWithRandomFieldsForMines = []

        while tempNumberOfMines:
            randXY = [rand.randint(0, self._gameWindowColumns - 1), rand.randint(0, self._gameWindowRows - 1)]
            if randXY not in tabWithRandomFieldsForMines:
                tabWithRandomFieldsForMines.append(randXY)
                tempNumberOfMines -= 1

        return tabWithRandomFieldsForMines

    def checkNeighbours(self):
        """This method checks how many mines are in neighbourhood of every single field."""

        for i in range(self._gameWindowRows):
            for j in range(self._gameWindowColumns):
                if self._gameTable[i][j] == -1:
                    self.findNeighbours(i, j)

    def findNeighbours(self, i, j):
        """This method cooperate with checkNeighbours()"""

        for k in range(j - 1, j + 2):
            if self._gameWindowColumns > k >= 0:
                for m in range(i - 1, i + 2):
                    if not (m == i and k == j):
                        if 0 <= m < self._gameWindowRows and self._gameTable[m][k] != -1:
                            self._gameTable[m][k] += 1

    def rightButton(self, button):
        """This method fulfills logic of right mouse button"""

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
        """This method controls if game can be continue if not ends it with the win or lose."""

        if self._numberOfMines == 0:
            if self._emptyFields == self.countAllLabelFields():
                self.initGameOverWindow()

    def countAllLabelFields(self):
        """This method count how many buttons are disabled"""

        counter = 0
        for i in range(self._gameWindowColumns):
            for j in range(self._gameWindowRows):
                if isinstance(self._gameButtons[j][i], tk.Label):
                    counter += 1

        return counter

    def initGameOverWindow(self, condition=True):
        """
        This method initiates window which display if player won or lost and it gives to player two options:
        - play next game,
        - close game window.
         """

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
        """This method is called if player want to close the game"""

        gameWinWindowTopLevel.destroy()
        self.root.destroy()

    def checkField(self, condition=True):
        """This method count how many mines player marked"""

        if condition:
            self._numberOfMines -= 1
        else:
            self._numberOfMines += 1

        if self._numberOfMines >= 0:
            zerosLeft = 4 - len(str(self._numberOfMines))
            self._upperPanelButtons[0]['text'] = zerosLeft * '0' + str(self._numberOfMines)

    def leftButton(self, button, i, j):
        """This method fulfills logic of left mouse button"""

        if self._gameTable[i][j] == -1:
            for i in range(self._gameWindowRows):
                for j in range(self._gameWindowColumns):
                    if self._gameTable[i][j] == -1:
                        self._gameButtons[i][j]['text'] = 'X'
            self.initGameOverWindow(False)
        else:
            self.updateButton(button, i, j)

        self.checkIfGameIsOver()

    def updateButton(self, button, i, j):
        """This method checks whether on clicked field is a number or nothing (empty field)"""

        if isinstance(button, tk.Button) and button['state'] != 'disabled':
            self.disableButton(i, j)
            if self._gameTable[i][j] > 0:
                self.displayButton(i, j)
            else:
                self.findAllZeroFieldsRecursion(i, j)

    def findAllZeroFieldsRecursion(self, i, j):
        """This method is using recursion to find all neighbours of clicked field that are not numbers."""

        for x in range(i - 1, i + 2):
            if self._gameWindowRows > x >= 0:
                for y in range(j - 1, j + 2):
                    if self._gameWindowColumns > y >= 0 and not (i == x and j == y):
                        self.updateButton(self._gameButtons[x][y], x, y)

    def displayButton(self, i, j):
        """This method is called when we clicked or findAllZeroFieldsRecursion() found field with the number."""

        if j == 0:
            self._gameButtons[i][j].grid(row=i + 2, column=j, padx=(50, 0))
        else:
            self._gameButtons[i][j].grid(row=i + 2, column=j)

    def disableButton(self, i, j):
        """This method disables clicked button and changes it to a tk.Label."""

        self._gameButtons[i][j].configure(state='disabled', border=1)
        self._gameButtons[i][j].unbind('<Button-1>')
        self._gameButtons[i][j].unbind('<Button-3>')

        number = self._gameTable[i][j]
        myFont = Font(self.root, size=10, weight=BOLD)

        if number == 1:
            self._gameButtons[i][j] = tk.Label(self.root,
                                               text=str(number),
                                               foreground='blue',
                                               font=myFont)
        elif number == 2:
            self._gameButtons[i][j] = tk.Label(self.root,
                                               text=str(number),
                                               foreground='green',
                                               font=myFont)
        elif number == 3:
            self._gameButtons[i][j] = tk.Label(self.root,
                                               text=str(number),
                                               foreground='red',
                                               font=myFont)
        elif number == 4:
            self._gameButtons[i][j] = tk.Label(self.root,
                                               text=str(number),
                                               foreground='#000066',
                                               font=myFont)
        elif number == 5:
            self._gameButtons[i][j] = tk.Label(self.root,
                                               text=str(number),
                                               foreground='#FFEBEE',
                                               font=myFont)
        elif number == 6:
            self._gameButtons[i][j] = tk.Label(self.root,
                                               text=str(number),
                                               foreground='#455A64',
                                               font=myFont)
        elif number == 7:
            self._gameButtons[i][j] = tk.Label(self.root,
                                               text=str(number),
                                               foreground='#FFD740',
                                               font=myFont)
        elif number == 8:
            self._gameButtons[i][j] = tk.Label(self.root,
                                               text=str(number),
                                               foreground='#E9C2A6',
                                               font=myFont)
        else:
            self._gameButtons[i][j] = tk.Label(self.root)

    def cheatsXYZZY(self):
        """Turns XYZZY cheats on.

        When player will press following combination "xyzzy" then fields with mines become darker.
        """

        self.root.bind('<Key>', lambda fun: self.checkIfCombinationIsCorrect(fun.char))

    def checkIfCombinationIsCorrect(self, char):
        """This method checks if player gave correct combination."""

        self._writtenCodeToCheats = char + self._writtenCodeToCheats[0:4]

        if self._writtenCodeToCheats[::-1] == self.CHEAT_CODE:
            self.makeFieldsWithMinesDarker()

    def makeFieldsWithMinesDarker(self):
        """When _writtenCodeToCheats is equal to 'xyzzy' then this method makes fields with mines darker."""

        for i in range(self._gameWindowRows):
            for j in range(self._gameWindowColumns):
                if self._gameTable[i][j] == -1:
                    self._gameButtons[i][j]['background'] = ['#A8A8A8']

    def startTimer(self, timer):
        """This method starts the timer and refreshes it every second."""

        zerosLeft = 4 - len(str(self._time))
        timer['text'] = zerosLeft * '0' + str(self._time)
        self._time += 1
        self.root.after(1000, self.startTimer, timer)

    @property
    def gameWindowColumns(self) -> int:
        return self._gameWindowColumns

    @gameWindowColumns.setter
    def gameWindowColumns(self, new):
        """Setter for _gameWindowColumn"""

        if 15 > new > 2:
            self._gameWindowColumns = new
        else:
            raise InputError

    @property
    def gameWindowRows(self) -> int:
        return self._gameWindowRows

    @gameWindowRows.setter
    def gameWindowRows(self, new):
        """Setter for _gameWindowRows"""

        if 15 > new > 2:
            self._gameWindowRows = new
        else:
            raise InputError

    @property
    def numberOfMines(self):
        return self._numberOfMines

    @numberOfMines.setter
    def numberOfMines(self, new):
        """Setter for _numberOfMines"""

        if self._gameWindowColumns * self._gameWindowRows >= new > 0:
            self._numberOfMines = new
        else:
            raise InputError

    def setEmptyFields(self):
        """This method is called when player restarted the game and it refreshes value of _emptyFields."""

        self._emptyFields = self._gameWindowRows * self._gameWindowColumns - self._numberOfMines


if __name__ == '__main__':
    gw = GameWindow()
    gw.startGame()
    gw.root.mainloop()
