import curses
from curses import wrapper
import time
from collections import deque
import random

#TODO: Add score, restart and difficulty

class Snake:

    def __init__(self) -> None:
        pass

    def calcule_new_position(self, y, x, direction, ROWS, COLS) -> tuple:
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

    def calcule_direction(self, current_direction, key) -> str:
        if key == "KEY_UP" and current_direction != "DOWN":
            return "UP"
        elif key == "KEY_DOWN" and current_direction != "UP":
            return "DOWN"
        elif key == "KEY_LEFT" and current_direction != "RIGHT":
            return "LEFT"
        elif key == "KEY_RIGHT" and current_direction != "LEFT":
            return "RIGHT"
        return current_direction

    def draw_snake(self, window, body, color) -> None:
        for i in range(len(body)):
            (y, x) = body[i]
            window.addstr(y, x, "  ", color)

    def draw_food(self, window, y, x, color) -> None:
        window.addstr(y, x, "  ", color)

    def draw_game_over(self, window, ROWS, COLS, score) -> None:
        window.addstr(ROWS//2, COLS//2, "GAME OVER", curses.A_BOLD)
        window.addstr(ROWS//2 + 1, COLS//2, "SCORE: " + str(score), curses.A_BLINK)
        window.addstr(ROWS//2 + 2, COLS//2, "Press enter to play again...", curses.A_BLINK)
        window.refresh()
        time.sleep(1)

    def new_food_coordinates(self, ROWS, COLS, body) -> tuple:
        y= random.randint(0, ROWS)
        x= random.randint(0, COLS)
        if x%2!=0:
            x-=1
        while (y,x) in body:
            y= random.randint(0, ROWS)
            x= random.randint(0, COLS)
            if x%2!=0:
                x-=1
        return y, x
        
    def check_food_eaten(self, body, y_food, x_food) -> bool:
        if body[len(body) - 1] == (y_food, x_food):
            return True
        return False

    def verify_collision(self, body) -> bool:

        for i in range(len(body) - 1):
            if body[len(body) - 1] == body[i]:
                return True
        return False


    def gameloop(self, stdscr) -> None:

        curses.curs_set(0)  # Hide cursor
        stdscr.nodelay(True) # Non-blocking input

        # Define colors
        curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_GREEN)
        COLOR_GREEN_GREEN = curses.color_pair(1)
        curses.init_pair(2, curses.COLOR_RED, curses.COLOR_RED)
        COLOR_RED_RED = curses.color_pair(2)


        (ROWS, COLS) = (curses.LINES - 2, curses.COLS - 2)

        score = 0
        # Initial snake
        body = deque([(0,0)])
        direction = "RIGHT"
        last_key = "KEY_RIGHT"

        y_food, x_food = self.new_food_coordinates(ROWS, COLS, body)
        while last_key != 'q':
            stdscr.clear()

            (y, x) = self.calcule_new_position(body[len(body) - 1][0], body[len(body) - 1][1], direction, ROWS, COLS)
            body.append((y, x))
            if self.verify_collision(body):
                self.draw_game_over(stdscr, ROWS, COLS, score)
                break
            if self.check_food_eaten(body, y_food, x_food):
                body.append((y, x))
                y_food, x_food = self.new_food_coordinates(ROWS, COLS, body)
                score += 1
            else:
                body.popleft()

            direction = self.calcule_direction(direction, last_key)

            self.draw_snake(stdscr, body, COLOR_GREEN_GREEN)
            self.draw_food(stdscr, y_food, x_food, COLOR_RED_RED)
            stdscr.refresh()
            
            try:
                last_key = stdscr.getkey()
            except:
                last_key = None

            time.sleep(0.05)
        stdscr.refresh()

    def init_game(self) -> None:
        wrapper(self.gameloop)  # Call the function via wrapper