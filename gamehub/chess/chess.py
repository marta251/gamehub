from gamehub.chess.chess_board import ChessBoard
import curses
from curses import wrapper
from curses.textpad import rectangle
import time
from gamehub.chess.chess_engine import ChessEngine

class Chess: 
    def __init__(self, mode : str = "Multiplayer", fen : str = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w - - 0 1"): # Castling disabled by default (when implemented, change to "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")
        self.mode = mode
        self.board = ChessBoard(fen) 
        self.players = ["w", "b"]
        if self.board.playerToMove == "w":
            self.current_player = self.players[0]
        else:
            self.current_player = self.players[1]
        self.turn = self.board.fullMoveCounter
        self.check, self.checkmate, self.stalemate = self.detect_check_checkmate_stalemate()

    def move_piece(self, start : tuple[int, int], end :tuple[int, int]) -> None:
        piece_to_move = self.board.matrix[start[1]][start[0]]
        piece_to_move.position = end
        self.board.matrix[end[1]][end[0]] = self.board.matrix[start[1]][start[0]]
        self.board.matrix[start[1]][start[0]] = None
        self.current_player = self.players[(self.turn) % 2]
        self.turn += 1
        self.board.playerToMove = self.current_player
        self.board.fullMoveCounter = self.turn
            
    def get_all_possible_moves_count(self):
        all_possible_moves_count = 0
        for i in range(8):
            for j in range(8):
                if self.board.matrix[i][j] != None and self.board.matrix[i][j].color == self.current_player:
                    all_possible_moves_count = all_possible_moves_count + len(self.board.matrix[i][j].legal_moves(self.board.matrix))
        return all_possible_moves_count
    
    def detect_check_checkmate_stalemate(self):
        check, checkmate, stalemate = False, False, False
        matrix = self.board.matrix
        king_position = self.board.detect_king_coordinates(self.current_player)
        if matrix[king_position[1]][king_position[0]].king_under_attack(matrix):
            check = True
            if self.get_all_possible_moves_count() == 0:
                checkmate = True
        else:
            if self.get_all_possible_moves_count() == 0:
                stalemate = True

        return check, checkmate, stalemate

    def init_curses(self):
        curses.curs_set(0)  # Hide cursor
        curses.mousemask(1) # Enable mouse events

        curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)
        curses.init_pair(3, curses.COLOR_RED, curses.COLOR_BLACK)
        return curses.color_pair(1), curses.color_pair(2), curses.color_pair(3)
        
    def draw_debug_messages(self, window):
                window.addstr(26, 0, "Fen: " + str(self.board.convert_board_to_fen()))
                if self.current_player == "w":
                    window.addstr(27, 0, "Player to Move: White")
                else:
                    window.addstr(27, 0, "Player to Move: Black")
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
            return x, y, None
        elif key == 27:
            return None, None, True
        else:
            return None, None, False
        
    def check_terminal_size(self, min_lines : int, min_cols : int, window : object) -> bool:
        if curses.COLS < min_cols or curses.LINES < min_lines:
            window.addstr(0, 0, "Resize the terminal (" + str(min_cols) + "x" + str(min_lines) + ")", curses.A_BOLD)
            window.refresh()
            time.sleep(2)
            return False
        return True
        
    def from_input_to_board(self, x, y):
        if x != None and y != None and x//5 >= 0 and x//5 < 8 and y//3 >= 0 and y//3 < 8:
            return x//5, y//3
        else:
            return None, None
    
    def multiplayer_gameloop(self, stdscr) -> None:
        COLOR_WHITE_BLACK, COLOR_GREEN_BLACK, COLOR_RED_BLACK = self.init_curses()
        
        if not self.check_terminal_size(35, 40, stdscr):
            return

        self.update_screen(stdscr, COLOR_WHITE_BLACK)
        
        while not self.checkmate and not self.stalemate:
            # Selecting the piece to move
            x1, y1, exit = self.get_input(stdscr)
            if exit:
                break
            x_start, y_start = self.from_input_to_board(x1, y1)
                
            # Check if the cursor is on a piece, and if it's the current player's piece
            if x_start is not None and y_start is not None and self.board.matrix[y_start][x_start] != None and self.board.matrix[y_start][x_start].color == self.current_player:
                possible = self.board.matrix[y_start][x_start].legal_moves(self.board.matrix)
                if not self.check:
                    self.update_screen(stdscr, COLOR_WHITE_BLACK, possible, COLOR_GREEN_BLACK)
                else:
                    self.update_screen(stdscr, COLOR_WHITE_BLACK, possible, COLOR_GREEN_BLACK, True, COLOR_RED_BLACK, self.board.detect_king_coordinates(self.current_player))

                # Selecting the destination
                x2, y2, exit = self.get_input(stdscr)
                if exit:
                    break
                x_end, y_end = self.from_input_to_board(x2, y2)
                if (x_end, y_end) in possible:
                    self.move_piece((x_start, y_start), (x_end, y_end))
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

        if self.checkmate or self.stalemate:
            self.update_screen(stdscr, COLOR_WHITE_BLACK, None, None, True, COLOR_RED_BLACK, self.board.detect_king_coordinates(self.current_player), True)

    def single_player_gameloop(self, stdscr) -> None:
        COLOR_WHITE_BLACK, COLOR_GREEN_BLACK, COLOR_RED_BLACK = self.init_curses()
        
        if not self.check_terminal_size(35, 40, stdscr):
            return

        self.update_screen(stdscr, COLOR_WHITE_BLACK)

        engine = ChessEngine()

        while not self.checkmate and not self.stalemate:
            # Selecting the piece to move
            if self.current_player == "w":
                x1, y1, exit = self.get_input(stdscr)
                if exit:
                    break
                x_start, y_start = self.from_input_to_board(x1, y1)
            else:
                x_start, y_start, x_end, y_end = engine.get_move(self.board.convert_board_to_fen())                  

            # Check if the cursor is on a piece, and if it's the current player's piece
            if x_start is not None and y_start is not None and self.board.matrix[y_start][x_start] != None and self.board.matrix[y_start][x_start].color == self.current_player:
                possible = self.board.matrix[y_start][x_start].legal_moves(self.board.matrix)
                if not self.check and self.current_player == "w":
                    self.update_screen(stdscr, COLOR_WHITE_BLACK, possible, COLOR_GREEN_BLACK)
                elif self.current_player == "w":
                    self.update_screen(stdscr, COLOR_WHITE_BLACK, possible, COLOR_GREEN_BLACK, True, COLOR_RED_BLACK, self.board.detect_king_coordinates(self.current_player))

                # Selecting the destination
                if self.current_player == "w":
                    x2, y2, exit = self.get_input(stdscr)
                    if exit:
                        break
                    x_end, y_end = self.from_input_to_board(x2, y2)
                if (x_end, y_end) in possible:
                    self.move_piece((x_start, y_start), (x_end, y_end))
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

        if self.checkmate or self.stalemate:
            self.update_screen(stdscr, COLOR_WHITE_BLACK, None, None, True, COLOR_RED_BLACK, self.board.detect_king_coordinates(self.current_player), True)

        engine.close()

    def init_game(self) -> None:
        if self.mode == "Singleplayer":
            wrapper(self.single_player_gameloop)
        elif self.mode == "Multiplayer":
            wrapper(self.multiplayer_gameloop)