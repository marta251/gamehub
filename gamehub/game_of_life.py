import curses
from curses import wrapper
import random
import time

class GameOfLife:
    def __init__(self, speed=100, mode="Automatic", density=30):
        self.speed = speed
        self.delta_time = speed / 1000
        self.mode = mode
        self.density = density
        self.matrix = None

    def initialize_matrix(self, rows : int, cols : int, density : int) -> list[list[int]]:
        matrix = [[0 for _ in range(cols)] for _ in range(rows)]
        for i in range(rows):
            for j in range(cols):
                if random.randint(0, 100) < density:
                    matrix[i][j] = 1
                else:
                    matrix[i][j] = 0
        return matrix

    def count_live_neighbors(self, matrix : list[list[int]], y : int, x : int) -> int:
        count = 0
        for i in range(y-1, y+2):
            for j in range(x-1, x+2):
                if i == y and j == x:
                    continue
                if i < 0 or j < 0 or i >= len(matrix) or j >= len(matrix[0]):
                    continue
                count += matrix[i][j]
        return count

    def update_matrix(self, matrix : list[list[int]]) -> list[list[int]]:
        new_matrix = [[0 for _ in range(len(matrix[0]))] for _ in range(len(matrix))]
        for i in range(len(matrix)):
            for j in range(len(matrix[0])):
                live_neighbors = self.count_live_neighbors(matrix, i, j)
                if matrix[i][j] == 1: # Cell is alive
                    if live_neighbors < 2 or live_neighbors > 3:
                        new_matrix[i][j] = 0 # Die (underpopulation or overpopulation)
                    elif live_neighbors == 3 or live_neighbors == 2:  # Survive
                        new_matrix[i][j] = 1
                else: # Cell is dead
                    if live_neighbors == 3: # Reproduce
                        new_matrix[i][j] = 1
        return new_matrix

    def draw_board(self, stdscr, matrix, color) -> None:
        stdscr.clear()
        for i in range(len(matrix)):
            for j in range(len(matrix[0])):
                if matrix[i][j] == 1:
                    try:
                        stdscr.addstr(i, j * 2, "  ", color)
                    except curses.error:
                        pass
        stdscr.refresh()

    def get_input_and_sleep(self, stdscr) -> str:
        try:
            last_key = stdscr.getkey()
        except:
            last_key = None

        if self.mode == "Automatic":
            time.sleep(self.delta_time)

        return last_key


    def init_curses(self, stdscr) -> None:
        curses.curs_set(0)  # Hide cursor

        if self.mode == "Automatic":
            stdscr.nodelay(True) # Non-blocking input

        # Define colors
        curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_WHITE)

        return curses.color_pair(1), curses.LINES, curses.COLS//2

    def gameloop(self, stdscr) -> None:
        COLOR_WHITE_WHITE, LINES, COLS = self.init_curses(stdscr)
        self.matrix = self.initialize_matrix(LINES, COLS, self.density)
        last_key = None
        while last_key != '\x1b':
            self.draw_board(stdscr, self.matrix, COLOR_WHITE_WHITE)
            self.matrix = self.update_matrix(self.matrix)
            last_key = self.get_input_and_sleep(stdscr)
   
    def init_game(self) -> None:
        wrapper(self.gameloop)  # Call the function via wrapper
