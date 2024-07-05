import chess_board
import chess_piece
import curses
from curses import wrapper
from curses.textpad import rectangle


class Chess: 
    def __init__(self):
        self.board = chess_board.ChessBoard( "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")
        self.players = ["w", "b"]
        self.current_player = self.players[0]
        self.turn = 0


    def draw_board(self, window, color):

        char_matrix = self.board.matrix

        window.clear()
        window.attron(color)

        for i in range(8):
            for j in range(8):
                rectangle(window, i*3, j*5, i*3+2, j*5+4)
                if char_matrix[i][j] == "P":
                    piece_char = "♟"
                elif char_matrix[i][j] == "R":
                    piece_char = "♜"
                elif char_matrix[i][j] == "N":
                    piece_char = "♞"
                elif char_matrix[i][j] == "B":
                    piece_char = "♝"
                elif char_matrix[i][j] == "Q":
                    piece_char = "♛"
                elif char_matrix[i][j] == "K":
                    piece_char = "♚"
                elif char_matrix[i][j] == "p":
                    piece_char = "♙"
                elif char_matrix[i][j] == "r":
                    piece_char = "♖"
                elif char_matrix[i][j] == "n":
                    piece_char = "♘"
                elif char_matrix[i][j] == "b":
                    piece_char = "♗"
                elif char_matrix[i][j] == "q":
                    piece_char = "♕"
                elif char_matrix[i][j] == "k":
                    piece_char = "♔"
                else:
                    piece_char = " "

                window.addstr(i*3 + 1, j*5 + 2, piece_char)

        window.attroff(color)     
        window.refresh()
    
    def get_input(self, window):
        key = window.getch()
        if key == curses.KEY_MOUSE:
            _, x, y, _, _ = curses.getmouse()
            return y, x
        else:
            return None, None
        
    def from_input_to_board(self, y, x):
        return y//3, x//5


    def gameloop(self, stdscr) -> None:

        #Didn't find a way to detect mouse events in a new window. So, I'm using the stdscr window to detect mouse events.

        curses.curs_set(0)  # Hide cursor
        curses.mousemask(1) # Enable mouse events

        # Define colors
        curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)
        COLOR_WHITE_WHITE = curses.color_pair(1)
        
        stdscr.clear()
        stdscr.refresh()
        
        debug_window = curses.newwin(1, 30, 0, 0)
        
        self.draw_board(stdscr, COLOR_WHITE_WHITE)
        
        while True:
            debug_window.attron(curses.color_pair(1))
            debug_window.clear()
            y, x = self.get_input(stdscr)
            if x is not None and y is not None:
                y, x = self.from_input_to_board(y, x)
            debug_window.addstr(0, 0, "({},{})".format(y, x))
            debug_window.refresh()
            debug_window.attroff(curses.color_pair(1))
            
            
        
    def init_game(self) -> None:
        wrapper(self.gameloop)  # Call the function via wrapper


    
Chess().init_game()