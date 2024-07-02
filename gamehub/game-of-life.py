import curses
from curses import wrapper
import random

def draw_board(stdscr, rows, cols) -> None:
    for i in range(rows):
        for j in range(cols):
            stdscr.addstr(i, j, ' ')

    num_zeros = (rows * cols) // 40  # Adjust the fraction to control density
    for _ in range(num_zeros):
        rand_row = random.randint(0, rows - 1)
        rand_col = random.randint(0, cols - 1)
        stdscr.addstr(rand_row, rand_col, '0')

    stdscr.refresh()


# TODO: Check the validity of the ranges for y and x

def count_live_neighbors(stdscr, y, x) -> int:
    count = 0
    if stdscr.inch(y-1, x) == '0':
        count += 1
    if stdscr.inch(y, x-1) == '0':
        count += 1
    if stdscr.inch(y, x+1) == '0':
        count += 1
    if stdscr.inch(y+1, x) == '0':
        count += 1

    return count

def update_board(stdscr, rows, cols) -> None:
    for y in range(rows):
        for x in range(cols):
            live_neighbors = count_live_neighbors(stdscr, y, x)

            if stdscr.inch(y, x) == '0':
                if live_neighbors < 2 or live_neighbors > 3:
                    stdscr.addstr(y, x, ' ') # Die because of underpopulation
                elif live_neighbors == 3 or live_neighbors == 2:
                    stdscr.addstr(y, x, '0') # Survive
            else:
                if live_neighbors == 3:
                    stdscr.addstr(y, x, '0') # Reproduce
    stdscr.refresh()

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

wrapper(main)