import curses
from curses import wrapper
import time
from collections import deque
import random


#TODO: Add losing conditions, score, and restart

def calcule_new_position(y, x, direction, ROWS, COLS):
    if direction == "UP":
        if y > 0:
            y -= 1
    elif direction == "DOWN":
        if y < ROWS:
            y += 1
    elif direction == "LEFT":
        if x > 1:
            x -= 2
    elif direction == "RIGHT":
        if x < COLS:
            x += 2
    return y, x

def calcule_direction(currentDirection, key):
    if key == "KEY_UP" and currentDirection != "DOWN":
        return "UP"
    elif key == "KEY_DOWN" and currentDirection != "UP":
        return "DOWN"
    elif key == "KEY_LEFT" and currentDirection != "RIGHT":
        return "LEFT"
    elif key == "KEY_RIGHT" and currentDirection != "LEFT":
        return "RIGHT"
    return currentDirection

def draw_snake(stdscr, body, color):
    for i in range(len(body)):
        (y, x) = body[i]
        stdscr.addstr(y, x, "  ", color)

def draw_food(stdscr, y, x, color):
    stdscr.addstr(y, x, "  ", color)

#TODO: Food shouldn't spawn on the snake
def new_food_coordinates(ROWS, COLS):
    y= random.randint(0, ROWS)
    x= random.randint(0, COLS)
    if x%2!=0:
        x-=1
    return y, x
    
def check_food_eaten(body, y_food, x_food):
    if body[len(body) - 1] == (y_food, x_food):
        return True
    return False

def verify_collision(body, ROWS, COLS):
    if body[len(body) - 1][0] < 0 or body[len(body) - 1][0] > ROWS:
        return True
    if body[len(body) - 1][1] < 0 or body[len(body) - 1][1] > COLS:
        return True
    for i in range(len(body) - 1):
        if body[len(body) - 1] == body[i]:
            return True
    return False


def main(stdscr):

    curses.curs_set(0)  # Hide cursor

    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_GREEN)
    COLOR_GREEN_GREEN = curses.color_pair(1)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_RED)
    COLOR_RED_RED = curses.color_pair(2)

    (ROWS, COLS) = (curses.LINES - 2, curses.COLS - 2)
    stdscr.nodelay(True)

    score = 0

    
    body = deque([(0,0)])
    y_food, x_food = new_food_coordinates(ROWS, COLS)
    direction = "RIGHT"
    last_key = "KEY_RIGHT"
    while last_key != 'q':
        stdscr.clear()

        (y, x) = calcule_new_position(body[len(body) - 1][0], body[len(body) - 1][1], direction, ROWS, COLS)
        body.append((y, x))
        if verify_collision(body, ROWS, COLS):
            stdscr.addstr(ROWS//2, COLS//2, "GAME OVER", curses.A_BLINK)
            stdscr.refresh()
            time.sleep(2)
            break
        if check_food_eaten(body, y_food, x_food):
            body.append((y, x))
            y_food, x_food = new_food_coordinates(ROWS, COLS)
            score += 1
        else:
            body.popleft()

        direction = calcule_direction(direction, last_key)

        draw_snake(stdscr, body, COLOR_GREEN_GREEN)
        draw_food(stdscr, y_food, x_food, COLOR_RED_RED)
        
        try:
            last_key = stdscr.getkey()
        except:
            last_key = None

        time.sleep(0.05)
    stdscr.refresh()


wrapper(main)  # Call the function via wrapper