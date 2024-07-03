class ChessBoard:
    def __init__(self, fen: str) -> None:
        self.matrix = self.convert_fen_to_matrix(fen)
        self.playerToMove = fen.split(" ")[1]
        self.castlingRights = fen.split(" ")[2]
        self.enPassant = fen.split(" ")[3]
        self.halfMoveCounter = int(fen.split(" ")[4])
        self.fullMoveCounter = int(fen.split(" ")[5])

    def __init__(self, matrix: list[list[str]], playerToMove: str, castlingRights: str, enPassant: str, halfMoveCounter: int, fullMoveCounter: int) -> None:
        self.matrix = matrix
        self.playerToMove = playerToMove
        self.castlingRights = castlingRights
        self.enPassant = enPassant
        self.halfMoveCounter = halfMoveCounter
        self.fullMoveCounter = fullMoveCounter
    
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
    
    def convert_board_to_fen(self) -> str:
        return self.convert_matrix_to_fen(self.matrix) + " " + self.playerToMove + " " + self.castlingRights + " " + self.enPassant + " " + str(self.halfMoveCounter) + " " + str(self.fullMoveCounter)
