class ChessBoard:
    # Generates a chess board from a FEN string
    def __init__(self, fen: str) -> None:
        self.matrix = self.convert_fen_to_matrix(fen)
        self.playerToMove = fen.split(" ")[1]
        self.castlingRights = fen.split(" ")[2]
        self.enPassant = fen.split(" ")[3]
        self.halfMoveCounter = int(fen.split(" ")[4])
        self.fullMoveCounter = int(fen.split(" ")[5])

    # Converts a FEN string to a 2D matrix
    def convert_fen_to_matrix(self, fen: str) -> list[list[str]]:
        matrix = []
        fen = fen.split(" ")[0]
        rows = fen.split("/")
        for row in rows:
            matrix_row = []
            for elem in row:
                if elem.isdigit():
                    for _ in range(int(elem)):
                        matrix_row.append(" ")
                else:
                    matrix_row.append(elem)
            matrix.append(matrix_row)

        return matrix
    
    # Converts a 2D matrix to a FEN string
    def convert_matrix_to_fen(self, matrix: list[list[str]]) -> str:
        fen = ""
        for row in matrix:
            empty = 0
            for elem in row:
                if elem == " ":
                    empty += 1
                else:
                    if empty > 0:
                        fen += str(empty)
                        empty = 0
                    fen += elem
            if empty > 0:
                fen += str(empty)
            fen += "/"
        return fen[:-1]
    
    # Converts the board to a FEN string
    def convert_board_to_fen(self) -> str:
        return self.convert_matrix_to_fen(self.matrix) + " " + self.playerToMove + " " + self.castlingRights + " " + self.enPassant + " " + str(self.halfMoveCounter) + " " + str(self.fullMoveCounter)
