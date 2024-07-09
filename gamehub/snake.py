import curses
from curses import wrapper
import time
from collections import deque
import random

class Snake:
    def __init__(self, difficulty="Medium") -> None:
        self.delta_time = None
        if difficulty == "Easy":
            self.delta_time = 0.1
        elif difficulty == "Medium":
            self.delta_time = 0.05
        else:
            self.delta_time = 0.025

    def calcule_new_position(self, y : int, x : int, direction : str, SNAKE_BOUNDS : tuple[int, int, int, int]) -> tuple[int, int]:
        if direction == "UP":
            if y > SNAKE_BOUNDS[0]:
                y -= 1
        elif direction == "DOWN":
            if y < SNAKE_BOUNDS[1]:
                y += 1
        elif direction == "LEFT":
            if x > SNAKE_BOUNDS[2]:
                x -= 2
        elif direction == "RIGHT":
            if x < SNAKE_BOUNDS[3]:
                x += 2
        return y, x

    def calcule_direction(self, current_direction : str, key : str) -> str:
        if key == "KEY_UP" and current_direction != "DOWN":
            return "UP"
        elif key == "KEY_DOWN" and current_direction != "UP":
            return "DOWN"
        elif key == "KEY_LEFT" and current_direction != "RIGHT":
            return "LEFT"
        elif key == "KEY_RIGHT" and current_direction != "LEFT":
            return "RIGHT"
        return current_direction

    def draw_snake(self, window, body : deque[tuple[int, int]], color : int) -> None:
        for i in range(len(body)):
            (y, x) = body[i]
            window.addstr(y, x, "  ", color)

    def draw_food(self, window, y : int, x : int, color : int) -> None:
        window.addstr(y, x, "  ", color)

    def draw_thick_border(self, window, ROWS : int, COLS : int, color : int) -> None:
        for i in range(ROWS - 1):
            window.addstr(i, 1, " ", color)
            window.addstr(i, COLS - 2, " ", color)
        

    def draw_game_over(self, window, ROWS : int, COLS : int, score : int) -> None:
        window.addstr(ROWS//2, COLS//2, "GAME OVER", curses.A_BOLD)
        window.addstr(ROWS//2 + 1, COLS//2, "SCORE: " + str(score), curses.A_BLINK)
        window.addstr(ROWS//2 + 2, COLS//2, "Press enter to play again...", curses.A_BLINK)
        window.refresh()
        time.sleep(3)

    def new_food_coordinates(self, body : deque[tuple[int, int]], SNAKE_BOUNDS : int) -> tuple:
        y= random.randint(SNAKE_BOUNDS[0], SNAKE_BOUNDS[1])
        x= random.randint(SNAKE_BOUNDS[2], SNAKE_BOUNDS[3])
        if x%2!=0:
            x-=1
        while (y,x) in body:
            y= random.randint(SNAKE_BOUNDS[0], SNAKE_BOUNDS[1])
            x= random.randint(SNAKE_BOUNDS[2], SNAKE_BOUNDS[3])
            if x%2!=0:
                x-=1
        return y, x
        
    def check_food_eaten(self, body : deque[tuple[int, int]], y_food : int, x_food : int) -> bool:
        if body[len(body) - 1] == (y_food, x_food):
            return True
        return False

    def verify_collision(self, body : deque[tuple[int, int]]) -> bool:

        for i in range(len(body) - 1):
            if body[len(body) - 1] == body[i]:
                return True
        return False
    
    def check_terminal_size(self, min_lines : int, min_cols : int, window : object) -> bool:
        if curses.COLS < min_cols or curses.LINES < min_lines:
            window.addstr(0, 0, "Resize the terminal (" + str(min_cols) + "x" + str(min_lines) + ")", curses.A_BOLD)
            window.refresh()
            time.sleep(2)
            return False
        return True


    def gameloop(self, stdscr) -> None:

        curses.curs_set(0)  # Hide cursor
        stdscr.nodelay(True) # Non-blocking input

        # Define colors
        curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_GREEN)
        COLOR_GREEN_GREEN = curses.color_pair(1)
        curses.init_pair(2, curses.COLOR_RED, curses.COLOR_RED)
        COLOR_RED_RED = curses.color_pair(2)
        curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_WHITE)
        COLOR_WHITE_WHITE = curses.color_pair(3)

        if not self.check_terminal_size(15, 40, stdscr):
            return

        LINES_MAIN_WINDOW = curses.LINES - 6
        if curses.COLS % 2 == 0:
            COLS_MAIN_WINDOW = curses.COLS - 10
        else:
            COLS_MAIN_WINDOW = curses.COLS - 11

        SNAKE_BOUNDS = (1, LINES_MAIN_WINDOW - 2, 2, COLS_MAIN_WINDOW - 4) # (y1,y2,x1,x2) : snake can't get out of this bounds (but it can walk over this bounds)

        main_window = curses.newwin(LINES_MAIN_WINDOW, COLS_MAIN_WINDOW, 3, 5)
        score_window = curses.newwin(1, 12, 1, curses.COLS - 20)

        score = 0
        # Initial snake
        body = deque([(2,4)])
        direction = "RIGHT"
        last_key = "KEY_RIGHT"

        y_food, x_food = self.new_food_coordinates(body, SNAKE_BOUNDS)
        while last_key != '\x1b':
            main_window.clear()

            (y, x) = self.calcule_new_position(body[len(body) - 1][0], body[len(body) - 1][1], direction, SNAKE_BOUNDS)
            body.append((y, x))
            if self.verify_collision(body):
                self.draw_game_over(main_window, LINES_MAIN_WINDOW, COLS_MAIN_WINDOW, score)
                break
            if self.check_food_eaten(body, y_food, x_food):
                body.append((y, x))
                y_food, x_food = self.new_food_coordinates(body, SNAKE_BOUNDS)
                score += 1
            else:
                body.popleft()

            direction = self.calcule_direction(direction, last_key)

            main_window.border(COLOR_WHITE_WHITE, COLOR_WHITE_WHITE, COLOR_WHITE_WHITE, COLOR_WHITE_WHITE, COLOR_WHITE_WHITE, COLOR_WHITE_WHITE, COLOR_WHITE_WHITE, COLOR_WHITE_WHITE)
            self.draw_thick_border(main_window, LINES_MAIN_WINDOW, COLS_MAIN_WINDOW, COLOR_WHITE_WHITE)
            self.draw_snake(main_window, body, COLOR_GREEN_GREEN)
            self.draw_food(main_window, y_food, x_food, COLOR_RED_RED)
            main_window.refresh()

            score_window.addstr(0, 0, "SCORE: " + str(score))
            score_window.refresh()
            
            try:
                last_key = stdscr.getkey()
            except:
                last_key = None

            time.sleep(self.delta_time)

    def init_game(self) -> None:
        wrapper(self.gameloop)  # Call the function via wrapper