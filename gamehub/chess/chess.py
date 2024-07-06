import chess_board
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
                if char_matrix[i][j] != None:
                    piece_symbol = char_matrix[i][j].piece_symbol
                else:
                    piece_symbol = " "

                window.addstr(i*3 + 1, j*5 + 2, piece_symbol)

        window.attroff(color)     
        window.refresh()
    
    def get_input(self, window):
        key = window.getch()
        if key == curses.KEY_MOUSE:
            _, x, y, _, _ = curses.getmouse()
            return x, y
        else:
            return None, None
        
    def from_input_to_board(self, x, y):
        return x//5, y//3

    def move_piece(self, start : tuple[int, int], end :tuple[int, int]) -> None:
        if start[0] >= 0 and start[0] < 8 and start[1] >= 0 and start[1] < 8 and end[0] >= 0 and end[0] < 8 and end[1] >= 0 and end[1] < 8 and self.board.matrix[start[1]][start[0]] != None:
            piece_to_move = self.board.matrix[start[1]][start[0]]
            possible_moves = piece_to_move.legal_moves(self.board.matrix)
            if end in possible_moves:
                piece_to_move.position = end
                self.board.matrix[end[1]][end[0]] = self.board.matrix[start[1]][start[0]]
                self.board.matrix[start[1]][start[0]] = None
            return possible_moves


    def gameloop(self, stdscr) -> None:

        #Didn't find a way to detect mouse events in a new window. So, I'm using the stdscr window to detect mouse events.

        curses.curs_set(0)  # Hide cursor
        curses.mousemask(1) # Enable mouse events

        # Define colors
        curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)
        COLOR_WHITE_WHITE = curses.color_pair(1)
        
        stdscr.clear()
        stdscr.refresh()
        
        self.draw_board(stdscr, COLOR_WHITE_WHITE)
        
        while True:
            
            # y, x = self.get_input(stdscr)
            # if x is not None and y is not None:
            #     y_start, x_start = self.from_input_to_board(y, x)
            #     if self.board.matrix[y_start][x_start] != None:
            #         y, x = self.get_input(stdscr)
            #     if x is not None and y is not None:
            #         y_end, x_end = self.from_input_to_board(y, x)
            
            # self.move_piece((y_start, x_start), (y_end, x_end))
            # self.draw_board(stdscr, COLOR_WHITE_WHITE)


                    

            x1, y1 = self.get_input(stdscr)
            x2, y2 = self.get_input(stdscr)
            if x1 is not None and y1 is not None and x2 is not None and y2 is not None:
                x_start, y_start = self.from_input_to_board(x1, y1)
                x_end, y_end = self.from_input_to_board(x2, y2)
                possible = self.move_piece((x_start, y_start), (x_end, y_end))
                self.draw_board(stdscr, COLOR_WHITE_WHITE)
                stdscr.addstr(26, 0, "Valid Moves: " + str(possible))
                stdscr.addstr(27, 0, "Board: " + str(self.board.convert_board_to_fen()))

            stdscr.addstr(25, 0, "Cursor Input: ({},{}) ({},{})".format(x_start, y_start, x_end, y_end))
            stdscr.refresh()
            stdscr.attroff(curses.color_pair(1))

        
    def init_game(self) -> None:
        wrapper(self.gameloop)  # Call the function via wrapper


    
Chess().init_game()