from gamehub.chess.chess import Chess
from gamehub.chess.chess_engine import ChessEngine
import pytest

class TestChess:
    def test_constructor(self):
        pass

    @pytest.mark.parametrize("starting_fen, start, end, expected", [
        ("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1", (4, 6), (4, 4), "rnbqkbnr/pppppppp/8/8/4P3/8/PPPP1PPP/RNBQKBNR b KQkq - 0 2"),    # e4
        ("8/5b2/8/P5kp/1P3pp1/3R4/2K5/8 b - - 0 32", (7, 3), (7, 4), "8/5b2/8/P5k1/1P3ppp/3R4/2K5/8 w - - 0 33")
    ])
    def test_move_piece(self, starting_fen : str, start : tuple[int, int], end : tuple[int, int], expected : str) -> None:
        c = Chess(fen=starting_fen)
        c.move_piece(start, end)
        assert c.board.convert_board_to_fen() == expected

    @pytest.mark.parametrize("fen, expected", [
        ("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1", (False, False, False)),    # Starting position
        ("8/5p2/p4K2/3pp3/8/1P3q2/1kr2R2/8 w - - 0 43", (True, False, False)),                  # Check
        ("8/8/4k3/8/8/8/2q5/K7 w - - 0 47", (False, False, True)),                              # Stalemate    
        ("8/8/4K3/8/8/8/2R5/k2R4 b - - 0 62", (True, True, False))                              # Checkmate
    ])
    def test_detect_check_checkmate_stalemate(self, fen : str, expected : tuple[bool, bool, bool]) -> None:
        c = Chess(fen=fen)
        check, checkmate, stalemate = c.detect_check_checkmate_stalemate()
        assert check == expected[0] and checkmate == expected[1] and stalemate == expected[2]


    # To test the chess gameloops we simulate a very short game with hardcoded inputs
    # The game is a checkmate in 4 moves (f2f3, e7e5, g2g4, d8h4)
    # We simulate the inputs for the game with a generator that returns the inputs (terminal coordinates)
    # We expect the variable checkmate to be True at the end of the gameloop
    def test_multiplayer_gameloop(self, monkeypatch):
        
        # Mock the user input
        def input_factory():
            inputs = [(25, 18, False), (25, 15, False), # f2f3
                      (20, 3 , False), (20, 9 , False), # e7e5
                      (30, 18, False), (30, 12, False), # g2g4
                      (15, 0 , False), (35, 12, False)] # d8h4 (checkmate)
            for i in inputs:
                yield i

        input_gen = input_factory()

        def get_next_input(*args):
            return next(input_gen)
        
        monkeypatch.setattr(Chess, "get_input", get_next_input)

        
        # Mock the curses functions
        def mock_init_curses(self, *args):
            return None, None, None    
        
        monkeypatch.setattr(Chess, "init_curses", mock_init_curses)
        monkeypatch.setattr(Chess, "check_terminal_size", lambda *args: True)
        monkeypatch.setattr(Chess, "update_screen", lambda *args: None)

        
        c = Chess()
        c.multiplayer_gameloop(None)
        assert c.checkmate == True


    # Same as above but for the single player gameloop
    def test_singleplayer_gameloop(self, monkeypatch):

        # We need to mock the chess engine to return the moves we want 
        def chess_engine_best_move_factory():
            best_moves = [(4, 1 , 4, 3), # e7e5
                          (3, 0, 7, 4)]  # d8h4 (checkmate)
            for best_move in best_moves:
                yield best_move

        best_move_gen = chess_engine_best_move_factory()

        def get_next_best_move(*args):
            return next(best_move_gen)
        
        monkeypatch.setattr(ChessEngine, "__init__", lambda *args: None)
        monkeypatch.setattr(ChessEngine, "get_move", get_next_best_move)
        monkeypatch.setattr(ChessEngine, "close", lambda *args: None)

        # Mock the user input
        def input_factory():
            inputs = [(25, 18, False), (25, 15, False), # f2f3
                      (30, 18, False), (30, 12, False)] # g2g4
            for i in inputs:
                yield i

        input_gen = input_factory()

        def get_next_input(*args):
            return next(input_gen)
        
        monkeypatch.setattr(Chess, "get_input", get_next_input)


        # Mock the curses functions
        def mock_init_curses(self, *args):
            return None, None, None
        
        monkeypatch.setattr(Chess, "init_curses", mock_init_curses)
        monkeypatch.setattr(Chess, "check_terminal_size", lambda *args: True)
        monkeypatch.setattr(Chess, "update_screen", lambda *args: None)


        c = Chess()
        c.single_player_gameloop(None)
        assert c.checkmate == True

        