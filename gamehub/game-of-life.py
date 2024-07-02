import curses
from curses import wrapper
import random
import time

def draw_board(stdscr, rows, cols):
    for i in range(rows):
        for j in range(cols):
            stdscr.addstr(i, j, ' ')

    num_zeros = (rows * cols) // 40  # Adjust the fraction to control density
    for _ in range(num_zeros):
        rand_row = random.randint(0, rows - 1)
        rand_col = random.randint(0, cols - 1)
        stdscr.addstr(rand_row, rand_col, '0')

    stdscr.refresh()

def main(stdscr):
    curses.curs_set(0)  # Hide cursor
    stdscr.nodelay(True)  # Non-blocking input

    (ROWS, COLS) = (curses.LINES - 1, curses.COLS - 1)
    key_pressed = None

    while key_pressed != 'q':
        stdscr.clear()
        draw_board(stdscr, ROWS, COLS)
        stdscr.refresh()

        try:
            key_pressed = stdscr.getkey()
        except:
            key_pressed = None
        
        time.sleep(2)

wrapper(main)