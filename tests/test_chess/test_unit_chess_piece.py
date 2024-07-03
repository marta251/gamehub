import pytest
from gamehub.chess.piece_type import PieceType
import gamehub.chess.chess_board as cb
from gamehub.chess.chess_piece import ChessPiece
from collections import Counter


class TestChessBoard:
    @pytest.mark.parametrize("piece, color, position, fen, expected",
                                [(PieceType.ROOK, 'w', (0, 0), "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1", []),
                                 (PieceType.ROOK, 'b', (0, 3), "8/8/8/R3k3/8/8/8/8 w KQkq - 0 1", [(0,0), (0,1), (0,2), (0,4), (0,5), (0,6), (0,7), (1,3), (2,3), (3,3), (4,3)]),
                                 (PieceType.ROOK, 'b', (0, 3), "8/8/8/R3K3/8/8/8/8 w KQkq - 0 1", [(0,0), (0,1), (0,2), (0,4), (0,5), (0,6), (0,7), (1,3), (2,3), (3,3)])])                       
    def test_legal_moves_rook(self, piece: PieceType, color : str, position : tuple[int,int], fen : str, expected : tuple) -> None:
        matrix = cb.ChessBoard(fen).matrix
        piece = ChessPiece(piece, color, position)
        print(piece.legal_moves(matrix))
        print(expected)
        assert Counter(piece.legal_moves(matrix)) == Counter(expected)