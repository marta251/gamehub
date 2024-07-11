from gamehub.chess.chess import Chess
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