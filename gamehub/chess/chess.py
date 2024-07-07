import chess_board
import curses
from curses import wrapper
from curses.textpad import rectangle


class Chess: 
    def __init__(self):
        self.board = chess_board.ChessBoard( "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")
        self.players = ["w", "b"]
        self.current_player = self.players[0]
        self.turn = 1




    def draw_board(self, window, color, moves=None, moves_color=None) -> None:

        char_matrix = self.board.matrix

        window.clear()
        window.attron(color)

        for i in range(8):
            for j in range(8):
                if moves != None and (j, i) in moves:
                    window.attroff(color)
                    window.attron(moves_color)
                    rectangle(window, i*3, j*5, i*3+2, j*5+4)
                    window.attroff(moves_color)
                    window.attron(color)
                else:
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
        if x != None and y != None and x//5 >= 0 and x//5 < 8 and y//3 >= 0 and y//3 < 8:
            return x//5, y//3
        else:
            return None, None

    def move_piece(self, start : tuple[int, int], end :tuple[int, int]) -> None:
        if start[0] >= 0 and start[0] < 8 and start[1] >= 0 and start[1] < 8 and end[0] >= 0 and end[0] < 8 and end[1] >= 0 and end[1] < 8 and self.board.matrix[start[1]][start[0]] != None:
            piece_to_move = self.board.matrix[start[1]][start[0]]
            possible_moves = piece_to_move.legal_moves(self.board.matrix)
            if end in possible_moves:
                piece_to_move.position = end
                self.board.matrix[end[1]][end[0]] = self.board.matrix[start[1]][start[0]]
                self.board.matrix[start[1]][start[0]] = None
            
    def get_all_possible_moves(self):
        all_possible_moves = []
        for i in range(8):
            for j in range(8):
                if self.board.matrix[i][j] != None and self.board.matrix[i][j].color == self.current_player:
                    all_possible_moves = all_possible_moves + self.board.matrix[i][j].legal_moves(self.board.matrix)
        return all_possible_moves
    
    def detect_check_and_checkmate(self):
        check, checkmate = False, False
        matrix = self.board.matrix
        for i in range(8):
            for j in range(8):
                if matrix[i][j]!=None and matrix[i][j].piece_char == 'K' and self.current_player == 'w':
                    king_position = (j, i)
                if matrix[i][j]!=None and matrix[i][j].piece_char == 'k' and self.current_player == 'b':
                    king_position = (j, i)
        if matrix[king_position[1]][king_position[0]].king_under_attack(matrix):
            check = True
            all_possible_moves = self.get_all_possible_moves()
            if len(all_possible_moves) == 0:
                checkmate = True
        return check, checkmate


        

    def gameloop(self, stdscr) -> None:

        #Didn't find a way to detect mouse events in a new window. So, I'm using the stdscr window to detect mouse events.

        curses.curs_set(0)  # Hide cursor
        curses.mousemask(1) # Enable mouse events

        # Define colors
        curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)
        COLOR_WHITE_BLACK = curses.color_pair(1)
        COLOR_GREEN_BLACK = curses.color_pair(2)
        
        stdscr.clear()
        stdscr.refresh()
        
        self.draw_board(stdscr, COLOR_WHITE_BLACK)
        
        # while True:    
        #     x1, y1 = self.get_input(stdscr)
        #     x2, y2 = self.get_input(stdscr)
        #     if x1 is not None and y1 is not None and x2 is not None and y2 is not None:
        #         x_start, y_start = self.from_input_to_board(x1, y1)
        #         x_end, y_end = self.from_input_to_board(x2, y2)
        #         possible = self.move_piece((x_start, y_start), (x_end, y_end))
        #         self.draw_board(stdscr, COLOR_WHITE_BLACK)
        #         stdscr.addstr(26, 0, "Valid Moves: " + str(possible))
        #         stdscr.addstr(27, 0, "Board: " + str(self.board.convert_board_to_fen()))

        #     stdscr.addstr(25, 0, "Cursor Input: ({},{}) ({},{})".format(x_start, y_start, x_end, y_end))
        #     stdscr.refresh()
        #     stdscr.attroff(curses.color_pair(1))

        while True:
            # Selecting the piece to move
            x1, y1 = self.get_input(stdscr)
            x_start, y_start = self.from_input_to_board(x1, y1)
            # Check if the cursor is on a piece, and if it's the current player's piece
            if x_start is not None and y_start is not None and self.board.matrix[y_start][x_start] != None and self.board.matrix[y_start][x_start].color == self.current_player:
                possible = self.board.matrix[y_start][x_start].legal_moves(self.board.matrix)
                stdscr.clear()
                self.draw_board(stdscr, COLOR_WHITE_BLACK, possible, COLOR_GREEN_BLACK)
                stdscr.addstr(25, 0, "Cursor Input: ({},{})".format(x_start, y_start))
                stdscr.addstr(26, 0, "Player to Move: " + str(self.current_player))
                stdscr.addstr(27, 0, "Valid Moves: " + str(possible))
                stdscr.addstr(28, 0, "Board: " + str(self.board.convert_board_to_fen()))
                stdscr.addstr(29, 0, "Check: " + str(self.detect_check_and_checkmate()[0]))
                stdscr.addstr(30, 0, "Checkmate: " + str(self.detect_check_and_checkmate()[1]))
                stdscr.addstr(31, 0, "All Possible Moves: " + str(self.get_all_possible_moves()[:10]))
                stdscr.refresh()

                # Selecting the destination
                x2, y2 = self.get_input(stdscr)
                x_end, y_end = self.from_input_to_board(x2, y2)
                if (x_end, y_end) in possible:
                    self.move_piece((x_start, y_start), (x_end, y_end))
                    self.current_player = self.players[(self.turn) % 2]
                    self.turn += 1
                    self.board.playerToMove = self.current_player
                    self.board.fullMoveCounter = self.turn
                    self.draw_board(stdscr, COLOR_WHITE_BLACK)
                    stdscr.addstr(25, 0, "Last Move: ({},{}) ({},{}) : Valid".format(x_start, y_start, x_end, y_end))
                    stdscr.addstr(26, 0, "Player to Move: " + str(self.current_player))
                    stdscr.addstr(28, 0, "Board: " + str(self.board.convert_board_to_fen()))
                    
                    stdscr.refresh()
                    
                else:
                    self.draw_board(stdscr, COLOR_WHITE_BLACK)
                    stdscr.addstr(25, 0, "Last Move: ({},{}) ({},{}) : Invalid".format(x_start, y_start, x_end, y_end))
                    stdscr.addstr(26, 0, "Player to Move: " + str(self.current_player))
                    stdscr.addstr(28, 0, "Board: " + str(self.board.convert_board_to_fen()))
                    stdscr.refresh()

        
    def init_game(self) -> None:
        wrapper(self.gameloop)  # Call the function via wrapper


    
Chess().init_game()