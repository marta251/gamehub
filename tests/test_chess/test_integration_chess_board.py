"""
Module that contains the TestChessBoardIntegration class,
which is used to test the ChessBoard class integrated with the ChessPiece class.
"""
import pytest
from gamehub.chess.chess_piece import ChessPiece
from gamehub.chess.chess_board import ChessBoard

class TestChessBoardIntegration:
    """
    Class to test the ChessBoard class integrated with the ChessPiece class.
    """
    @pytest.mark.parametrize("fen, expected",
                                [("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1",
                                [[ChessPiece('r', (0, 0)), ChessPiece('n', (1, 0)), ChessPiece('b', (2, 0)), ChessPiece('q', (3, 0)), ChessPiece('k', (4, 0)), ChessPiece('b', (5, 0)), ChessPiece('n', (6, 0)), ChessPiece('r', (7, 0))],
                                [ChessPiece('p', (0, 1)), ChessPiece('p', (1, 1)), ChessPiece('p', (2, 1)), ChessPiece('p', (3, 1)), ChessPiece('p', (4, 1)), ChessPiece('p', (5, 1)), ChessPiece('p', (6, 1)), ChessPiece('p', (7, 1))],
                                [None, None, None, None, None, None, None, None],
                                [None, None, None, None, None, None, None, None],
                                [None, None, None, None, None, None, None, None],
                                [None, None, None, None, None, None, None, None],
                                [ChessPiece('P', (0, 6)), ChessPiece('P', (1, 6)), ChessPiece('P', (2, 6)), ChessPiece('P', (3, 6)), ChessPiece('P', (4, 6)), ChessPiece('P', (5, 6)), ChessPiece('P', (6, 6)), ChessPiece('P', (7, 6))],
                                [ChessPiece('R', (0, 7)), ChessPiece('N', (1, 7)), ChessPiece('B', (2, 7)), ChessPiece('Q', (3, 7)), ChessPiece('K', (4, 7)), ChessPiece('B', (5, 7)), ChessPiece('N', (6, 7)), ChessPiece('R', (7, 7))]])])
    def test_constructor_chess_board_from_fen(self, fen : str, expected : tuple[list[list[ChessPiece]]]) -> None:
        """
        Verify that the constructor of the ChessBoard class works as expected when given a FEN string.
        """
        assert ChessBoard(fen).matrix == expected

    @pytest.mark.parametrize("expected, board",
                                [("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1",
                                ([[ChessPiece('r', (0, 0)), ChessPiece('n', (1, 0)), ChessPiece('b', (2, 0)), ChessPiece('q', (3, 0)), ChessPiece('k', (4, 0)), ChessPiece('b', (5, 0)), ChessPiece('n', (6, 0)), ChessPiece('r', (7, 0))],
                                [ChessPiece('p', (0, 1)), ChessPiece('p', (1, 1)), ChessPiece('p', (2, 1)), ChessPiece('p', (3, 1)), ChessPiece('p', (4, 1)), ChessPiece('p', (5, 1)), ChessPiece('p', (6, 1)), ChessPiece('p', (7, 1))],
                                [None, None, None, None, None, None, None, None],
                                [None, None, None, None, None, None, None, None],
                                [None, None, None, None, None, None, None, None],
                                [None, None, None, None, None, None, None, None],
                                [ChessPiece('P', (0, 6)), ChessPiece('P', (1, 6)), ChessPiece('P', (2, 6)), ChessPiece('P', (3, 6)), ChessPiece('P', (4, 6)), ChessPiece('P', (5, 6)), ChessPiece('P', (6, 6)), ChessPiece('P', (7, 6))],
                                [ChessPiece('R', (0, 7)), ChessPiece('N', (1, 7)), ChessPiece('B', (2, 7)), ChessPiece('Q', (3, 7)), ChessPiece('K', (4, 7)), ChessPiece('B', (5, 7)), ChessPiece('N', (6, 7)), ChessPiece('R', (7, 7))]],
                                'w', 'KQkq', '-', 0, 1))])
    def test_convert_board_to_fen(self, expected : str, board : tuple[list[list[ChessPiece]], str, str, str, int, int]) -> None:
        """
        Test the convert_board_to_fen method, verify that it returns the correct FEN string.
        """
        board = ChessBoard(matrix=board[0], playerToMove=board[1], castlingRights=board[2], enPassant=board[3], halfMoveCounter=board[4], fullMoveCounter=board[5])
        assert board.convert_board_to_fen() == expected

    @pytest.mark.parametrize("fen, color, expected",
                                [("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1", "w", (4, 7)),
                                 ("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1", "b", (4, 0)),
                                 ("rn1q1rk1/pp2b1pp/2p2n2/3p1pB1/3P4/1QP2N2/PP1N1PPP/R4RK1 b - - 1 11", "w", (6, 7)),
                                 ("rn1q1rk1/pp2b1pp/2p2n2/3p1pB1/3P4/1QP2N2/PP1N1PPP/R4RK1 b - - 1 11", "b", (6, 0))
                                ])
    def test_detect_king_coordinates(self, fen : str, color : str, expected : tuple[int, int]) -> None:
        """
        Test that the detect_king_coordinates method returns the correct coordinates of the king.
        """
        board = ChessBoard(fen)
        assert board.detect_king_coordinates(color) == expected
