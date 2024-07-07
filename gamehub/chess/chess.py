import chess_board
import curses
from curses import wrapper
from curses.textpad import rectangle
import time


class Chess: 
    def __init__(self):
        self.board = chess_board.ChessBoard( "4k3/8/8/8/8/8/8/RNBQKBNR w KQkq - 0 1")
        self.players = ["w", "b"]
        self.current_player = self.players[0]
        self.turn = 1
        self.check, self.checkmate, self.stalemate = False, False, False

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
    
    def detect_check_checkmate_stalemate(self):
        check, checkmate, stalemate = False, False, False
        matrix = self.board.matrix
        king_position = self.board.detect_king_coordinates(self.current_player)
        if matrix[king_position[1]][king_position[0]].king_under_attack(matrix):
            check = True
            all_possible_moves = self.get_all_possible_moves()
            if len(all_possible_moves) == 0:
                checkmate = True
        else:
            all_possible_moves = self.get_all_possible_moves()
            if len(all_possible_moves) == 0:
                stalemate = True

        return check, checkmate, stalemate

    def init_curses(self):
        curses.curs_set(0)  # Hide cursor
        curses.mousemask(1) # Enable mouse events

        # Define colors
        curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)
        curses.init_pair(3, curses.COLOR_RED, curses.COLOR_BLACK)
        return curses.color_pair(1), curses.color_pair(2), curses.color_pair(3)
        
    def draw_debug_messages(self, window):
                window.addstr(26, 0, "Fen: " + str(self.board.convert_board_to_fen()))
                window.addstr(27, 0, "Player to Move: " + str(self.current_player))
                window.addstr(28, 0, "Check: " + str(self.check))
                window.addstr(29, 0, "Checkmate: " + str(self.checkmate))
                window.addstr(30, 0, "Stalemate: " + str(self.stalemate))

    def draw_board(self, window, color, moves=None, moves_color=None, check_visualization=False, check_color=None, king_coordinates=None) -> None:

        char_matrix = self.board.matrix

        window.clear()
        window.attron(color)

        if check_visualization:
            king_coordinates = self.board.detect_king_coordinates(self.current_player)

        for i in range(8):
            for j in range(8):
                if moves != None and (j, i) in moves:
                    window.attroff(color)
                    window.attron(moves_color)
                    rectangle(window, i*3, j*5, i*3+2, j*5+4)
                    window.attroff(moves_color)
                    window.attron(color)
                elif check_visualization and king_coordinates != None and (j, i) == king_coordinates:
                    window.attroff(color)
                    window.attron(check_color)
                    rectangle(window, i*3, j*5, i*3+2, j*5+4)
                    window.attroff(check_color)
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

    def update_screen(self, window, color, moves=None, moves_color=None, check_visualization=False, check_color=None, king_coordinates=None, end_game=False) -> None:
        if not end_game:
            window.clear()
            self.draw_board(window, color, moves, moves_color, check_visualization, check_color, king_coordinates)
            self.draw_debug_messages(window)
            window.refresh()
        else:
            window.clear()
            if self.checkmate:
                self.draw_board(window, color, None, None, True, check_color, king_coordinates)
            elif self.stalemate:
                self.draw_board(window, color)
            if self.checkmate:
                if self.current_player == "w":
                    window.addstr(26, 0, "Checkmate. Black wins.")
                else:
                    window.addstr(26, 0, "Checkmate. White wins.")
            elif self.stalemate:
                window.addstr(26, 0, "Stalemate.")
            window.refresh()
            time.sleep(3)

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
    
    
    def gameloop(self, stdscr) -> None:

        COLOR_WHITE_BLACK, COLOR_GREEN_BLACK, COLOR_RED_BLACK = self.init_curses()
        
        self.draw_board(stdscr, COLOR_WHITE_BLACK)
        
        while not self.checkmate and not self.stalemate:
            # Selecting the piece to move
            x1, y1 = self.get_input(stdscr)
            x_start, y_start = self.from_input_to_board(x1, y1)

            # Check if the cursor is on a piece, and if it's the current player's piece
            if x_start is not None and y_start is not None and self.board.matrix[y_start][x_start] != None and self.board.matrix[y_start][x_start].color == self.current_player:
                possible = self.board.matrix[y_start][x_start].legal_moves(self.board.matrix)
                if not self.check:
                    self.update_screen(stdscr, COLOR_WHITE_BLACK, possible, COLOR_GREEN_BLACK)
                else:
                    self.update_screen(stdscr, COLOR_WHITE_BLACK, possible, COLOR_GREEN_BLACK, True, COLOR_RED_BLACK, self.board.detect_king_coordinates(self.current_player))

                # Selecting the destination
                x2, y2 = self.get_input(stdscr)
                x_end, y_end = self.from_input_to_board(x2, y2)
                if (x_end, y_end) in possible:
                    self.move_piece((x_start, y_start), (x_end, y_end))
                    self.current_player = self.players[(self.turn) % 2]
                    self.turn += 1
                    self.board.playerToMove = self.current_player
                    self.board.fullMoveCounter = self.turn
                    self.check, self.checkmate, self.stalemate = self.detect_check_checkmate_stalemate()

                    if not self.check:
                        self.update_screen(stdscr, COLOR_WHITE_BLACK)
                    else:
                        self.update_screen(stdscr, COLOR_WHITE_BLACK, None, None, True, COLOR_RED_BLACK, self.board.detect_king_coordinates(self.current_player))
                    
                else:
                    if not self.check:
                        self.update_screen(stdscr, COLOR_WHITE_BLACK)
                    else:
                        self.update_screen(stdscr, COLOR_WHITE_BLACK, None, None, True, COLOR_RED_BLACK, self.board.detect_king_coordinates(self.current_player))

        self.update_screen(stdscr, COLOR_WHITE_BLACK, None, None, True, COLOR_RED_BLACK, self.board.detect_king_coordinates(self.current_player), True)


    def init_game(self) -> None:
        wrapper(self.gameloop)  # Call the function via wrapper


    
Chess().init_game()