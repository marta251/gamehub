import pytest # type: ignore
import gamehub.chess.chess_board as cb

class TestChessBoard:
    @pytest.mark.parametrize("fen, expected",
                             [("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1",
                               ([['r', 'n', 'b', 'q', 'k', 'b', 'n', 'r'],
                                ['p', 'p', 'p', 'p', 'p', 'p', 'p', 'p'],
                                [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
                                [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
                                [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
                                [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
                                ['P', 'P', 'P', 'P', 'P', 'P', 'P', 'P'],
                                ['R', 'N', 'B', 'Q', 'K', 'B', 'N', 'R']],'w', 'KQkq', '-', 0, 1))])
    def test_board_constructor(self, fen : str, expected : tuple) -> None:
        board = cb.ChessBoard(fen)
        assert (board.matrix == expected[0] and
                board.playerToMove == expected[1] and
                board.castlingRights == expected[2] and
                board.enPassant == expected[3] and
                board.halfMoveCounter == expected[4] and
                board.fullMoveCounter == expected[5])
    
    
    @pytest.mark.parametrize("expected, board",
                             [("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1",
                               ([['r', 'n', 'b', 'q', 'k', 'b', 'n', 'r'],
                                 ['p', 'p', 'p', 'p', 'p', 'p', 'p', 'p'],
                                 [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
                                 [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
                                 [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
                                 [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
                                 ['P', 'P', 'P', 'P', 'P', 'P', 'P', 'P'],
                                 ['R', 'N', 'B', 'Q', 'K', 'B', 'N', 'R']],'w', 'KQkq', '-', 0, 1))])
    def test_convert_board_to_fen(self, expected : str, board : tuple) -> None:
        board = cb.ChessBoard(matrix=board[0], playerToMove=board[1], castlingRights=board[2], enPassant=board[3], halfMoveCounter=board[4], fullMoveCounter=board[5])
        assert board.convert_board_to_fen() == expected