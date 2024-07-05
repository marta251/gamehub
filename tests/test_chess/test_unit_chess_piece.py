import pytest 
from gamehub.chess.chess_board import ChessBoard
from collections import Counter


class TestChessBoard:
    @pytest.mark.parametrize("position, fen, expected",
                                [((0, 0), "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1", []),
                                 ((0, 3), "7k/8/8/R3k3/8/8/8/7K w KQkq - 0 1", [(0,0), (0,1), (0,2), (0,4), (0,5), (0,6), (0,7), (1,3), (2,3), (3,3), (4,3)]),
                                 ((0, 3), "7k/8/8/R3K3/8/8/8/7K w KQkq - 0 1", [(0,0), (0,1), (0,2), (0,4), (0,5), (0,6), (0,7), (1,3), (2,3), (3,3)])])                       
    def test_legal_moves_rook(self, position : tuple[int,int], fen : str, expected : tuple) -> None:
        matrix = ChessBoard(fen).matrix
        piece = matrix[position[1]][position[0]]
        print (matrix)
        print (piece)

        assert Counter(piece.legal_moves(matrix)) == Counter(expected)
    
    @pytest.mark.parametrize("position, fen, expected",
                                [((2, 0), "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1", []),
                                 ((0, 3), "7K/8/8/B7/8/8/3P4/7k w KQkq - 0 1", [(1,2), (2,1), (3,0), (1,4), (2,5)]),
                                 ((0, 3), "7K/8/8/B7/8/8/3p4/7k w KQkq - 0 1", [(1,2), (2,1), (3,0), (1,4), (2,5), (3,6)])])
    def test_legal_moves_bishop(self, position : tuple[int,int], fen : str, expected : tuple) -> None:
        board = ChessBoard(fen)
        matrix = board.matrix
        piece = matrix[position[1]][position[0]]
        assert Counter(piece.legal_moves(matrix)) == Counter(expected)

    @pytest.mark.parametrize("position, fen, expected",
                                [((1, 0), "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1", [(0,2), (2,2)]),
                                 ((0, 3), "7k/8/2p5/N7/8/8/8/7K w KQkq - 0 1", [(1,1), (2,2), (2,4), (1,5)]),
                                 ((0, 3), "7k/8/2P5/N7/8/8/8/7K w KQkq - 0 1", [(1,1), (2,4), (1,5)])])
    def test_legal_moves_knight(self, position : tuple[int,int], fen : str, expected : tuple) -> None:
        matrix = ChessBoard(fen).matrix
        piece = matrix[position[1]][position[0]]
        assert Counter(piece.legal_moves(matrix)) == Counter(expected)


    @pytest.mark.parametrize("position, fen, expected",
                                [((3, 0), "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1", []),
                                 ((0, 3), "7k/8/8/Q2p4/8/8/3p4/7K w KQkq - 0 1", [(0,0), (0,1), (0,2), (0,4), (0,5), (0,6), (0,7), (1,3), (2,3), (3,3), (1,2), (2,1), (3,0), (1,4), (2,5), (3,6)]),
                                 ((0, 3), "7k/8/8/Q2P4/8/8/3P4/7K w KQkq - 0 1", [(0,0), (0,1), (0,2), (0,4), (0,5), (0,6), (0,7), (1,3), (2,3), (1,2), (2,1), (3,0), (1,4), (2,5)])])
    def test_legal_moves_queen(self, position : tuple[int,int], fen : str, expected : tuple) -> None:
        matrix = ChessBoard(fen).matrix
        piece = matrix[position[1]][position[0]]
        assert Counter(piece.legal_moves(matrix)) == Counter(expected)

    @pytest.mark.parametrize("position, fen, expected",
                                [((4, 6), "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1", [(4,5), (4,4)]),
                                 ((3, 3), "rn1q1rk1/pp2b1pp/2p2n2/3p1pB1/3P4/1QP2N2/PP1N1PPP/R4RK1 b - - 1 11", []),
                                 ((3, 4), "rn1q1rk1/pp2b1pp/5n2/2pp1pB1/3P4/1QP2N2/PP1N1PPP/R4RK1 w - - 1 12", [(2,3)])])
    def test_legal_moves_pawn(self, position : tuple[int,int], fen : str, expected : tuple) -> None:
        matrix = ChessBoard(fen).matrix
        piece = matrix[position[1]][position[0]]
        assert Counter(piece.legal_moves(matrix)) == Counter(expected)

    @pytest.mark.parametrize("position, fen, expected",
                                [((4, 7), "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1", []),
                                 ((0, 3), "8/8/P7/Kp6/8/8/8/7k w KQkq - 0 1", [(1,2), (1,3), (1,4)])])
    def test_legal_moves_king(self, position : tuple[int,int], fen : str, expected : tuple) -> None:
        matrix = ChessBoard(fen).matrix
        piece = matrix[position[1]][position[0]]
        assert Counter(piece.legal_moves(matrix)) == Counter(expected)


    @pytest.mark.parametrize("position, fen, expected",
                                [((7,7), "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1", False),
                                 ((0,0), "rn1q1rk1/pp2b1pp/5n2/2pp1pB1/3P4/1QP2N2/PP1N1PPP/R4RK1 w - - 1 12", False),
                                 ((0,0), "rn1q1rk1/pp2b1pp/5n2/2p2pB1/3P4/1QP2N2/PP1N1PPP/R4RK1 w - - 1 12", True),
                                 ((6,7), "rn1q1rk1/pp2b1pp/5n2/2p2pB1/3P4/1QP2N2/PP1N1PPP/R4RK1 w - - 1 12", False)])
    def test_king_under_attack(self, position : str, fen : str, expected : bool) -> None:
        matrix = ChessBoard(fen).matrix
        piece = matrix[position[1]][position[0]]
        assert piece.king_under_attack(matrix) == expected
    

    #TODO: ValueError exception could be raised
