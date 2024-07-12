import pytest  # type: ignore
from gamehub.chess.chess_board import ChessBoard
from gamehub.chess.chess_piece import ChessPiece

class TestChessBoard:
    @pytest.mark.parametrize("fen, expected",
                                [("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1",
                                ('w', 'KQkq', '-', 0, 1))])
    def test_constructor_chess_board_from_fen(self, fen : str, expected : tuple[list[list[ChessPiece]], str, str, str, int, int]) -> None:
            
        board = ChessBoard(fen)
        assert (board.playerToMove == expected[1] and
                board.castlingRights == expected[2] and
                board.enPassant == expected[3] and
                board.halfMoveCounter == expected[4] and
                board.fullMoveCounter == expected[5])
        
    @pytest.mark.parametrize("board, expected",
                                [(
                                ([[ChessPiece('r', (0, 0)), ChessPiece('n', (1, 0)), ChessPiece('b', (2, 0)), ChessPiece('q', (3, 0)), ChessPiece('k', (4, 0)), ChessPiece('b', (5, 0)), ChessPiece('n', (6, 0)), ChessPiece('r', (7, 0))],
                                [ChessPiece('p', (0, 1)), ChessPiece('p', (1, 1)), ChessPiece('p', (2, 1)), ChessPiece('p', (3, 1)), ChessPiece('p', (4, 1)), ChessPiece('p', (5, 1)), ChessPiece('p', (6, 1)), ChessPiece('p', (7, 1))],
                                [None, None, None, None, None, None, None, None],
                                [None, None, None, None, None, None, None, None],
                                [None, None, None, None, None, None, None, None],
                                [None, None, None, None, None, None, None, None],
                                [ChessPiece('P', (0, 6)), ChessPiece('P', (1, 6)), ChessPiece('P', (2, 6)), ChessPiece('P', (3, 6)), ChessPiece('P', (4, 6)), ChessPiece('P', (5, 6)), ChessPiece('P', (6, 6)), ChessPiece('P', (7, 6))],
                                [ChessPiece('R', (0, 7)), ChessPiece('N', (1, 7)), ChessPiece('B', (2, 7)), ChessPiece('Q', (3, 7)), ChessPiece('K', (4, 7)), ChessPiece('B', (5, 7)), ChessPiece('N', (6, 7)), ChessPiece('R', (7, 7))]], 
                                'w', 'KQkq', '-', 0, 1),
                                ([[ChessPiece('r', (0, 0)), ChessPiece('n', (1, 0)), ChessPiece('b', (2, 0)), ChessPiece('q', (3, 0)), ChessPiece('k', (4, 0)), ChessPiece('b', (5, 0)), ChessPiece('n', (6, 0)), ChessPiece('r', (7, 0))],
                                [ChessPiece('p', (0, 1)), ChessPiece('p', (1, 1)), ChessPiece('p', (2, 1)), ChessPiece('p', (3, 1)), ChessPiece('p', (4, 1)), ChessPiece('p', (5, 1)), ChessPiece('p', (6, 1)), ChessPiece('p', (7, 1))],
                                [None, None, None, None, None, None, None, None],
                                [None, None, None, None, None, None, None, None],
                                [None, None, None, None, None, None, None, None],
                                [None, None, None, None, None, None, None, None],
                                [ChessPiece('P', (0, 6)), ChessPiece('P', (1, 6)), ChessPiece('P', (2, 6)), ChessPiece('P', (3, 6)), ChessPiece('P', (4, 6)), ChessPiece('P', (5, 6)), ChessPiece('P', (6, 6)), ChessPiece('P', (7, 6))],
                                [ChessPiece('R', (0, 7)), ChessPiece('N', (1, 7)), ChessPiece('B', (2, 7)), ChessPiece('Q', (3, 7)), ChessPiece('K', (4, 7)), ChessPiece('B', (5, 7)), ChessPiece('N', (6, 7)), ChessPiece('R', (7, 7))]], 
                                'w', 'KQkq', '-', 0, 1))])
    def test_constructor_chess_board_from_fen(self, board : tuple[list[list[ChessPiece]], str, str, str, int, int] , expected : tuple[list[list[ChessPiece]], str, str, str, int, int]) -> None:
        board = ChessBoard(matrix=board[0], playerToMove=board[1], castlingRights=board[2], enPassant=board[3], halfMoveCounter=board[4], fullMoveCounter=board[5])
        assert (board.matrix == expected[0] and
                board.playerToMove == expected[1] and
                board.castlingRights == expected[2] and
                board.enPassant == expected[3] and
                board.halfMoveCounter == expected[4] and
                board.fullMoveCounter == expected[5])
    
    @pytest.mark.parametrize("fen",
                             [("rnbqkbnr/pppppppp/8/8/8/8/RNBQKBNR w KQkq - 0 1"),
                              ("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - a 1"),
                              ("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 c"),
                              ("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR n KQkq - 0 1"),
                              ("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR n 1010 - 0 1"),
                              ("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR n KQkq 0 1"),
                              ])
    def test_constructor_raises_exception_invalid_fen(self, fen : str) -> None:
        with pytest.raises(ValueError):
            ChessBoard(fen)

    @pytest.mark.parametrize("arguments",
                             [((None, None, None, None, None, None, None)),
                            ((None, None, "w", "KQkq", "-", 1, 5)),
                            ((None, None, "b", "-", "-", 1, 5)),
                            ((None, None, "w", "KQkq", None, 1, 5)),
                              ])
    def test_constructor_raises_exception_invalid_arguments(self, arguments : tuple) -> None:
        with pytest.raises(ValueError):
            ChessBoard(arguments[0], arguments[1], arguments[2], arguments[3], arguments[4], arguments[5], arguments[6])
