import pytest
from gamehub.chess.piece_type import PieceType
import gamehub.chess.chess_board as cb
from gamehub.chess.chess_piece import ChessPiece
from collections import Counter


class TestChessBoard:
    @pytest.mark.parametrize("piece, color, position, fen, expected",
                                [(PieceType.ROOK, 'b', (0, 0), "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1", []),
                                 (PieceType.ROOK, 'w', (0, 3), "8/8/8/R3k3/8/8/8/8 w KQkq - 0 1", [(0,0), (0,1), (0,2), (0,4), (0,5), (0,6), (0,7), (1,3), (2,3), (3,3), (4,3)]),
                                 (PieceType.ROOK, 'w', (0, 3), "8/8/8/R3K3/8/8/8/8 w KQkq - 0 1", [(0,0), (0,1), (0,2), (0,4), (0,5), (0,6), (0,7), (1,3), (2,3), (3,3)])])                       
    def test_legal_moves_rook(self, piece: PieceType, color : str, position : tuple[int,int], fen : str, expected : tuple) -> None:
        matrix = cb.ChessBoard(fen).matrix
        piece = ChessPiece(piece, color, position)
        assert Counter(piece.legal_moves(matrix)) == Counter(expected)

    @pytest.mark.parametrize("piece, color, position, fen, expected",
                                [(PieceType.BISHOP, 'b', (2, 0), "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1", []),
                                 (PieceType.BISHOP, 'w', (0, 3), "8/8/8/B7/8/8/3P4/8 w KQkq - 0 1", [(1,2), (2,1), (3,0), (1,4), (2,5)]),
                                 (PieceType.BISHOP, 'w', (0, 3), "8/8/8/B7/8/8/3p4/8 w KQkq - 0 1", [(1,2), (2,1), (3,0), (1,4), (2,5), (3,6)])])
    def test_legal_moves_bishop(self, piece: PieceType, color : str, position : tuple[int,int], fen : str, expected : tuple) -> None:
        matrix = cb.ChessBoard(fen).matrix
        piece = ChessPiece(piece, color, position)
        assert Counter(piece.legal_moves(matrix)) == Counter(expected)

    @pytest.mark.parametrize("piece, color, position, fen, expected",
                                [(PieceType.KNIGHT, 'b', (1, 0), "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1", [(0,2), (2,2)]),
                                    (PieceType.KNIGHT, 'w', (0, 3), "8/8/2p5/N7/8/8/8/8 w KQkq - 0 1", [(1,1), (2,2), (2,4), (1,5)]),
                                    (PieceType.KNIGHT, 'w', (0, 3), "8/8/2P5/N7/8/8/8/8 w KQkq - 0 1", [(1,1), (2,4), (1,5)])])
    def test_legal_moves_knight(self, piece: PieceType, color : str, position : tuple[int,int], fen : str, expected : tuple) -> None:
        matrix = cb.ChessBoard(fen).matrix
        piece = ChessPiece(piece, color, position)
        assert Counter(piece.legal_moves(matrix)) == Counter(expected)


    @pytest.mark.parametrize("piece, color, position, fen, expected",
                                [(PieceType.QUEEN, 'b', (3, 0), "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1", []),
                                 (PieceType.QUEEN, 'w', (0, 3), "8/8/8/Q2p4/8/8/3p4/8 w KQkq - 0 1", [(0,0), (0,1), (0,2), (0,4), (0,5), (0,6), (0,7), (1,3), (2,3), (3,3), (1,2), (2,1), (3,0), (1,4), (2,5), (3,6)]),
                                 (PieceType.QUEEN, 'w', (0, 3), "8/8/8/Q2P4/8/8/3P4/8 w KQkq - 0 1", [(0,0), (0,1), (0,2), (0,4), (0,5), (0,6), (0,7), (1,3), (2,3), (1,2), (2,1), (3,0), (1,4), (2,5)])])
    def test_legal_moves_queen(self, piece: PieceType, color : str, position : tuple[int,int], fen : str, expected : tuple) -> None:
        matrix = cb.ChessBoard(fen).matrix
        piece = ChessPiece(piece, color, position)
        assert Counter(piece.legal_moves(matrix)) == Counter(expected)
