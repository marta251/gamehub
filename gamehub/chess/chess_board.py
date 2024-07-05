from gamehub.chess.chess_piece import ChessPiece
class ChessBoard:

    #TODO: Check validity of FEN string

    # Generates a chess board from a FEN string
    def __init__(self, fen=None, matrix=None, playerToMove=None, castlingRights=None, enPassant=None, halfMoveCounter=None, fullMoveCounter=None) -> None:
        if fen is not None:
            self.matrix = self.convert_fen_to_matrix(fen)
            self.playerToMove = fen.split(" ")[1]
            self.castlingRights = fen.split(" ")[2]
            self.enPassant = fen.split(" ")[3]
            self.halfMoveCounter = int(fen.split(" ")[4])
            self.fullMoveCounter = int(fen.split(" ")[5])
        elif matrix is not None and playerToMove is not None and castlingRights is not None and enPassant is not None and halfMoveCounter is not None and fullMoveCounter is not None:
            self.matrix = matrix
            self.playerToMove = playerToMove
            self.castlingRights = castlingRights
            self.enPassant = enPassant
            self.halfMoveCounter = halfMoveCounter
            self.fullMoveCounter = fullMoveCounter
        else:
            raise ValueError("Invalid arguments")

    # Converts a FEN string to a 2D matrix
    def convert_fen_to_matrix(self, fen: str) -> list[list[ChessPiece]]:
        matrix = []
        fen = fen.split(" ")[0]
        rows = fen.split("/")
        row_index = 0
        element_index = 0
        for row in rows:
            matrix_row = []
            for elem in row:
                if elem.isdigit():
                    for _ in range(int(elem)):
                        matrix_row.append(None)
                        element_index += 1
                else:
                    if elem.isupper():
                        piece = ChessPiece(elem, (element_index, row_index))
                    else:
                        piece = ChessPiece(elem, (element_index, row_index))
                    matrix_row.append(piece)
                    element_index += 1
            matrix.append(matrix_row)
            row_index += 1
            element_index = 0

        return matrix
    
    # Converts a 2D matrix to a FEN string
    def convert_matrix_to_fen(self, matrix: list[list[ChessPiece]]) -> str:
        fen = ""
        for row in matrix:
            empty = 0
            for elem in row:
                if elem == None:
                    empty += 1
                else:
                    if empty > 0:
                        fen += str(empty)
                        empty = 0
                    fen += elem.piece_char
            if empty > 0:
                fen += str(empty)
            fen += "/"
        return fen[:-1]
    
    # Converts the board to a FEN string
    def convert_board_to_fen(self) -> str:
        return self.convert_matrix_to_fen(self.matrix) + " " + self.playerToMove + " " + self.castlingRights + " " + self.enPassant + " " + str(self.halfMoveCounter) + " " + str(self.fullMoveCounter)


# board = ChessBoard("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1").matrix
# print(board)
# board_fen = ChessBoard(matrix=board, playerToMove="w", castlingRights="KQkq", enPassant="-", halfMoveCounter=0, fullMoveCounter=1).convert_board_to_fen()
# print(board_fen)

matrix = ChessBoard("rn1q1rk1/pp2b1pp/5n2/2p2pB1/3P4/1QP2N2/PP1N1PPP/R4RK1 w - - 1 12").matrix
piece = matrix[6][7]
print(piece.king_under_attack(matrix))
