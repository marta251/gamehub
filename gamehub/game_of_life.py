import curses
from curses import wrapper
import random

class GameOfLife:
    def __init__(self):
        pass

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
        for i in range(len(matrix)):
            for j in range(len(matrix[0])):
                live_neighbors = self.count_live_neighbors(matrix, i, j)

                if matrix[i][j] == 1: # Cell is alive
                    if live_neighbors < 2 or live_neighbors > 3: # Die because of underpopulation or overpopulation
                        matrix[i][j] = 0
                    elif live_neighbors == 3 or live_neighbors == 2:  # Survive
                        matrix[i][j] = 1
                else:         # Cell is dead
                    if live_neighbors == 3: # Reproduce
                        matrix[i][j] = 1    
        return matrix

    #def draw_board(stdscr, rows, cols) -> None:
    '''
    def main(stdscr) -> None:
        curses.curs_set(0)  # Hide cursor

        (ROWS, COLS) = (curses.LINES - 1, curses.COLS - 1)

        while True:
            stdscr.clear()
            draw_board(stdscr, ROWS, COLS)
            stdscr.refresh()
            
            if stdscr.getkey() == 'q': # Exit the game when 'q' is pressed
                break
            else:
                update_board(stdscr, ROWS, COLS)
    '''

