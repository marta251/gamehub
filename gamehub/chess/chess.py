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
    

    def gameloop(self, stdscr) -> None:
        curses.curs_set(0)  # Hide cursor

        # Define colors
        curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)
        COLOR_WHITE_WHITE = curses.color_pair(1)
        
        stdscr.clear()
        stdscr.refresh()
        
        board_window = curses.newwin(26, 44, curses.LINES//2 - 13, curses.COLS//2 - 22)
        
        self.draw_board(board_window, COLOR_WHITE_WHITE)
        
        stdscr.getch()
            
        
    def init_game(self) -> None:
        wrapper(self.gameloop)  # Call the function via wrapper


    
Chess().init_game()