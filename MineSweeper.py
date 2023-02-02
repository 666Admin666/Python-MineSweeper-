import tkinter as tk
import random

class Minesweeper:
    
    def __init__(self, rows=10, cols=10, mines=10):
        self.rows = rows
        self.cols = cols
        self.mines = mines
        self.grid = [[0] * cols for _ in range(rows)]
        self.revealed = [[False] * cols for _ in range(rows)]
        self.flags = [[False] * cols for _ in range(rows)]
        self.game_over = False

        self.window = tk.Tk()
        self.window.title("Minesweeper")
        self.restart_button = tk.Button(self.window, text="Restart", command=self.restart)
        self.restart_button.grid(row=self.rows, column=0, columnspan=self.cols)

        self.buttons = []
        for r in range(self.rows):
            button_row = []
            for c in range(self.cols):
                button = tk.Button(self.window, width=4, height=2, command=lambda r=r, c=c: self.reveal(r, c))
                button.bind("<Button-3>", lambda event, r=r, c=c: self.toggle_flag(r, c))
                button.grid(row=r, column=c)
                button_row.append(button)
            self.buttons.append(button_row)

        self.place_mines()

        


    def place_mines(self):
        mines_placed = 0
        while mines_placed < self.mines:
            r = random.randint(0, self.rows - 1)
            c = random.randint(0, self.cols - 1)
            if not self.grid[r][c]:
                self.grid[r][c] = -1
                mines_placed += 1

        for r in range(self.rows):
            for c in range(self.cols):
                if self.grid[r][c] == -1:
                    continue
                count = 0
                for dr in range(-1, 2):
                    for dc in range(-1, 2):
                        if not (0 <= r + dr < self.rows) or not (0 <= c + dc < self.cols):
                            continue
                        if self.grid[r + dr][c + dc] == -1:
                            count += 1
                self.grid[r][c] = count

    def reveal(self, r, c):
        if self.game_over:
            return
        if self.revealed[r][c]:
            return
        if self.flags[r][c]:
            return
        self.revealed[r][c] = True
        self.buttons[r][c]["text"] = str(self.grid[r][c])
        self.buttons[r][c]["state"] = "disabled"
        if self.grid[r][c] == -1:
            self.game_over = True
            self.reveal_mines()
            self.window.title("Game Over :(")
            return
        elif self.grid[r][c] == 0:
            for dr in range(-1, 2):
                for dc in range(-1, 2):
                    if not (0 <= r + dr < self.rows) or not (0 <= c + dc < self.cols):
                        continue
                    self.reveal(r + dr, c + dc)
        revealed_count = 0
        for r in range(self.rows):
            for c in range(self.cols):
                if self.revealed[r][c]:
                    revealed_count += 1
        if revealed_count == self.rows * self.cols - self.mines:
            self.window.title("You Win!")

    def reveal_mines(self):
        for r in range(self.rows):
            for c in range(self.cols):
                if self.grid[r][c] == -1:
                    self.buttons[r][c]["text"] = "X"
                    self.buttons[r][c]["state"] = "disabled"
    def toggle_flag(self, r, c):
        if self.game_over:
            return
        if self.revealed[r][c]:
            return
        self.flags[r][c] = not self.flags[r][c]
        if self.flags[r][c]:
            self.buttons[r][c]["text"] = "F"
        else:
            self.buttons[r][c]["text"] = ""
    def reset_game(self):
        self.grid = [[0] * self.cols for _ in range(self.rows)]
        self.revealed = [[False] * self.cols for _ in range(self.rows)]
        self.flags = [[False] * self.cols for _ in range(self.rows)]
        self.game_over = False
        self.place_mines()

    def reset_ui(self):
        for r in range(self.rows):
            for c in range(self.cols):
                self.buttons[r][c]["text"] = ""
                self.buttons[r][c]["state"] = "normal"

    def restart(self):
        self.reset_game()
        self.reset_ui()
        self.window.title("Minesweeper")


game = Minesweeper()
game.window.mainloop()
                   
