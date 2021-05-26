import InputError
import tkinter as tk


class GameWindow:
    """"""
    root = tk.Tk()

    def __init__(self, game_window_rows, game_window_columns, number_of_mines):
        """Game window parameters initialization."""
        if 15 <= game_window_rows or 15 <= game_window_columns or game_window_rows <= 2 or game_window_columns <= 2:
            raise InputError
        else:
            self.gameWindowRows = game_window_rows
            self.gameWindowColumns = game_window_columns

        if game_window_columns * game_window_rows > number_of_mines <= 0:
            raise InputError
        else:
            self.numberOfMines = number_of_mines

        self.time = 0

    def initUpperGamePanel(self):
        """"""
        counterOfMines = tk.Label(self.root, bg='black', fg='red', font=('Times New Roman', 20))
        counterOfMines.grid(row=0, column=0, columnspan=6, sticky=tk.W)
        self.checkedFields(counterOfMines)

        timer = tk.Label(self.root, bg='black', fg='red', font=('Times New Roman', 20))
        timer.grid(row=0, column=self.gameWindowRows - 1, columnspan=6, sticky=tk.E)
        timer['text'] = '0000'
        self.startTimer(timer)

        resetButton = tk.Button(self.root)
        resetButton.grid(row=0, column=self.gameWindowRows // 2)

        buttons = [counterOfMines, timer, resetButton]

        return buttons

    def initGameBoard(self):
        """"""
        fields = [[0] * self.gameWindowRows] * self.gameWindowColumns
        for i in range(self.gameWindowRows):
            for j in range(self.gameWindowColumns):
                if i == 0:
                    fields[j][i] = tk.Button(self.root, width=1, height=1)
                    fields[j][i].grid(row=j + 2, column=i, padx=(30, 0))
                else:
                    fields[j][i] = tk.Button(self.root, width=1, height=1)
                    fields[j][i].grid(row=j + 2, column=i)

        return fields

    def startTimer(self, timer):
        zerosLeft = 4 - len(str(self.time))
        timer['text'] = zerosLeft * '0' + str(self.time)
        self.time += 1
        self.root.after(1000, self.startTimer, timer)

    def checkedFields(self, counterOfMines):
        zerosLeft = 4 - len(str(self.numberOfMines))
        counterOfMines['text'] = zerosLeft * '0' + str(self.numberOfMines)
        self.numberOfMines -= 1


if __name__ == '__main__':
    gw = GameWindow(14, 8, 20)
    upperPanel = gw.initUpperGamePanel()
    gameBoard = gw.initGameBoard()
    gw.root.mainloop()
