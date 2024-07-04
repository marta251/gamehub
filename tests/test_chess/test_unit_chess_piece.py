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

    @pytest.mark.parametrize("piece, color, position, fen, expected",
                                [(PieceType.PAWN, 'w', (4, 6), "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1", [(4,5), (4,4)]),
                                 (PieceType.PAWN, 'b', (3, 3), "rn1q1rk1/pp2b1pp/2p2n2/3p1pB1/3P4/1QP2N2/PP1N1PPP/R4RK1 b - - 1 11", []),
                                 (PieceType.PAWN, 'w', (3, 4), "rn1q1rk1/pp2b1pp/5n2/2pp1pB1/3P4/1QP2N2/PP1N1PPP/R4RK1 w - - 1 12", [(2,3)])])
    def test_legal_moves_pawn(self, piece: PieceType, color : str, position : tuple[int,int], fen : str, expected : tuple) -> None:
        matrix = cb.ChessBoard(fen).matrix
        piece = ChessPiece(piece, color, position)
        assert Counter(piece.legal_moves(matrix)) == Counter(expected)

    @pytest.mark.parametrize("piece, color, position, fen, expected",
                                [(PieceType.KING, 'w', (4, 7), "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1", []),
                                 (PieceType.KING, 'w', (0, 3), "8/8/P7/Kp6/8/8/8/8 w KQkq - 0 1", [(1,2), (1,3), (1,4), (0,4)])])
    def test_legal_moves_king(self, piece: PieceType, color : str, position : tuple[int,int], fen : str, expected : tuple) -> None:
        matrix = cb.ChessBoard(fen).matrix
        piece = ChessPiece(piece, color, position)
        assert Counter(piece.legal_moves(matrix)) == Counter(expected)


    @pytest.mark.parametrize("color, fen, expected",
                                [('w', "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1", False),
                                 ('b', "rn1q1rk1/pp2b1pp/5n2/2pp1pB1/3P4/1QP2N2/PP1N1PPP/R4RK1 w - - 1 12", False),
                                 ('b', "rn1q1rk1/pp2b1pp/5n2/2p2pB1/3P4/1QP2N2/PP1N1PPP/R4RK1 w - - 1 12", True),
                                 ('w', "rn1q1rk1/pp2b1pp/5n2/2p2pB1/3P4/1QP2N2/PP1N1PPP/R4RK1 w - - 1 12", False)])
    def test_king_under_attack(self, color : str, fen : str, expected : bool) -> None:
        matrix = cb.ChessBoard(fen).matrix
        piece = ChessPiece(PieceType.KING, color, (0,0)) # position and piece type doesn't matter for this test
        assert piece.king_under_attack(matrix) == expected
    




    '''
    Visto che è parametrica potresti fare na roba del genere ...
    @pytest.mark.parametrize("piece, color, position, fen, expected",
                                [
                                    (PieceType.ROOK, 'b', (0, 0), "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1", []),
                                    (PieceType.ROOK, 'w', (0, 3), "8/8/8/R3k3/8/8/8/8 w KQkq - 0 1", [(0,0), (0,1), (0,2), (0,4), (0,5), (0,6), (0,7), (1,3), (2,3), (3,3), (4,3)]),
                                    (PieceType.ROOK, 'w', (0, 3), "8/8/8/R3K3/8/8/8/8 w KQkq - 0 1", [(0,0), (0,1), (0,2), (0,4), (0,5), (0,6), (0,7), (1,3), (2,3), (3,3)]),
                                    (PieceType.BISHOP, 'b', (2, 0), "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1", []),
                                    (PieceType.BISHOP, 'w', (0, 3), "8/8/8/B7/8/8/3P4/8 w KQkq - 0 1", [(1,2), (2,1), (3,0), (1,4), (2,5)]),
                                    (PieceType.BISHOP, 'w', (0, 3), "8/8/8/B7/8/8/3p4/8 w KQkq - 0 1", [(1,2), (2,1), (3,0), (1,4), (2,5), (3,6)]),
                                    (PieceType.KNIGHT, 'b', (1, 0), "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1", [(0,2), (2,2)]),
                                    (PieceType.KNIGHT, 'w', (0, 3), "8/8/2p5/N7/8/8/8/8 w KQkq - 0 1", [(1,1), (2,2), (2,4), (1,5)]),
                                    (PieceType.KNIGHT, 'w', (0, 3), "8/8/2P5/N7/8/8/8/8 w KQkq - 0 1", [(1,1), (2,4), (1,5)]),
                                    (PieceType.QUEEN, 'b', (3, 0), "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1", []),
                                    (PieceType.QUEEN, 'w', (0, 3), "8/8/8/Q2p4/8/8/3p4/8 w KQkq - 0 1", [(0,0), (0,1), (0,2), (0,4), (0,5), (0,6), (0,7), (1,3), (2,3), (3,3), (1,2), (2,1), (3,0), (1,4), (2,5), (3,6)]),
                                    (PieceType.QUEEN, 'w', (0, 3), "8/8/8/Q2P4/8/8/3P4/8 w KQkq - 0 1", [(0,0), (0,1), (0,2), (0,4), (0,5), (0,6), (0,7), (1,3), (2,3), (1,2), (2,1), (3,0), (1,4), (2,5)]),
                                    (PieceType.PAWN, 'w', (4, 6), "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1", [(4,5), (4,4)]),
                                    (PieceType.PAWN, 'b', (3, 3), "rn1q1rk1/pp2b1pp/2p2n2/3p1pB1/3P4/1QP2N2/PP1N1PPP/R4RK1 b - - 1 11", []),
                                    (PieceType.PAWN, 'w', (3, 4), "rn1q1rk1/pp2b1pp/5n2/2pp1pB1/3P4/1QP2N2/PP1N1PPP/R4RK1 w - - 1 12", [(2,3)])
                                ])                       
    def test_legal_moves(self, piece: PieceType, color : str, position : tuple[int,int], fen : str, expected : tuple) -> None:
        matrix = cb.ChessBoard(fen).matrix
        piece = ChessPiece(piece, color, position)
        assert Counter(piece.legal_moves(matrix)) == Counter(expected)
    '''
    
