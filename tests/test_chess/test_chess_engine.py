import pytest # type: ignore
from gamehub.chess.chess_engine import ChessEngine

class TestChessEngine:
    def test_chess_engine_move(self, monkeypatch):
        monkeypatch.setattr(ChessEngine, "__init__", lambda n: None)
        monkeypatch.setattr(ChessEngine, "get_move", lambda n: "e7e5")

        ce = ChessEngine()
        move = ce.get_move()
        assert ce.convert_algebraic_to_coordinates(move) == (4,1,4,3)
