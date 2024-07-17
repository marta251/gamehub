"""
Module that contains the TestChessEngine class,
which is used to test the ChessEngine class.
"""
from gamehub.chess.chess_engine import ChessEngine

class TestChessEngine:
    """
    Class to test the ChessEngine class
    """
    def test_chess_engine_move(self, monkeypatch):
        """
        Verify that the convert_algebraic_to_coordinates method works as expected.
        """
        monkeypatch.setattr(ChessEngine, "__init__", lambda n: None)
        monkeypatch.setattr(ChessEngine, "get_move", lambda n: "e7e5")

        chess_engine = ChessEngine()
        move = chess_engine.get_move()
        assert chess_engine.convert_algebraic_to_coordinates(move) == (4,1,4,3)
