import pytest  # type: ignore
from gamehub.chess.chess_piece import ChessPiece
from collections import Counter

class TestChessPiece:
    #I define the matrix without using the ChessBoard class since I'm unit testing the ChessPiece class
    def chess_piece_matrix_factory(self) -> list[list[ChessPiece]]:
        # Magnus Carlsen vs Hikaru Nakamura 
        # 12th Norway Chess (2024) (armageddon), Stavanger NOR, rd 2, May-28 Move 20 (Bxd3)
        matrix = [[None for _ in range(8)] for _ in range(8)]
        matrix[0][2]= ChessPiece("q", (2 ,0))
        matrix[0][3]= ChessPiece("r", (3 ,0))
        matrix[0][4]= ChessPiece("r", (4 ,0))
        matrix[0][6]= ChessPiece("k", (6 ,0))
        matrix[1][1]= ChessPiece("b", (1 ,1))
        matrix[1][5]= ChessPiece("p", (5 ,1))  
        matrix[1][6]= ChessPiece("p", (6 ,1))    
        matrix[1][7]= ChessPiece("p", (7 ,1))    
        matrix[2][0]= ChessPiece("p", (0 ,2))
        matrix[2][3]= ChessPiece("p", (3 ,2))
        matrix[2][6]= ChessPiece("n", (6 ,2))
        matrix[3][1]= ChessPiece("p", (1 ,3))
        matrix[3][7]= ChessPiece("Q", (7 ,3))
        matrix[4][2]= ChessPiece("p", (2 ,4))
        matrix[4][4]= ChessPiece("P", (4 ,4))
        matrix[5][2]= ChessPiece("P", (2 ,5))
        matrix[5][3]= ChessPiece("B", (3 ,5))
        matrix[5][6]= ChessPiece("B", (6 ,5))
        matrix[6][0]= ChessPiece("P", (0 ,6))
        matrix[6][1]= ChessPiece("P", (1 ,6))
        matrix[6][5]= ChessPiece("P", (5 ,6))
        matrix[6][6]= ChessPiece("P", (6 ,6))
        matrix[6][7]= ChessPiece("P", (7 ,6))
        matrix[7][3]= ChessPiece("R", (3 ,7))
        matrix[7][4]= ChessPiece("R", (4 ,7))
        matrix[7][5]= ChessPiece("N", (5 ,7))
        matrix[7][6]= ChessPiece("K", (6 ,7))
        
        return matrix
    
    # For each piece I test the legal moves
    @pytest.mark.parametrize("position, expected",
                                [((2, 0), [(0, 0), (1, 0), (2, 1), (2, 2), (2, 3), (3, 1), (4, 2), (5, 3), (6, 4), (7, 5)]),
                                 ((3, 0), [(3, 1)]),
                                 ((4, 0), [(4, 1), (4, 2), (4, 3), (4, 4), (5, 0)]),
                                 ((6, 0), [(5, 0), (7, 0)]),
                                 ((1, 1), [(0, 0), (2, 2), (3, 3), (4, 4)]),
                                 ((5, 1), [(5, 2), (5, 3)]),
                                 ((6, 1), []),
                                 ((7, 1), [(7, 2)]),
                                 ((0, 2), [(0, 3)]),
                                 ((3, 2), [(3, 3)]),
                                 ((6, 2), [(5, 0), (7, 0), (4, 1), (4, 3), (5, 4), (7, 4)]),
                                 ((1, 3), [(1, 4)]),
                                 ((7, 3), [(7, 2), (7, 1), (6, 2), (7, 4), (7, 5), (6, 4), (5, 5), (4, 6), (6, 3), (5, 3), (4, 3), (3, 3), (2, 3), (1, 3)]),
                                 ((2, 4), [(3, 5)]),
                                 ((4, 4), [(4, 3)]),
                                 ((2, 5), []),
                                 ((3, 5), [(2, 4), (2, 6), (1, 7), (4, 6)]),
                                 ((6, 5), [(5, 4), (4, 3), (3, 2), (7, 4)]),
                                 ((0, 6), [(0, 5), (0, 4)]),
                                 ((1, 6), [(1, 5), (1, 4)]),
                                 ((5, 6), [(5, 5), (5, 4)]),
                                 ((6, 6), []),
                                 ((7, 6), [(7, 5), (7, 4)]),
                                 ((3, 7), [(3, 6), (2, 7), (1, 7), (0, 7)]),
                                 ((4, 7), [(4, 6), (4, 5)]),
                                 ((5, 7), [(3, 6), (4, 5)]),
                                 ((6, 7), [(7, 7)])
                                 ])                                                      
    def test_legal_moves(self, position : tuple[int,int], expected : tuple) -> None:
        matrix = self.chess_piece_matrix_factory()
        piece = matrix[position[1]][position[0]]
        assert Counter(piece.legal_moves(matrix)) == Counter(expected)

    @pytest.mark.parametrize("char, position, expected",
                               [("q", (2, 0), ("q", (2, 0), "Queen", "b", "♕")),
                                ("r", (3, 0), ("r", (3, 0), "Rook", "b", "♖")),
                                ("R", (4, 7), ("R", (4, 7), "Rook", "w", "♜")),
                                ("N", (5, 7), ("N", (5, 7), "Knight", "w", "♞"))])
    def test_chess_piece_constructor(self, char : str, position : tuple[int, int], expected : tuple[str,tuple[int,int],str,str,str]) -> None:
        piece = ChessPiece(char, position)
        assert (piece.piece_char == expected[0] and
                piece.position == expected[1] and
                piece.piece == expected[2] and
                piece.color == expected[3] and
                piece.piece_symbol == expected[4])
    @pytest.mark.parametrize("char, position",
                                 [("a", (0, 0)),
                                  ("H", (0, 0)),
                                  ("c", (0, 0)),
                                  ("Q", (0, 8)),
                                  ("q", (-1, 0)),
                                  ("n", (0, -1)),
                                  ("p", (121, 0))])
    def test_chess_piece_constructor_invalid_piece(self, char : str, position : tuple[int,int]) -> None:
        with pytest.raises(ValueError):
            ChessPiece(char, position)
