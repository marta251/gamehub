import curses
from curses import wrapper
import time
from collections import deque
import random

class Snake:
    def __init__(self, difficulty="Medium") -> None:
        self.delta_time = None
        self.difficulty = difficulty
        if self.difficulty == "Easy":
            self.delta_time = 0.1
        elif self.difficulty == "Medium":
            self.delta_time = 0.05
        else:
            self.delta_time = 0.025

        self.score = 0
        self.highscore = self.get_highscore()

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
        

    def draw_game_over(self, window, ROWS : int, COLS : int) -> None:
        window.addstr(ROWS//2 - 3, COLS//2 - 10, "GAME OVER", curses.A_BOLD)
        window.addstr(ROWS//2 - 2, COLS//2 - 10, "SCORE: " + str(self.score), curses.A_BOLD)
        window.addstr(ROWS//2 - 1, COLS//2 - 10, "HIGHSCORE: " + str(self.get_highscore()), curses.A_BOLD)
        window.addstr(ROWS//2, COLS//2 - 10, "Press enter to play again...", curses.A_BLINK)
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
    
    def get_highscore(self) -> int:
        try:
            with open("/home/gamehub/files/snake_highscore.txt", "r") as file:
                return int(file.read())
        except:
            return 0
        
    def set_highscore(self) -> None:
        if self.score > self.highscore:
            with open("/home/gamehub/files/snake_highscore.txt", "w") as file:
                file.write(str(self.score))
            self.highscore = self.score
    
    def check_terminal_size(self, min_lines : int, min_cols : int, window : object) -> bool:
        if curses.COLS < min_cols or curses.LINES < min_lines:
            window.addstr(0, 0, "Resize the terminal (" + str(min_cols) + "x" + str(min_lines) + ")", curses.A_BOLD)
            window.refresh()
            time.sleep(2)
            return False
        return True

    def set_up_curses(self, stdscr) -> None:

        curses.curs_set(0)  # Hide cursor
        stdscr.nodelay(True) # Non-blocking input

        # Define colors
        curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_GREEN)
        curses.init_pair(2, curses.COLOR_RED, curses.COLOR_RED)
        curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_WHITE)

        LINES_MAIN_WINDOW = curses.LINES - 6
        if curses.COLS % 2 == 0:
            COLS_MAIN_WINDOW = curses.COLS - 10
        else:
            COLS_MAIN_WINDOW = curses.COLS - 11

        main_window = curses.newwin(LINES_MAIN_WINDOW, COLS_MAIN_WINDOW, 3, 5)
        score_window = curses.newwin(2, 12, 1, curses.COLS - 20)


        return curses.color_pair(1), curses.color_pair(2), curses.color_pair(3), LINES_MAIN_WINDOW, COLS_MAIN_WINDOW, main_window, score_window

    def update_main_window(self, main_window, color_border, color_snake, color_food, LINES_MAIN_WINDOW, COLS_MAIN_WINDOW, body, x_food, y_food, game_over=False) -> None:
        main_window.clear()
        main_window.border(color_border, color_border, color_border, color_border, color_border, color_border, color_border, color_border)
        self.draw_thick_border(main_window, LINES_MAIN_WINDOW, COLS_MAIN_WINDOW, color_border)
        self.draw_snake(main_window, body, color_snake)
        self.draw_food(main_window, y_food, x_food, color_food)
        if game_over:
            self.draw_game_over(main_window, LINES_MAIN_WINDOW, COLS_MAIN_WINDOW)
        main_window.refresh()
    
    def update_score_window(self, score_window) -> None:
        score_window.clear()
        score_window.addstr(0, 0, "Score: " + str(self.score))
        score_window.addstr(1, 0, "Best: " + str(self.highscore))
        score_window.refresh()

    def get_input_and_delay(self, stdscr) -> str:
        try:
            key = stdscr.getkey()
        except:
            key = None
        time.sleep(self.delta_time)
        return key


    def gameloop(self, stdscr) -> None:

        if not self.check_terminal_size(15, 40, stdscr):
            return

        COLOR_GREEN_GREEN, COLOR_RED_RED, COLOR_WHITE_WHITE, LINES_MAIN_WINDOW, COLS_MAIN_WINDOW, main_window, score_window = self.set_up_curses(stdscr)

        SNAKE_BOUNDS = (1, LINES_MAIN_WINDOW - 2, 2, COLS_MAIN_WINDOW - 4) # (y1,y2,x1,x2) : snake can't get out of this bounds (but it can walk over this bounds)

        # Initial snake
        body = deque([(2,4)])
        direction = "RIGHT"
        last_key = "KEY_RIGHT"

        y_food, x_food = self.new_food_coordinates(body, SNAKE_BOUNDS)
        self.update_score_window(score_window)   
        while last_key != '\x1b':

            (y, x) = self.calcule_new_position(body[len(body) - 1][0], body[len(body) - 1][1], direction, SNAKE_BOUNDS)
            body.append((y, x))
            if self.verify_collision(body):
                self.set_highscore()
                self.update_main_window(main_window, COLOR_WHITE_WHITE, COLOR_GREEN_GREEN, COLOR_RED_RED, LINES_MAIN_WINDOW, COLS_MAIN_WINDOW, body, x_food, y_food, True)
                break
            if self.check_food_eaten(body, y_food, x_food):
                body.append((y, x))
                y_food, x_food = self.new_food_coordinates(body, SNAKE_BOUNDS)
                self.score += 1
                self.update_score_window(score_window)
            else:
                body.popleft()

            direction = self.calcule_direction(direction, last_key)

            self.update_main_window(main_window, COLOR_WHITE_WHITE, COLOR_GREEN_GREEN, COLOR_RED_RED, LINES_MAIN_WINDOW, COLS_MAIN_WINDOW, body, x_food, y_food)

            last_key = self.get_input_and_delay(stdscr)   

    def init_game(self) -> None:
        wrapper(self.gameloop)  # Call the function via wrapper