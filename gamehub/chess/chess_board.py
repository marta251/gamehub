from gamehub.chess.chess_piece import ChessPiece

class ChessBoard:
    """
    Object representing a chess board with its pieces and attributes.

    Attributes:
    - matrix: The 2D matrix representing the board, each cell contains a ChessPiece object
    - playerToMove: The color of the player to move ("w" for white, "b" for black)
    - castlingRights: The castling rights of the players ("KQkq" for all rights, "-" for none)
    - enPassant: The en passant square (e.g. "e3" or "-") [not implemented yet]
    - halfMoveCounter: The number of half moves since the last capture or pawn move [not implemented yet]
    - fullMoveCounter: The number of full moves since the start of the game
    """
    # Generates a chess board from a FEN string or from a matrix and other parameters
    def __init__(self, fen=None, matrix=None, playerToMove=None, castlingRights=None, enPassant=None, halfMoveCounter=None, fullMoveCounter=None) -> None:
        if fen is not None:
            if not self.check_fen_validity(fen):
                raise ValueError("Invalid FEN string")
            fen_split = fen.split(" ")
            self.matrix = self.convert_fen_to_matrix(fen_split[0])
            self.playerToMove = fen_split[1]
            self.castlingRights = fen_split[2]
            self.enPassant = fen_split[3]
            self.halfMoveCounter = int(fen_split[4])
            self.fullMoveCounter = int(fen_split[5])
        elif matrix is not None and playerToMove is not None and castlingRights is not None and enPassant is not None and halfMoveCounter is not None and fullMoveCounter is not None:
            self.matrix = matrix
            self.playerToMove = playerToMove
            self.castlingRights = castlingRights
            self.enPassant = enPassant
            self.halfMoveCounter = halfMoveCounter
            self.fullMoveCounter = fullMoveCounter
        else:
            raise ValueError("Invalid arguments")

    def __eq__(self, value: object) -> bool:
        if not isinstance(value, ChessBoard):
            return False
        return (self.matrix == value.matrix and
                self.playerToMove == value.playerToMove and
                self.castlingRights == value.castlingRights and
                self.enPassant == value.enPassant and
                self.halfMoveCounter == value.halfMoveCounter and
                self.fullMoveCounter == value.fullMoveCounter)

    def check_fen_validity(self, fen: str) -> bool:
        """
        Function that checks the validity of a FEN string.

        Parameters:
        - fen: The FEN string to check

        Return:
        - True if the FEN string is valid, False otherwise
        """
        fen_split = fen.split(" ")
        if len(fen_split) != 6:
            return False
        if len(fen_split[0].split("/")) != 8:
            return False
        if fen_split[1] != "w" and fen_split[1] != "b":
            return False
        if len(fen_split[2]) > 4 or not all([c in "KQkq" for c in fen_split[2]]) and fen_split[2] != "-":
            return False
        if fen_split[3] != "-" and (len(fen_split[3]) != 2 or not fen_split[3][0].isalpha() or not fen_split[3][1].isdigit()):
            return False
        if not fen_split[4].isdigit() or not fen_split[5].isdigit():
            return False
        return True

    # Converts a FEN string to a 2D matrix
    def convert_fen_to_matrix(self, fen: str) -> list[list[ChessPiece]]:
        """
        Function that converts a FEN string (the matrix part) to a 2D matrix of ChessPiece objects.

        Parameters:
        - fen: The FEN string to convert (only the matrix part)

        Return:
        - list[list[ChessPiece]] -> The 2D matrix of ChessPiece objects
        """
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
        """
        Function that converts a 2D matrix of ChessPiece objects to a FEN string (the matrix part).

        Parameters:
        - matrix: The 2D matrix of ChessPiece objects

        Return:
        - str -> The FEN string (only the matrix part)
        """
        fen = ""
        for row in matrix:
            empty = 0
            for elem in row:
                if elem is None:
                    empty += 1
                else:
                    if empty > 0:
                        fen += str(empty)
                        empty = 0
                    fen += elem.get_piece_char()
            if empty > 0:
                fen += str(empty)
            fen += "/"
        return fen[:-1]

    # Converts the board to a FEN string
    def convert_board_to_fen(self) -> str:
        """
        Function that converts the board to a FEN string (all parts).

        Return:
        - str -> The FEN string
        """
        return self.convert_matrix_to_fen(self.matrix) + " " + self.playerToMove + " " + self.castlingRights + " " + self.enPassant + " " + str(self.halfMoveCounter) + " " + str(self.fullMoveCounter)

    def detect_king_coordinates (self, color):
        """
        Function that detects the coordinates of the king of the given color.

        Parameters:
        - color: The color of the king to detect

        Return:
        - tuple -> The coordinates of the king
        """
        for i in range(8):
            for j in range(8):
                if self.matrix[i][j] is not None and (self.matrix[i][j].get_piece_char() == "K" or self.matrix[i][j].get_piece_char() == "k") and self.matrix[i][j].color == color:
                    return (j, i)
        return None
